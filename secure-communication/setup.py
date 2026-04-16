#!/usr/bin/env python3
"""
Setup script for Secure Soldier-to-Soldier Communication Network
Generates encryption and authentication keys and updates config.json
"""

import json
import base64
import sys
from pathlib import Path
from config import generate_keys


def main():
    """Generate keys and update configuration file."""
    print("\n" + "="*60)
    print("  SECURE SOLDIER-TO-SOLDIER COMMUNICATION - SETUP")
    print("="*60 + "\n")
    
    config_file = Path("config.json")
    
    # Check if config file exists
    if not config_file.exists():
        print("Error: config.json not found")
        print("Please ensure you're running this from the secure-communication directory")
        sys.exit(1)
    
    # Load existing configuration
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {e}")
        sys.exit(1)
    
    # Generate keys
    print("Generating cryptographic keys...")
    encryption_key, auth_key = generate_keys()
    
    # Encode keys to base64 strings for JSON storage
    encryption_key_b64 = encryption_key.decode('utf-8')  # Fernet key is already base64
    auth_key_b64 = base64.b64encode(auth_key).decode('utf-8')
    
    # Update configuration
    config['security']['encryption_key'] = encryption_key_b64
    config['security']['auth_key'] = auth_key_b64
    
    # Save updated configuration
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("✓ Keys generated and saved to config.json\n")
    except Exception as e:
        print(f"Error saving config.json: {e}")
        sys.exit(1)
    
    # Display keys
    print("="*60)
    print("GENERATED KEYS (for reference)")
    print("="*60)
    print(f"\nEncryption Key (Fernet):")
    print(f"  {encryption_key_b64}\n")
    print(f"Authentication Key (HMAC):")
    print(f"  {auth_key_b64}\n")
    
    # Instructions
    print("="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. COPY this entire 'secure-communication' folder to all 3 laptops")
    print("\n2. On each laptop, update config.json with the correct IP addresses:")
    print("   - Laptop A (Sender): No changes needed")
    print("   - Laptop B (Receiver): Set 'receiver_ip' to Laptop B's IP address")
    print("   - Laptop C (Attacker): Set 'receiver_ip' to Laptop B's IP address")
    
    print("\n3. Ensure all laptops are on the SAME WiFi network")
    
    print("\n4. Install dependencies on all laptops:")
    print("   pip install -r requirements.txt")
    
    print("\n5. Run the demonstration:")
    print("   - Laptop B (Receiver): python receiver.py")
    print("   - Laptop C (Attacker):  python attacker.py")
    print("   - Laptop A (Sender):    python sender.py")
    
    print("\n" + "="*60)
    print("Setup complete! Ready for demonstration.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
