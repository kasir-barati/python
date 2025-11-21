"""Development runner that handles hot reload signals gracefully."""
import sys
import signal

def signal_handler(signal_number: int, frame):
    """Handle termination signals gracefully during development."""
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Import and run the main application
if __name__ == "__main__":
    try:
        import main
    except (KeyboardInterrupt, SystemExit):
        # Suppress the traceback on hot reload
        sys.exit(0)
