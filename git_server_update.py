import os
import json
import subprocess
from typing import Dict, Any
from datetime import datetime

def run_git_command(cmd: list[str]) -> tuple[bool, str]:
    """
    Run a git command and return the result
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stderr if result.returncode != 0 else result.stdout
    except Exception as e:
        return False, str(e)

def init_git_repo() -> bool:
    """
    Initialize git repository if needed and set up remote
    """
    # Check if git repo exists
    if not os.path.exists('.git'):
        success, output = run_git_command(['git', 'init'])
        if not success:
            print(f"Failed to initialize git repository: {output}")
            return False

    # Check remote and add if needed
    success, output = run_git_command(['git', 'remote', 'get-url', 'origin'])
    if not success:
        success, output = run_git_command([
            'git', 'remote', 'add', 'origin',
            'https://github.com/leekycauldron/ai-context-server.git'
        ])
        if not success:
            print(f"Failed to add remote: {output}")
            return False

    # Pull latest changes with unrelated histories allowed
    success, output = run_git_command([
        'git', 'pull', 'origin', 'master', '--allow-unrelated-histories'
    ])
    if not success and "refusing to merge unrelated histories" in output:
        print("Note: Repository has unrelated histories, continuing with local changes")
    
    return True

def update_context_json(payload: Dict[str, Any]) -> bool:
    """
    Updates the local context.json file and pushes changes to GitHub.
    
    Args:
        payload (Dict[str, Any]): The JSON payload to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize git repository if needed
        if not init_git_repo():
            return False

        # Save the payload to context.json
        with open('context.json', 'w') as f:
            json.dump(payload, f, indent=2)
        
        # Git commands to commit and push
        commands = [
            ['git', 'add', 'context.json'],
            ['git', 'commit', '-m', f'Update context.json - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'],
            ['git', 'push', '-u', 'origin', 'master']
        ]
        
        # Execute git commands
        for cmd in commands:
            success, output = run_git_command(cmd)
            if not success:
                print(f"Error executing {' '.join(cmd)}")
                print(f"Error output: {output}")
                return False
            print(f"Successfully executed: {' '.join(cmd)}")
        
        print("Successfully updated and pushed context.json")
        return True
        
    except Exception as e:
        print(f"Error updating context.json: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    test_payload = {
        "weather": "Cloudy with a chance of meatballs",
        "news": "Elon Musk launches a flamethrower into space."
    }
    update_context_json(test_payload)
