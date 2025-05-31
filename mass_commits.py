import os
import datetime

def setup_git_repo():
    # Initialize git repository if not already one
    if not os.path.exists('.git'):
        os.system('git init')
        # Create initial commit if this is a new repo
        with open('commit_log.txt', 'w') as f:
            f.write('Initial commit\n')
        os.system('git add .')
        os.system('git commit -m "Initial commit"')

def make_commits():
    setup_git_repo()
    
    for i in range(1, 101):
        # Append current timestamp and commit number to file
        with open('commit_log.txt', 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Commit {i} at {timestamp}\n")
        
        # Stage and commit the changes
        os.system('git add .')
        os.system(f'git commit -m "Commit {i}: Made at {timestamp}"')
        
        print(f"Created commit {i}/100")

if __name__ == "__main__":
    print("Starting to create 100 commits...")
    make_commits()
    print("\nAll 100 commits have been created!")
