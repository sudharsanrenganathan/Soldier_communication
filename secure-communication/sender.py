# Sender role (Soldier A) implementation
# Encrypts and sends secure messages to receiver

import sys
import time
import base64
from config import load_config, get_network_config, get_security_config, get_display_config
from crypto_utils import encrypt_message, generate_hmac
from network_utils import create_client_socket, send_message


def send_secure_message(message: str, sock, seq_num: int, encryption_key: bytes, auth_key: bytes) -> None:
    """Encrypt and send a secure message.
    
    Args:
        message: Plaintext message to send
        sock: Connected socket to receiver
        seq_num: Current sequence number
        encryption_key: Fernet encryption key
        auth_key: HMAC authentication key
    """
    # 1. Encrypt the message
    encrypted_payload = encrypt_message(message, encryption_key)
    
    # 2. Convert encrypted payload to base64 string for JSON serialization
    encrypted_payload_str = encrypted_payload.decode('utf-8')
    
    # 3. Generate HMAC of the encrypted payload
    hmac_digest = generate_hmac(encrypted_payload_str, auth_key)
    
    # 4. Attach timestamp
    timestamp = time.time()
    
    # 5. Package as JSON message
    message_dict = {
        "encrypted_payload": encrypted_payload_str,
        "hmac": hmac_digest,
        "timestamp": timestamp,
        "sequence_number": seq_num
    }
    
    # 6. Send message
    send_message(sock, message_dict)


def main():
    """Main entry point for sender role."""
    print("\n" + "="*50)
    print("  SECURE SOLDIER-TO-SOLDIER COMMUNICATION")
    print("  Role: SENDER (Soldier A)")
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
    except Exception as e:
        print(f"Error loading keys: {e}")
        print("Run setup.py to generate keys")
        sys.exit(1)
    
    # Connect to receiver
    receiver_ip = network_config['receiver_ip']
    receiver_port = network_config['receiver_port']
    timeout = network_config['timeout']
    
    print(f"{colors['info']}Connecting to receiver at {receiver_ip}:{receiver_port}...{colors['reset']}")
    sock = create_client_socket(receiver_ip, receiver_port, timeout)
    print(f"{colors['safe']}✓ Connected successfully!{colors['reset']}\n")
    
    # Initialize sequence number
    seq_num = 1
    
    # User input loop
    print(f"{colors['info']}Enter messages to send (Ctrl+C to exit):{colors['reset']}\n")
    
    try:
        while True:
            # Get user input
            message = input(f"{colors['info']}Message > {colors['reset']}")
            
            if not message.strip():
                continue
            
            try:
                # Send secure message
                send_secure_message(message, sock, seq_num, encryption_key, auth_key)
                
                # Display confirmation
                print(f"{colors['safe']}✓ Message sent (seq #{seq_num}): {message}{colors['reset']}\n")
                
                # Increment sequence number
                seq_num += 1
            
            except Exception as e:
                print(f"{colors['attack']}Error sending message: {e}{colors['reset']}")
                print(f"{colors['attack']}Connection may be lost. Exiting...{colors['reset']}")
                break
    
    except KeyboardInterrupt:
        print(f"\n\n{colors['info']}Sender shutting down...{colors['reset']}")
    
    finally:
        sock.close()
        print(f"{colors['info']}Connection closed.{colors['reset']}\n")


if __name__ == "__main__":
    main()
