# Network utilities for TCP socket communication
# Handles server/client socket creation and message transmission

import socket
import json
import struct
import sys


def create_server_socket(host: str, port: int) -> socket.socket:
    """Create and bind TCP server socket.
    
    Args:
        host: IP address to bind to (use '0.0.0.0' for all interfaces)
        port: Port number to listen on
    
    Returns:
        Configured server socket ready to accept connections
    
    Raises:
        OSError: If port is already in use or binding fails
    """
    try:
        # Create TCP socket (IPv4, SOCK_STREAM)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR option for quick port reuse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to address and port
        server_socket.bind((host, port))
        
        # Listen for incoming connections (backlog of 5)
        server_socket.listen(5)
        
        return server_socket
    
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:  # Address already in use (Linux/Windows)
            print(f"Error: Port {port} is already in use")
            print(f"Change the port in config.json or stop the process using this port")
        else:
            print(f"Error creating server socket: {e}")
        sys.exit(1)


def accept_connection(server_socket: socket.socket) -> tuple[socket.socket, tuple]:
    """Accept incoming client connection.
    
    Args:
        server_socket: Listening server socket
    
    Returns:
        tuple: (client_socket, client_address) where:
            - client_socket: Socket for communication with client
            - client_address: Tuple of (ip_address, port)
    """
    client_socket, client_address = server_socket.accept()
    return client_socket, client_address



def create_client_socket(host: str, port: int, timeout: int = 30) -> socket.socket:
    """Create and connect TCP client socket.
    
    Args:
        host: Receiver IP address
        port: Receiver port number
        timeout: Connection timeout in seconds (default: 30)
    
    Returns:
        Connected client socket
    
    Raises:
        ConnectionRefusedError: If receiver is not available
        socket.timeout: If connection times out
    """
    try:
        # Create TCP socket (IPv4, SOCK_STREAM)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set connection timeout
        client_socket.settimeout(timeout)
        
        # Connect to receiver
        client_socket.connect((host, port))
        
        return client_socket
    
    except ConnectionRefusedError:
        print(f"Error: Cannot connect to receiver at {host}:{port}")
        print("Ensure receiver is running and network is configured correctly")
        sys.exit(1)
    
    except socket.timeout:
        print(f"Error: Connection timeout after {timeout} seconds")
        print(f"Check if receiver at {host}:{port} is reachable")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error connecting to receiver: {e}")
        sys.exit(1)



def send_message(sock: socket.socket, message_dict: dict) -> None:
    """Send JSON message over TCP socket with length prefix.
    
    Args:
        sock: Connected socket
        message_dict: Message data as dictionary
    
    Raises:
        BrokenPipeError: If connection is lost
        OSError: If transmission fails
    """
    try:
        # Serialize message to JSON
        message_json = json.dumps(message_dict)
        message_bytes = message_json.encode('utf-8')
        
        # Create 4-byte length prefix (network byte order)
        message_length = len(message_bytes)
        length_prefix = struct.pack('!I', message_length)
        
        # Send length prefix followed by message
        sock.sendall(length_prefix + message_bytes)
    
    except BrokenPipeError:
        print("Error: Connection lost during transmission")
        raise
    
    except OSError as e:
        print(f"Network error during send: {e}")
        raise


def receive_message(sock: socket.socket, buffer_size: int = 4096) -> dict:
    """Receive JSON message from TCP socket with length prefix.
    
    Args:
        sock: Connected socket
        buffer_size: Maximum bytes to receive (default: 4096)
    
    Returns:
        Parsed message dictionary
    
    Raises:
        ConnectionResetError: If connection is lost
        json.JSONDecodeError: If message is malformed
        ValueError: If message length is invalid
    """
    try:
        # Receive 4-byte length prefix
        length_data = sock.recv(4)
        if not length_data:
            raise ConnectionResetError("Connection closed by peer")
        
        # Unpack message length (network byte order)
        message_length = struct.unpack('!I', length_data)[0]
        
        # Validate message length
        if message_length > buffer_size:
            raise ValueError(f"Message too large: {message_length} bytes (max: {buffer_size})")
        
        # Receive message data
        message_bytes = b''
        while len(message_bytes) < message_length:
            chunk = sock.recv(min(message_length - len(message_bytes), buffer_size))
            if not chunk:
                raise ConnectionResetError("Connection closed during message reception")
            message_bytes += chunk
        
        # Decode and parse JSON
        message_json = message_bytes.decode('utf-8')
        message_dict = json.loads(message_json)
        
        return message_dict
    
    except ConnectionResetError:
        print("Error: Connection reset by peer")
        raise
    
    except json.JSONDecodeError as e:
        print(f"Error: Received malformed message: {e}")
        raise
    
    except Exception as e:
        print(f"Error receiving message: {e}")
        raise
