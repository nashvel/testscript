import sys
import os
import datetime
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QScrollArea,
                           QFileDialog, QMessageBox, QGroupBox, QComboBox, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QIcon, QFont, QPixmap, QPainter, QPainterPath, QDesktopServices, QColor

class CommitWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, num_commits, repo_path, github_url=None, parent=None):
        super().__init__()
        self.num_commits = num_commits
        self.repo_path = repo_path
        self.github_url = github_url
        self.parent_widget = parent
        self.running = True

    def run(self):
        try:
            os.chdir(self.repo_path)
            
            if not os.path.exists('.git'):
                self.status.emit("Initializing Git repository...")
                self._run_command('git init')
                with open('commit_log.txt', 'w') as f:
                    f.write('Initial commit\n')
                self._run_command('git add .')
                self._run_command('git commit -m "Initial commit"')
            
            if self.github_url:
                self.status.emit("Configuring remote repository...")
                remote = self._run_command('git remote -v')
                if not remote or 'origin' not in remote:
                    self._run_command(f'git remote add origin {self.github_url}')
            
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
            
            if self.github_url and self.running:
                self.status.emit("Pushing to GitHub...")
                branch = self._run_command('git branch --show-current')
                if branch:
                    # Get GitHub username and token from the main thread
                    github_user = self.parent().github_user_edit.text().strip()
                    github_token = self.parent().github_token_edit.text().strip()
                    
                    if github_user and github_token:
                        # Update remote URL with authentication
                        repo_url = self.github_url.replace('https://', f'https://{github_user}:{github_token}@')
                        self._run_command(f'git remote set-url origin {repo_url}')
                        
                        # Push with authentication
                        self._run_command(f'git push -u origin {branch}')
                        self.status.emit("Successfully pushed to GitHub!")
                    else:
                        self.status.emit("GitHub username and token are required for pushing")
            
            if self.running:
                self.finished.emit(True, "Operation completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def _run_command(self, command, env_vars=None):
        import subprocess
        try:
            # Prepare environment
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)
                
            # Run command with environment variables
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=True,
                env=env
            )
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
    
    def create_round_avatar(self, image_path, size=80):
        """Create a circular avatar from an image"""
        pixmap = QPixmap(image_path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                          Qt.TransformationMode.SmoothTransformation)
        
        rounded = QPixmap(size, size)
        rounded.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw circle mask
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        
        # Draw the image
        x = (size - pixmap.width()) // 2
        y = (size - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        
        # Draw border
        pen = painter.pen()
        pen.setWidth(3)
        pen.setColor(Qt.GlobalColor.white)
        painter.setPen(pen)
        painter.drawEllipse(0, 0, size, size)
        
        painter.end()
        return rounded

    def init_ui(self):
        self.setWindowTitle("Git Commit Generator")
        self.setMinimumSize(800, 650)
        
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass
            
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            QFrame#contentFrame {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QFrame#contentFrame:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 50))
        content_frame.setGraphicsEffect(shadow)
        
        # Create content layout
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Add content frame to main layout
        main_layout.addWidget(content_frame)
        
        # Store content layout for later use
        self.content_layout = content_layout
        
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
        
        # GitHub URL and Auth
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("GitHub URL (optional):"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://github.com/username/repo.git")
        url_layout.addWidget(self.url_edit, 1)
        
        # GitHub Auth
        auth_layout = QHBoxLayout()
        auth_layout.addWidget(QLabel("GitHub Username:"))
        self.github_user_edit = QLineEdit()
        self.github_user_edit.setPlaceholderText("your_username")
        auth_layout.addWidget(self.github_user_edit)
        
        auth_layout.addWidget(QLabel("Personal Access Token:"))
        self.github_token_edit = QLineEdit()
        self.github_token_edit.setPlaceholderText("ghp_...")
        self.github_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        auth_layout.addWidget(self.github_token_edit)
        
        # Add to repo group
        repo_layout.addLayout(path_layout)
        repo_layout.addLayout(url_layout)
        repo_layout.addLayout(auth_layout)
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
        
        # Add widgets directly to content layout
        self.content_layout.addWidget(repo_group)
        self.content_layout.addWidget(commit_group)
        self.content_layout.addWidget(QLabel("Progress:"))
        self.content_layout.addWidget(self.progress_bar)
        self.content_layout.addWidget(QLabel("Status:"))
        self.content_layout.addWidget(self.status_label)
        self.content_layout.addWidget(QLabel("Log:"))
        self.content_layout.addWidget(self.log_area, 1)
        
        # Add button layout
        button_container = QWidget()
        button_container.setLayout(button_layout)
        self.content_layout.addWidget(button_container)
        
        # Add coffee button to show donation section
        self.coffee_btn = QPushButton()
        self.coffee_btn.setIcon(QIcon.fromTheme("emblem-favorite", QIcon("image/coffee.png")))
        self.coffee_btn.setIconSize(QSize(24, 24))
        self.coffee_btn.setToolTip("Support this project")
        self.coffee_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 10px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # Create donation section (initially hidden)
        self.donation_frame = QFrame()
        self.donation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.donation_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #dee2e6;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#subtitle {
                color: #6c757d;
                font-size: 13px;
            }
        """)
        
        # Initially hide the donation frame
        self.donation_frame.setVisible(False)
        
        donation_layout = QHBoxLayout(self.donation_frame)
        
        # Add avatar
        avatar_label = QLabel()
        try:
            avatar = self.create_round_avatar("image/images.jpeg")
            avatar_label.setPixmap(avatar)
        except Exception as e:
            print(f"Could not load avatar: {e}")
        
        # Add text and button
        text_layout = QVBoxLayout()
        title_label = QLabel("Support My Work")
        title_label.setObjectName("title")
        
        subtitle_label = QLabel("If you find this tool useful, consider buying me a coffee!")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setWordWrap(True)
        
        # PayPal button
        paypal_btn = QPushButton("Donate with PayPal")
        paypal_btn.setIcon(QIcon.fromTheme("emblem-money", QIcon("image/paypal.png")))
        paypal_btn.setIconSize(QSize(20, 20))
        paypal_btn.setStyleSheet("""
            QPushButton {
                background-color: #0070ba;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005ea6;
            }
        """)
        paypal_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://paypal.me/LotisQuiblat?country.x=PH&locale.x=en_US")))
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)
        text_layout.addWidget(paypal_btn, 0, Qt.AlignmentFlag.AlignLeft)
        
        donation_layout.addWidget(avatar_label)
        donation_layout.addSpacing(15)
        donation_layout.addLayout(text_layout, 1)
        
        # Add coffee button and donation frame to main layout
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(self.coffee_btn)
        
        # Add to content layout
        self.content_layout.addWidget(button_container)
        self.content_layout.addWidget(self.donation_frame)
        
        # Connect coffee button to toggle donation section
        self.coffee_btn.clicked.connect(self.toggle_donation_section)
        
        # Apply style
        self.apply_style()
    
    def resizeEvent(self, event):
        # Update background if needed
        super().resizeEvent(event)
    
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #6a11cb;
                background-image: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #6a11cb, stop: 1 #2575fc
                );
            }
            QWidget {
                color: #ffffff;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                margin-top: 15px;
                padding: 15px 10px 10px 10px;
                font-weight: bold;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                min-width: 100px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.3);
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
            QPushButton#donateButton {
                background-color: #ffc439;
                color: #253b80;
                font-weight: bold;
                border-radius: 20px;
                padding: 8px 20px;
            }
            QPushButton#donateButton:hover {
                background-color: #f2bb35;
            }
            QTextEdit, QLineEdit, QComboBox {
                padding: 8px 12px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                selection-background-color: #6a11cb;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                text-align: center;
                height: 20px;
                color: white;
                background: rgba(0, 0, 0, 0.2);
            }
            QProgressBar::chunk {
                background-color: #6a11cb;
                background-image: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #6a11cb, stop: 1 #2575fc
                );
                border-radius: 2px;
            }
            
            /* Success message box */
            QMessageBox {
                background-color: #2a2a4a;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background: #6a11cb;
                color: white;
                border: 1px solid #8a4bff;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #7d2bff;
            }
            
            /* Dropdown list */
            QComboBox QAbstractItemView {
                background: #2a2a4a;
                color: white;
                selection-background-color: #6a11cb;
                border: 1px solid #444;
                outline: none;
            }
            QComboBox::item:selected {
                background: #6a11cb;
                color: white;
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
        try:
            if self.worker and self.worker.isRunning():
                self.log_message("Operation already in progress")
                return
                
            repo_path = self.path_edit.text().strip()
            if not repo_path:
                self.log_message("Please select a repository directory")
                return
                
            github_url = self.url_edit.text().strip() or None
            
            # Get number of commits
            try:
                num_commits = int(self.num_commits.currentText())
                if num_commits <= 0:
                    raise ValueError("Number of commits must be positive")
            except (ValueError, AttributeError) as e:
                self.log_message(f"Invalid number of commits: {str(e)}")
                return
                
            if not os.path.isdir(repo_path):
                self.log_message(f"Directory does not exist: {repo_path}")
                return
                
            # Check if GitHub URL is provided and auth is complete
            if github_url:
                github_user = self.github_user_edit.text().strip()
                github_token = self.github_token_edit.text().strip()
                if not github_user or not github_token:
                    self.log_message("GitHub username and token are required when providing a GitHub URL")
                    return
                # Update URL with credentials
                github_url = github_url.replace('https://', f'https://{github_user}:{github_token}@')
                    
            # Disable UI elements during operation
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.progress_bar.setValue(0)
            self.log_area.clear()
            
            self.log_message(f"Starting to create {num_commits} commits in {repo_path}")
            if github_url:
                self.log_message(f"Will push to: {github_url.split('@')[-1]}")
            
            self.worker = CommitWorker(num_commits, repo_path, github_url, self)
            self.worker.progress.connect(self.update_progress)
            self.worker.status.connect(self.update_status)
            self.worker.finished.connect(self.operation_finished)
            
            self.worker.start()
            
        except Exception as e:
            self.log_message(f"Error starting operation: {str(e)}")
            import traceback
            traceback.print_exc()
            self.reset_ui()
    
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
    
    def toggle_donation_section(self):
        """Toggle the visibility of the donation section"""
        self.donation_frame.setVisible(not self.donation_frame.isVisible())
    
    def reset_ui(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitCommitGenerator()
    window.show()
    sys.exit(app.exec())
