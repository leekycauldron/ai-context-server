count = 0

def run():
    """Returns the number of times this plugin has been called."""
    global count
    count += 1
    return f"Called {count} times" 