# Cryptographic utilities for encryption and authentication
# Implements AES-256-GCM encryption (upgraded from Fernet for enhanced security)
# AES-256-GCM provides authenticated encryption with associated data (AEAD)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.fernet import Fernet, InvalidToken
import hmac
import hashlib
import os
import base64


def encrypt_message(plaintext: str, key: bytes) -> bytes:
    """Encrypt message using AES-256-GCM encryption.
    
    AES-256-GCM provides:
    - 256-bit key strength (stronger than Fernet's AES-128)
    - Authenticated encryption (integrity + confidentiality in one operation)
    - Galois/Counter Mode for parallel processing and performance
    
    Args:
        plaintext: Message to encrypt
        key: Encryption key (32 bytes for AES-256, or base64-encoded Fernet key for compatibility)
    
    Returns:
        Encrypted message as bytes (nonce + ciphertext + tag, base64-encoded)
    
    Raises:
        ValueError: If key is invalid
        TypeError: If plaintext is not a string
    """
    try:
        # Check if key is base64-encoded Fernet key (for backward compatibility)
        if len(key) == 44 and key.endswith(b'='):
            # Decode Fernet key to get raw 32 bytes
            key = base64.urlsafe_b64decode(key)
        
        # Ensure key is exactly 32 bytes for AES-256
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        
        # Create AES-GCM cipher
        aesgcm = AESGCM(key)
        
        # Generate random 96-bit (12-byte) nonce (recommended for GCM)
        nonce = os.urandom(12)
        
        # Encode plaintext to bytes (UTF-8) and encrypt
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Encrypt and authenticate (GCM provides both)
        # Returns ciphertext + 16-byte authentication tag
        ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
        
        # Combine nonce + ciphertext for transmission
        # Format: [12-byte nonce][ciphertext + 16-byte tag]
        encrypted_data = nonce + ciphertext
        
        # Base64 encode for JSON serialization
        return base64.b64encode(encrypted_data)
    
    except ValueError as e:
        raise ValueError(f"Invalid encryption key: {e}")
    except AttributeError:
        raise TypeError("Plaintext must be a string")


def decrypt_message(ciphertext: bytes, key: bytes) -> str:
    """Decrypt message using AES-256-GCM decryption.
    
    AES-256-GCM automatically verifies authentication tag during decryption,
    ensuring both confidentiality and integrity.
    
    Args:
        ciphertext: Encrypted message (base64-encoded: nonce + ciphertext + tag)
        key: Encryption key (32 bytes for AES-256, or base64-encoded Fernet key for compatibility)
    
    Returns:
        Decrypted plaintext string
    
    Raises:
        ValueError: If decryption fails or message is tampered
    """
    try:
        # Check if key is base64-encoded Fernet key (for backward compatibility)
        if len(key) == 44 and key.endswith(b'='):
            # Decode Fernet key to get raw 32 bytes
            key = base64.urlsafe_b64decode(key)
        
        # Ensure key is exactly 32 bytes for AES-256
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        
        # Base64 decode the encrypted data
        encrypted_data = base64.b64decode(ciphertext)
        
        # Extract nonce (first 12 bytes) and ciphertext (remaining bytes)
        nonce = encrypted_data[:12]
        ciphertext_with_tag = encrypted_data[12:]
        
        # Create AES-GCM cipher
        aesgcm = AESGCM(key)
        
        # Decrypt and verify authentication tag
        # Raises exception if tag verification fails (message tampered)
        plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
        
        # Decode to string (UTF-8)
        plaintext = plaintext_bytes.decode('utf-8')
        
        return plaintext
    
    except Exception as e:
        raise ValueError(f"Decryption failed - message may be corrupted or tampered: {e}")



def generate_hmac(message: str, key: bytes) -> str:
    """Generate HMAC-SHA256 authentication token.
    
    Args:
        message: Message to authenticate (will be encoded to UTF-8)
        key: HMAC secret key (32 bytes)
    
    Returns:
        Hex-encoded HMAC digest (64 characters)
    """
    # Encode message to bytes if it's a string
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
    
    # Generate HMAC-SHA256
    hmac_obj = hmac.new(key, message_bytes, hashlib.sha256)
    
    # Return hex-encoded digest
    return hmac_obj.hexdigest()


def verify_hmac(message: str, hmac_digest: str, key: bytes) -> bool:
    """Verify HMAC authentication token.
    
    Args:
        message: Original message (will be encoded to UTF-8)
        hmac_digest: Hex-encoded HMAC to verify
        key: HMAC secret key (32 bytes)
    
    Returns:
        True if HMAC is valid, False otherwise
    """
    # Generate expected HMAC
    expected_hmac = generate_hmac(message, key)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_hmac, hmac_digest)
