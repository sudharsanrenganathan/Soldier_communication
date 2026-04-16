# Receiver role (Soldier B) implementation
# Receives, validates, and decrypts secure messages

import sys
import time
import base64
from config import load_config, get_network_config, get_security_config, get_display_config
from crypto_utils import verify_hmac, decrypt_message
from network_utils import create_server_socket, accept_connection, receive_message
from logger import log_attack, get_threat_level, display_threat_level, display_attack_log


def validate_message(message_dict: dict, last_seq_num: int, auth_key: bytes, timestamp_window: int) -> tuple[bool, str]:
    """Validate message security properties.
    
    Args:
        message_dict: Received message dictionary
        last_seq_num: Last valid sequence number seen
        auth_key: HMAC authentication key (32 bytes)
        timestamp_window: Maximum age for timestamps (seconds)
    
    Returns:
        tuple: (is_valid, error_message) where:
            - is_valid: True if message passes all validation checks
            - error_message: Empty string if valid, error description if invalid
    """
    # Check for required fields
    required_fields = ["encrypted_payload", "hmac", "timestamp", "sequence_number"]
    for field in required_fields:
        if field not in message_dict:
            return (False, f"MALFORMED_MESSAGE: Missing field '{field}'")
    
    # 1. Verify HMAC authentication
    encrypted_payload = message_dict["encrypted_payload"]
    hmac_digest = message_dict["hmac"]
    
    if not verify_hmac(encrypted_payload, hmac_digest, auth_key):
        return (False, "FAKE_SENDER: HMAC verification failed")
    
    # 2. Check timestamp freshness
    current_time = time.time()
    message_time = message_dict["timestamp"]
    time_diff = current_time - message_time
    
    # Check for future timestamps
    if time_diff < 0:
        return (False, f"INVALID_TIMESTAMP: Message from future ({abs(time_diff):.0f} seconds)")
    
    # Check if timestamp is too old
    if time_diff > timestamp_window:
        return (False, f"REPLAY_ATTACK: Timestamp too old ({time_diff:.0f} seconds)")
    
    # 3. Validate sequence number
    message_seq_num = message_dict["sequence_number"]
    if message_seq_num <= last_seq_num:
        return (False, f"REPLAY_ATTACK: Sequence number {message_seq_num} not greater than {last_seq_num}")
    
    # All validation checks passed
    return (True, "")


def receive_and_process_message(sock, last_seq_num: int, encryption_key: bytes, auth_key: bytes, timestamp_window: int, colors: dict) -> int:
    """Receive and validate a message.
    
    Args:
        sock: Connected socket
        last_seq_num: Last valid sequence number
        encryption_key: Fernet encryption key
        auth_key: HMAC authentication key
        timestamp_window: Maximum age for timestamps (seconds)
        colors: ANSI color codes dictionary
    
    Returns:
        Updated sequence number if valid, unchanged if invalid
    """
    try:
        # Receive message
        message_dict = receive_message(sock)
        
        # Validate message
        is_valid, error_message = validate_message(message_dict, last_seq_num, auth_key, timestamp_window)
        
        if not is_valid:
            # Log attack
            attack_type = error_message.split(":")[0]
            log_attack(attack_type, error_message, message_dict)
            
            # Display attack
            print(f"{colors['attack']}✗ ATTACK DETECTED: {error_message}{colors['reset']}")
            
            # Return unchanged sequence number
            return last_seq_num
        
        # Decrypt message
        encrypted_payload = message_dict["encrypted_payload"].encode('utf-8')
        plaintext = decrypt_message(encrypted_payload, encryption_key)
        
        # Display decrypted message
        seq_num = message_dict["sequence_number"]
        print(f"{colors['safe']}✓ Message received (seq #{seq_num}): {plaintext}{colors['reset']}")
        
        # Return updated sequence number
        return seq_num
    
    except Exception as e:
        print(f"{colors['attack']}Error processing message: {e}{colors['reset']}")
        return last_seq_num


def main():
    """Main entry point for receiver role."""
    print("\n" + "="*50)
    print("  SECURE SOLDIER-TO-SOLDIER COMMUNICATION")
    print("  Role: RECEIVER (Soldier B)")
    print("="*50 + "\n")
    
    # Load configuration
    try:
        load_config()
        network_config = get_network_config()
        security_config = get_security_config()
        display_config = get_display_config()
        colors = display_config['colors']
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    
    # Load encryption and authentication keys
    try:
        # Fernet key is already base64-encoded, just encode to bytes
        encryption_key = security_config['encryption_key'].encode('utf-8')
        auth_key = base64.b64decode(security_config['auth_key'])
        timestamp_window = security_config['timestamp_window']
    except Exception as e:
        print(f"Error loading keys: {e}")
        print("Run setup.py to generate keys")
        sys.exit(1)
    
    # Create server socket
    receiver_ip = '0.0.0.0'  # Listen on all interfaces
    receiver_port = network_config['receiver_port']
    
    print(f"{colors['info']}Starting receiver on port {receiver_port}...{colors['reset']}")
    server_socket = create_server_socket(receiver_ip, receiver_port)
    print(f"{colors['safe']}✓ Receiver listening on port {receiver_port}{colors['reset']}")
    
    # Display initial threat level
    display_threat_level(colors)
    
    # Initialize sequence number tracking
    last_seq_num = 0
    
    print(f"{colors['info']}Waiting for connections...{colors['reset']}\n")
    
    try:
        while True:
            # Accept connection
            client_socket, client_address = accept_connection(server_socket)
            print(f"{colors['info']}Connection from {client_address[0]}:{client_address[1]}{colors['reset']}\n")
            
            try:
                # Continuous message reception loop
                while True:
                    # Receive and process message
                    last_seq_num = receive_and_process_message(
                        client_socket, 
                        last_seq_num, 
                        encryption_key, 
                        auth_key, 
                        timestamp_window,
                        colors
                    )
                    
                    # Display threat level after each message
                    display_threat_level(colors)
            
            except ConnectionResetError:
                print(f"{colors['info']}Connection closed by peer{colors['reset']}\n")
                print(f"{colors['info']}Waiting for new connection...{colors['reset']}\n")
            
            except Exception as e:
                print(f"{colors['attack']}Error: {e}{colors['reset']}")
                print(f"{colors['info']}Waiting for new connection...{colors['reset']}\n")
            
            finally:
                client_socket.close()
                
                # Display attack log if any attacks detected
                if get_threat_level().value != "SAFE":
                    display_attack_log(colors)
    
    except KeyboardInterrupt:
        print(f"\n\n{colors['info']}Receiver shutting down...{colors['reset']}")
        
        # Display final attack log
        display_attack_log(colors)
        display_threat_level(colors)
    
    finally:
        server_socket.close()
        print(f"{colors['info']}Server socket closed.{colors['reset']}\n")


if __name__ == "__main__":
    main()
