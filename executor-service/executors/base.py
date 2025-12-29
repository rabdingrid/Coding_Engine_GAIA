"""Base executor class"""
import tempfile
import shutil
import os

def create_sandboxed_directory() -> str:
    """Create a sandboxed temporary directory"""
    temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
    os.chmod(temp_dir, 0o700)
    return temp_dir

