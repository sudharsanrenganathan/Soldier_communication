# Attacker role (Hacker) implementation
# Intercepts messages and performs replay attacks

import sys
import socket
import time
from config import load_config, get_network_config, get_display_config
from network_utils import create_client_socket, send_message, receive_message


# Storage for captured messages
captured_messages = []


def display_captured_messages(messages: list[dict], colors: dict) -> None:
    """Display list of captured messages with indices.
    
    Args:
        messages: List of captured message dictionaries
        colors: ANSI color codes dictionary
    """
    if not messages:
        print(f"{colors['attacker']}No messages captured yet.{colors['reset']}\n")
        return
    
    print(f"\n{colors['attacker']}=== CAPTURED MESSAGES ==={colors['reset']}")
    for i, msg in enumerate(messages, 1):
        encrypted_payload = msg.get('encrypted_payload', '')
        truncated = encrypted_payload[:50] + "..." if len(encrypted_payload) > 50 else encrypted_payload
        timestamp = msg.get('timestamp', 0)
        seq_num = msg.get('sequence_number', 0)
        
        print(f"{colors['attacker']}[{i}] Seq #{seq_num} | Time: {time.strftime('%H:%M:%S', time.localtime(timestamp))}{colors['reset']}")
        print(f"{colors['attacker']}    Encrypted: {truncated}{colors['reset']}")
    print()


def capture_message_from_sender(receiver_ip: str, receiver_port: int, colors: dict) -> dict:
    """Capture a message by acting as a man-in-the-middle (simplified simulation).
    
    For demonstration purposes, this function prompts the attacker to manually
    trigger capture when they know a message is being sent.
    
    Args:
        receiver_ip: IP address of receiver
        receiver_port: Port of receiver
        colors: ANSI color codes dictionary
    
    Returns:
        Captured message dictionary
    """
    print(f"{colors['attacker']}Waiting to intercept message...{colors['reset']}")
    print(f"{colors['info']}(In a real scenario, this would passively sniff network traffic){colors['reset']}")
    print(f"{colors['info']}For this demo, we'll connect as a client and receive a message{colors['reset']}\n")
    
    try:
        # Connect to receiver (simulating interception)
        sock = create_client_socket(receiver_ip, receiver_port, timeout=60)
        
        # Wait for sender to send a message (we'll receive it)
        print(f"{colors['attacker']}Connected. Waiting for message transmission...{colors['reset']}")
        
        # In a real attack, we'd sniff packets. For demo, we receive directly.
        # This simulates the attacker being on the same network
        input(f"{colors['info']}Press Enter after sender sends a message...{colors['reset']}")
        
        sock.close()
        
        # For demo purposes, return a placeholder
        # In reality, packet sniffing would capture the actual message
        print(f"{colors['attack']}Note: In this simplified demo, manually provide message details{colors['reset']}")
        return None
        
    except Exception as e:
        print(f"{colors['attack']}Error during capture: {e}{colors['reset']}")
        return None


def replay_message(message_dict: dict, target_ip: str, target_port: int, colors: dict) -> None:
    """Replay a captured message to the receiver.
    
    Args:
        message_dict: Previously captured message
        target_ip: Receiver IP address
        target_port: Receiver port
        colors: ANSI color codes dictionary
    """
    try:
        print(f"{colors['attacker']}Connecting to receiver at {target_ip}:{target_port}...{colors['reset']}")
        sock = create_client_socket(target_ip, target_port, timeout=30)
        
        print(f"{colors['attacker']}Replaying captured message...{colors['reset']}")
        send_message(sock, message_dict)
        
        print(f"{colors['attack']}✓ REPLAY ATTACK EXECUTED!{colors['reset']}")
        print(f"{colors['attacker']}Message sent to receiver (should be detected as replay){colors['reset']}\n")
        
        sock.close()
    
    except Exception as e:
        print(f"{colors['attack']}Error during replay: {e}{colors['reset']}\n")


def manual_message_entry(colors: dict) -> dict:
    """Manually enter a captured message (for demo purposes).
    
    Args:
        colors: ANSI color codes dictionary
    
    Returns:
        Message dictionary
    """
    print(f"\n{colors['info']}=== MANUAL MESSAGE CAPTURE ==={colors['reset']}")
    print(f"{colors['info']}(Simulating packet interception){colors['reset']}\n")
    
    encrypted_payload = input(f"{colors['attacker']}Encrypted payload: {colors['reset']}")
    hmac = input(f"{colors['attacker']}HMAC: {colors['reset']}")
    timestamp = float(input(f"{colors['attacker']}Timestamp: {colors['reset']}"))
    seq_num = int(input(f"{colors['attacker']}Sequence number: {colors['reset']}"))
    
    message_dict = {
        "encrypted_payload": encrypted_payload,
        "hmac": hmac,
        "timestamp": timestamp,
        "sequence_number": seq_num
    }
    
    print(f"{colors['attack']}✓ Message captured!{colors['reset']}\n")
    return message_dict


def main():
    """Main entry point for attacker role."""
    print("\n" + "="*50)
    print("  SECURE SOLDIER-TO-SOLDIER COMMUNICATION")
    print("  Role: ATTACKER (Hacker)")
    print("="*50 + "\n")
    
    # Load configuration (NO encryption/auth keys)
    try:
        load_config()
        network_config = get_network_config()
        display_config = get_display_config()
        colors = display_config['colors']
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    
    receiver_ip = network_config['receiver_ip']
    receiver_port = network_config['receiver_port']
    
    print(f"{colors['attacker']}Target: {receiver_ip}:{receiver_port}{colors['reset']}")
    print(f"{colors['attack']}⚠ Attacker has NO encryption or authentication keys{colors['reset']}")
    print(f"{colors['attack']}⚠ Can only see encrypted data and replay captured messages{colors['reset']}\n")
    
    try:
        while True:
            print(f"{colors['attacker']}=== ATTACKER MENU ==={colors['reset']}")
            print(f"{colors['info']}1. Capture message (manual entry){colors['reset']}")
            print(f"{colors['info']}2. View captured messages{colors['reset']}")
            print(f"{colors['info']}3. Replay captured message{colors['reset']}")
            print(f"{colors['info']}4. Exit{colors['reset']}\n")
            
            choice = input(f"{colors['attacker']}Select option: {colors['reset']}")
            
            if choice == '1':
                # Capture message
                message = manual_message_entry(colors)
                if message:
                    captured_messages.append(message)
                    print(f"{colors['attack']}Total captured: {len(captured_messages)}{colors['reset']}\n")
            
            elif choice == '2':
                # View captured messages
                display_captured_messages(captured_messages, colors)
            
            elif choice == '3':
                # Replay message
                if not captured_messages:
                    print(f"{colors['attack']}No messages to replay. Capture a message first.{colors['reset']}\n")
                    continue
                
                display_captured_messages(captured_messages, colors)
                
                try:
                    index = int(input(f"{colors['attacker']}Select message number to replay: {colors['reset']}"))
                    if 1 <= index <= len(captured_messages):
                        message = captured_messages[index - 1]
                        replay_message(message, receiver_ip, receiver_port, colors)
                    else:
                        print(f"{colors['attack']}Invalid message number{colors['reset']}\n")
                except ValueError:
                    print(f"{colors['attack']}Invalid input{colors['reset']}\n")
            
            elif choice == '4':
                print(f"{colors['info']}Exiting attacker...{colors['reset']}\n")
                break
            
            else:
                print(f"{colors['attack']}Invalid option{colors['reset']}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{colors['info']}Attacker shutting down...{colors['reset']}\n")


if __name__ == "__main__":
    main()
