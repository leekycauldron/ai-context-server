from datetime import datetime

def run():
    """Returns the current time as a string."""
    return datetime.now().strftime("%H:%M:%S") 