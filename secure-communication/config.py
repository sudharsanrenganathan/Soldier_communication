# Configuration module for Secure Soldier-to-Soldier Communication Network
# This module handles configuration loading and cryptographic key generation

import json
import secrets
import base64
import sys
from pathlib import Path
from cryptography.fernet import Fernet


def generate_keys() -> tuple[bytes, bytes]:
    """Generate encryption and authentication keys.
    
    Returns:
        tuple: (encryption_key, auth_key) where:
            - encryption_key: Fernet encryption key (32 bytes, base64-encoded)
            - auth_key: HMAC authentication key (32 bytes, raw bytes)
    """
    # Generate Fernet encryption key (32 bytes, base64-encoded)
    encryption_key = Fernet.generate_key()
    
    # Generate HMAC authentication key (32 bytes, raw bytes)
    auth_key = secrets.token_bytes(32)
    
    return encryption_key, auth_key



# Global configuration storage
_config = None


def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file (default: config.json)
    
    Returns:
        dict: Configuration dictionary
    
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        json.JSONDecodeError: If configuration file is invalid JSON
        KeyError: If required configuration keys are missing
    """
    global _config
    
    try:
        with open(config_path, 'r') as f:
            _config = json.load(f)
        
        # Validate required top-level keys
        required_keys = ['network', 'security', 'display']
        for key in required_keys:
            if key not in _config:
                raise KeyError(f"Missing required configuration section: '{key}'")
        
        return _config
    
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found")
        print("Run setup.py to generate keys and configuration")
        sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)
    
    except KeyError as e:
        print(f"Error: {e}")
        sys.exit(1)


def get_network_config() -> dict:
    """Extract network configuration parameters.
    
    Returns:
        dict: Network configuration with keys:
            - receiver_ip: IP address of receiver
            - receiver_port: Port number for receiver
            - buffer_size: Socket buffer size
            - timeout: Connection timeout in seconds
    
    Raises:
        RuntimeError: If configuration hasn't been loaded
    """
    if _config is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    
    return _config['network']


def get_security_config() -> dict:
    """Extract security configuration parameters.
    
    Returns:
        dict: Security configuration with keys:
            - encryption_key: Base64-encoded Fernet encryption key
            - auth_key: Base64-encoded HMAC authentication key
            - timestamp_window: Maximum age for timestamps (seconds)
            - replay_window: Window for sequence number tracking (seconds)
    
    Raises:
        RuntimeError: If configuration hasn't been loaded
    """
    if _config is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    
    return _config['security']


def get_display_config() -> dict:
    """Extract display/color configuration parameters.
    
    Returns:
        dict: Display configuration with color codes:
            - colors: Dictionary of ANSI color codes
    
    Raises:
        RuntimeError: If configuration hasn't been loaded
    """
    if _config is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    
    return _config['display']
