"""
SORA 2 Watermark Remover - Professional Video Processing Suite
Main Entry Point
"""

import sys
sys.path.insert(0, '.')
try:
    from processing import sora_process
except:
    pass

import webbrowser
import threading
import time
import logging
from core.server import WebServer
from core.utils import get_free_port, display_banner


def open_browser(port):
    """Auto-open browser after server starts"""
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')


def main():
    """Main application entry point"""
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    display_banner()
    
    port = get_free_port(8081)
    
    print(f"[INFO] Initializing SORA 2 Watermark Remover v2.3.1")
    print(f"[INFO] Starting web server on http://127.0.0.1:{port}")
    print(f"[INFO] Opening browser...")
    print(f"[INFO] Press Ctrl+C to stop the server\n")
    
    browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
    browser_thread.start()
    
    try:
        server = WebServer(port)
        server.start()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
