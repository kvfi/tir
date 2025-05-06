import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class MultiPathHandler(PatternMatchingEventHandler):
    def __init__(self, callback_function, patterns=None, ignore_patterns=None):
        # Set up patterns
        # Default is to watch all files
        if patterns is None:
            patterns = ["*"]

        # Default is to ignore nothing
        if ignore_patterns is None:
            ignore_patterns = []

        # Initialize the pattern handler with our settings
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=False,
            case_sensitive=True
        )

        self.callback_function = callback_function

    def on_any_event(self, event):
        if event.is_directory:
            return

        print(f"Change detected: {event.src_path} - Event type: {event.event_type}")
        self.callback_function(event)


def watch_multiple_directories(paths_to_watch, callback, patterns=None, ignore_patterns=None):
    """
    Watch multiple directories with pattern filtering

    Args:
        paths_to_watch: List of directory paths to watch
        callback: Function to call when changes are detected
        patterns: List of glob patterns to watch (e.g. ["*.py", "*.txt"])
        ignore_patterns: List of glob patterns to ignore (e.g. ["*.tmp", "*.log"])
    """
    # Create the event handler
    event_handler = MultiPathHandler(
        callback,
        patterns=patterns,
        ignore_patterns=ignore_patterns
    )

    # Create an observer
    observer = Observer()

    # Schedule monitoring for each path
    for path in paths_to_watch:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
            print(f"Watching: {path}")
        else:
            print(f"Warning: Path does not exist: {path}")

    # Start the observer
    observer.start()

    try:
        print("File watcher started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
