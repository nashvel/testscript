# Git Commit Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python utility with both CLI and GUI interfaces for generating multiple Git commits programmatically. This tool is useful for testing Git workflows, demonstrating version control concepts, or populating a new repository with commit history.

![Git Commit Generator GUI](screenshot.png)

## GitHub Repository

```bash
git clone https://github.com/nashvel/testscript.git
cd testscript
```

## Features

### GUI Version
- Modern, user-friendly interface with dark theme
- Real-time progress tracking with visual feedback
- Interactive log display with detailed status updates
- Automatic credential saving for convenience
- Easy repository selection and initialization
- Support for both local and remote repositories
- Cross-platform compatibility (Windows, macOS, Linux)

## Prerequisites

- Python 3.6 or higher
- Git installed and configured on your system
- (Optional) GitHub account for pushing commits

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nashvel/testscript.git
   cd testscript
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Getting a GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Give your token a descriptive name (e.g., "Commit Generator")
4. Select these scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Important**: Copy the token immediately - you won't be able to see it again!

## Usage

### GUI Version (Recommended)

```bash
# Run the GUI application
python3 git_commit_gui.py
```

#### Step-by-Step Guide:

1. **Select Repository Directory**
   - Click "Browse" and select your local Git repository
   - Or enter the path manually
   - If the directory isn't a Git repository, one will be initialized

2. **GitHub Integration (Optional)**
   - Enter your GitHub repository URL (e.g., `https://github.com/username/repo.git`)
   - Enter your GitHub username
   - Paste your GitHub personal access token

3. **Configure Commits**
   - Use the dropdown to select the number of commits to generate (1-100)
   - Each commit will have a unique timestamp and message

4. **Generate Commits**
   - Click "Start" to begin generating commits
   - Monitor progress in the log area
   - The progress bar shows overall completion
   - Detailed status messages appear below the progress bar

5. **Pushing to GitHub**
   - If GitHub URL is provided, commits will be automatically pushed
   - The app will verify your access and create the repository if needed
   - You'll be prompted before creating a new repository
### Command Line Version

For advanced users, a command-line version is available:

```bash
python3 mass_commits.py --repo /path/to/repo --count 10 --github-url https://github.com/username/repo.git
```

### GUI Features

1. **Automatic Credential Saving**
   - Your GitHub credentials are saved automatically (securely in your home directory)
   - No need to re-enter your token and username each time

2. **Repository Management**
   - Initialize new Git repositories with one click
   - Connect to existing repositories easily
   - Automatic remote repository configuration

3. **Progress Tracking**
   - Real-time progress bar
   - Detailed log of all operations
   - Clear status messages

4. **User Experience**
   - Clean, modern interface
   - Responsive design
   - Error handling with helpful messages

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   - Ensure your GitHub token has the `repo` scope
   - Verify you have write access to the repository

2. **Repository Not Found**
   - Check the repository URL is correct
   - Ensure the repository exists and is not private (unless using a token with private repo access)

3. **Authentication Failures**
   - Generate a new token if the current one is expired
   - Make sure to copy the entire token correctly

4. **Push Rejected**
   - Try enabling the "Force Push" option if you're working with an existing repository
   - Make sure you have the latest changes before pushing

## Security Notes

- Your GitHub token is only used during the push operation and is not stored
- For better security, consider using SSH authentication
- Never commit your token to version control

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

💡 **Tip**: For best results, use this tool responsibly and in accordance with GitHub's Terms of Service.

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

## Contributors

- [nacht](https://github.com/nacht) - Main contributor

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

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.facebook.com/github.nashvel)

Or via [PayPal](https://paypal.me/LotisQuiblat?country.x=PH&locale.x=en_US)

## Author

**Nacht**  
Email: [nash.backup21@gmail.com](mailto:nash.backup21@gmail.com)  
GitHub: [@nashvel](https://github.com/nashvel)

---

*This tool is intended for educational and testing purposes only. Use responsibly in development environments.*
