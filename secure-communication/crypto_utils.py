# Cryptographic utilities for encryption and authentication
# Implements Fernet encryption and HMAC-SHA256 authentication

from cryptography.fernet import Fernet, InvalidToken
import hmac
import hashlib


def encrypt_message(plaintext: str, key: bytes) -> bytes:
    """Encrypt message using Fernet encryption.
    
    Args:
        plaintext: Message to encrypt
        key: Fernet encryption key (32 bytes, base64-encoded)
    
    Returns:
        Encrypted message as bytes (base64-encoded by Fernet)
    
    Raises:
        InvalidToken: If key is invalid
        TypeError: If plaintext is not a string
    """
    try:
        # Create Fernet cipher with the provided key
        cipher = Fernet(key)
        
        # Encode plaintext to bytes (UTF-8) and encrypt
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = cipher.encrypt(plaintext_bytes)
        
        return ciphertext
    
    except InvalidToken:
        raise InvalidToken("Invalid encryption key")
    except AttributeError:
        raise TypeError("Plaintext must be a string")


def decrypt_message(ciphertext: bytes, key: bytes) -> str:
    """Decrypt message using Fernet decryption.
    
    Args:
        ciphertext: Encrypted message (base64-encoded bytes)
        key: Fernet encryption key (32 bytes, base64-encoded)
    
    Returns:
        Decrypted plaintext string
    
    Raises:
        InvalidToken: If decryption fails or message is tampered
    """
    try:
        # Create Fernet cipher with the provided key
        cipher = Fernet(key)
        
        # Decrypt and decode to string (UTF-8)
        plaintext_bytes = cipher.decrypt(ciphertext)
        plaintext = plaintext_bytes.decode('utf-8')
        
        return plaintext
    
    except InvalidToken:
        raise InvalidToken("Decryption failed - message may be corrupted or tampered")
    except Exception as e:
        raise InvalidToken(f"Decryption error: {e}")



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
