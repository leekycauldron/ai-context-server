import os
import importlib.util
import time
from typing import Any, Dict

def load_plugins(plugin_dir: str = "plugins") -> Dict[str, Any]:
    """
    Load all Python plugins from the specified directory.
    Returns a dictionary of plugin names and their module objects.
    """
    plugins = {}
    
    # Ensure plugin directory exists
    if not os.path.exists(plugin_dir):
        print(f"Creating plugin directory: {plugin_dir}")
        os.makedirs(plugin_dir)
        return plugins

    # Get all Python files in the plugin directory
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py"):
            plugin_name = filename[:-3]  # Remove .py extension
            plugin_path = os.path.join(plugin_dir, filename)
            
            try:
                # Load the plugin module
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Check if the module has a run function
                    if hasattr(module, "run"):
                        plugins[plugin_name] = module
                        print(f"Successfully loaded plugin: {plugin_name}")
                    else:
                        print(f"Warning: Plugin {plugin_name} does not have a run function")
            except Exception as e:
                print(f"Error loading plugin {plugin_name}: {str(e)}")
    
    return plugins

def main(interval: float = 5.0):
    """
    Main loop that runs plugins at specified intervals.
    
    Args:
        interval (float): Time in seconds between plugin execution cycles
    """
    print(f"Starting plugin monitor (interval: {interval} seconds)")
    
    while True:
        # Load/reload plugins on each iteration
        plugins = load_plugins()
        
        if not plugins:
            print("No plugins found. Waiting for plugins to be added...")
        else:
            print("\nExecuting plugins:")
            print("-" * 40)
            
            # Execute each plugin
            for plugin_name, plugin in plugins.items():
                try:
                    result = plugin.run()
                    print(f"{plugin_name}: {result}")
                except Exception as e:
                    print(f"Error executing {plugin_name}: {str(e)}")
            
            print("-" * 40)
        
        time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down plugin monitor...")
