# Git Commit Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python utility with both CLI and GUI interfaces for generating multiple Git commits programmatically. This tool is useful for testing Git workflows, demonstrating version control concepts, or populating a new repository with commit history.

![Git Commit Generator GUI](screenshot.png) *Screenshot of the Git Commit Generator GUI*

## Features

### GUI Version
- Modern, user-friendly interface
- Real-time progress tracking
- Interactive log display
- Dark theme with smooth animations
- Easy repository selection
- Optional GitHub remote configuration

### CLI Version
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

### GUI Version

Run the GUI application:

```bash
./run_gui.sh
# Or directly with Python:
python3 git_commit_gui.py
```

1. Select your repository directory
2. (Optional) Enter your GitHub repository URL
3. Choose the number of commits to generate
4. Click "Start" to begin
5. Monitor progress in the log area

### CLI Version

Run the command-line version:

```bash
python3 mass_commit.py
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

## Screenshots

### Main Interface
![Main Interface](screenshot1.png)

### Progress Tracking
![Progress Tracking](screenshot2.png)

### Success Message
![Success Message](screenshot3.png)

## Example Output (CLI)

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

### Development Setup

1. Fork the repository
2. Create a new branch for your feature
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes and submit a pull request

## Support

If you find this tool useful, consider supporting its development:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/yourusername)

Or via [PayPal](https://paypal.me/yourusername)

## Author

[Your Name] - [Your Email]

---

*This tool is intended for educational and testing purposes only. Use responsibly in development environments.*
