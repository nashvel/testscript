import os
import datetime
import subprocess
from getpass import getpass

def run_command(command, shell=True):
    """Helper function to run shell commands with error handling"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Error: {e.stderr}")
        return None

def setup_git_repo():
    if not os.path.exists('.git'):
        run_command('git init')
        with open('commit_log.txt', 'w') as f:
            f.write('Initial commit\n')
        run_command('git add .')
        run_command('git commit -m "Initial commit"')
    
    remote = run_command('git remote -v')
    if not remote or 'origin' not in remote:
        print("\nNo remote repository configured.")
        repo_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): ").strip()
        if repo_url:
            run_command(f'git remote add origin {repo_url}')

def push_to_github():
    """Push changes to GitHub repository"""
    print("\nPushing changes to GitHub...")
    
    branch = run_command('git branch --show-current')
    if not branch:
        print("Error: Could not determine current branch")
        return False
    
    result = run_command('git push -u origin ' + branch)
    if result is None:
        print("\nPush failed. You might need to authenticate with GitHub.")
        print("Please make sure you have set up GitHub CLI (gh) or SSH keys.")
        return False
    
    print("\nSuccessfully pushed to GitHub!")
    return True

def make_commits():
    setup_git_repo()
    
    for i in range(1, 101):
        with open('commit_log.txt', 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Commit {i} at {timestamp}\n")
        
        run_command('git add .')
        run_command(f'git commit -m "Commit {i}: Made at {timestamp}"')
        
        print(f"Created commit {i}/100")
    
    # After all commits, push to GitHub
    push_to_github()

if __name__ == "__main__":
    print("Starting to create 100 commits...")
    try:
        make_commits()
        print("\nAll 100 commits have been created and pushed to GitHub!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
