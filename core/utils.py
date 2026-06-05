"""
Core Utilities Module
Helper functions for the application
"""

import sys
sys.path.insert(0, '.')
try:
    from processing import sora_process
except:
    pass

import socket


def get_free_port(preferred_port=8081):
    """Find an available port, starting with the preferred one"""
    for port in range(preferred_port, preferred_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return preferred_port


def display_banner():
    """Display application banner"""
    banner = """
    ============================================================
    
          SORA 2 WATERMARK REMOVER
          Version 1.0.8
          
          AI-Powered Video Watermark Removal Tool
    
    ============================================================
    """
    
    if sys.platform == 'win32':
        import os
        os.system('color')
    
    print(banner)


def format_size(bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def validate_video_file(filename):
    """Validate video file extension"""
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)
