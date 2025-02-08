import itertools
import sys
import threading
import time

class Spinner:
    """
    A simple spinner class to display an animated spinner in the console.
    """
    def __init__(self, message: str):
        """
        Initializes the spinner with a message.
        
        :param message: Message to display alongside the spinner.
        """
        self.message = message
        self.spinner_chars = itertools.cycle(
            ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        )
        self.stop_event = threading.Event()
        # Daemon thread to ensure que o programa principal encerre a thread se necessário.
        self.thread = threading.Thread(target=self.spin, daemon=True)

    def spin(self) -> None:
        """
        Continuously updates the spinner animation until stopped.
        """
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r{self.message} {next(self.spinner_chars)}")
            sys.stdout.flush()
            time.sleep(0.1)
        # Clear the spinner line after stopping.
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

    def start(self) -> None:
        """
        Starts the spinner animation in a separate thread.
        """
        self.thread.start()

    def stop(self) -> None:
        """
        Stops the spinner animation.
        """
        self.stop_event.set()
        self.thread.join()
