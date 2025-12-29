"""Network access blocking"""
import socket

def block_network_access():
    """Block network access during code execution"""
    original_socket = socket.socket
    
    def blocked_socket(*args, **kwargs):
        raise PermissionError("Network access is not allowed")
    
    socket.socket = blocked_socket
    return original_socket

def restore_network_access(original_socket):
    """Restore network access after code execution"""
    socket.socket = original_socket

