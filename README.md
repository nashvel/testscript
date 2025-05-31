# Git Commit Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python utility for generating multiple Git commits programmatically. This tool is useful for testing Git workflows, demonstrating version control concepts, or populating a new repository with commit history.

## Features

- Creates a configurable number of Git commits
- Automatically initializes a Git repository if needed
- Tracks commit history in a `commit_log.txt` file
- Includes timestamps in commit messages for tracking
- Simple, clean Python implementation

## Prerequisites

- Python 3.6 or higher
- Git installed on your system

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/github-script.git
   cd github-script
   ```

2. No additional Python packages are required beyond the standard library.

## Usage

Run the script with Python:

```bash
python3 mass_commits.py
```

This will:
1. Initialize a Git repository in the current directory (if not already a Git repo)
2. Create 100 commits with sequential messages
3. Generate a `commit_log.txt` file tracking all commits

### Customization

You can modify the script to:
- Change the number of commits by adjusting the range in the `make_commits()` function
- Modify the commit message format by editing the `git commit -m` command
- Change the tracked file name from `commit_log.txt` to any other filename

## Example Output

```
Starting to create 100 commits...
Created commit 1/100
Created commit 2/100
...
Created commit 100/100

All 100 commits have been created!
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

[Your Name] - [Your Email]

---

*This tool is intended for educational and testing purposes only. Use responsibly in development environments.*
