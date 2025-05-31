import sys
import os
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit,
                           QFileDialog, QMessageBox, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

class CommitWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, num_commits, repo_path, github_url=None):
        super().__init__()
        self.num_commits = num_commits
        self.repo_path = repo_path
        self.github_url = github_url
        self.running = True

    def run(self):
        try:
            os.chdir(self.repo_path)
            
            # Initialize repository if needed
            if not os.path.exists('.git'):
                self.status.emit("Initializing Git repository...")
                self._run_command('git init')
                with open('commit_log.txt', 'w') as f:
                    f.write('Initial commit\n')
                self._run_command('git add .')
                self._run_command('git commit -m "Initial commit"')
            
            # Set up remote if provided
            if self.github_url:
                self.status.emit("Configuring remote repository...")
                remote = self._run_command('git remote -v')
                if not remote or 'origin' not in remote:
                    self._run_command(f'git remote add origin {self.github_url}')
            
            # Create commits
            self.status.emit("Creating commits...")
            for i in range(1, self.num_commits + 1):
                if not self.running:
                    break
                    
                with open('commit_log.txt', 'a') as f:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"Commit {i} at {timestamp}\n")
                
                self._run_command('git add .')
                self._run_command(f'git commit -m "Commit {i}: Made at {timestamp}"')
                
                self.progress.emit(int((i / self.num_commits) * 100))
                self.status.emit(f"Created commit {i}/{self.num_commits}")
            
            # Push to GitHub if URL provided
            if self.github_url and self.running:
                self.status.emit("Pushing to GitHub...")
                branch = self._run_command('git branch --show-current')
                if branch:
                    self._run_command(f'git push -u origin {branch}')
                    self.status.emit("Successfully pushed to GitHub!")
            
            if self.running:
                self.finished.emit(True, "Operation completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def _run_command(self, command):
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.status.emit(f"Error: {e.stderr}")
            raise
    
    def stop(self):
        self.running = False

class GitCommitGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Git Commit Generator")
        self.setMinimumSize(600, 500)
        
        # Set window icon if available
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Repository settings group
        repo_group = QGroupBox("Repository Settings")
        repo_layout = QVBoxLayout()
        
        # Repository path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Repository Path:"))
        self.path_edit = QLineEdit(os.getcwd())
        self.path_edit.setPlaceholderText("Select repository directory...")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(browse_btn)
        
        # GitHub URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("GitHub URL (optional):"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://github.com/username/repo.git")
        url_layout.addWidget(self.url_edit, 1)
        
        # Add to repo group
        repo_layout.addLayout(path_layout)
        repo_layout.addLayout(url_layout)
        repo_group.setLayout(repo_layout)
        
        # Commit settings group
        commit_group = QGroupBox("Commit Settings")
        commit_layout = QVBoxLayout()
        
        # Number of commits
        num_layout = QHBoxLayout()
        num_layout.addWidget(QLabel("Number of Commits:"))
        self.num_commits = QComboBox()
        self.num_commits.addItems(["10", "50", "100", "200", "500"])
        self.num_commits.setCurrentText("100")
        num_layout.addWidget(self.num_commits)
        num_layout.addStretch()
        
        commit_layout.addLayout(num_layout)
        commit_group.setLayout(commit_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)
        
        # Log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Operation log will appear here...")
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_operation)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_operation)
        self.stop_btn.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        
        # Add all to main layout
        layout.addWidget(repo_group)
        layout.addWidget(commit_group)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_area, 1)
        layout.addLayout(button_layout)
        
        # Apply style
        self.apply_style()
    
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QPushButton#stopButton {
                background-color: #f44336;
            }
            QPushButton#stopButton:hover {
                background-color: #d32f2f;
            }
            QTextEdit, QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        self.stop_btn.setObjectName("stopButton")
    
    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Repository Directory")
        if dir_path:
            self.path_edit.setText(dir_path)
    
    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        self.status_label.setText(message)
        self.log_message(message)
    
    def start_operation(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_area.clear()
        
        repo_path = self.path_edit.text()
        if not os.path.isdir(repo_path):
            QMessageBox.critical(self, "Error", "Please select a valid directory")
            self.reset_ui()
            return
        
        try:
            num_commits = int(self.num_commits.currentText())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number of commits")
            self.reset_ui()
            return
        
        github_url = self.url_edit.text().strip() or None
        
        self.worker = CommitWorker(num_commits, repo_path, github_url)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.operation_finished)
        
        self.log_message(f"Starting to create {num_commits} commits...")
        self.worker.start()
    
    def stop_operation(self):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, 'Stop Operation',
                'Are you sure you want to stop the current operation?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                self.worker.wait()
                self.log_message("Operation stopped by user")
                self.reset_ui()
    
    def operation_finished(self, success, message):
        self.log_message(message)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        self.reset_ui()
    
    def reset_ui(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitCommitGenerator()
    window.show()
    sys.exit(app.exec())
