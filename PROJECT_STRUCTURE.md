# 📁 Project Structure

```
Pi-5-Relay-Controller/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 TROUBLESHOOTING.md           # Problem solving guide
├── 📄 .gitignore                   # Git ignore rules
│
├── 🚀 Installation & Setup
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 requirements-dev.txt     # Development dependencies
│   ├── 📄 install.sh              # Main installation script
│   ├── 📄 quick_install.sh        # One-command installation
│   ├── 📄 check_system.py         # System compatibility check
│   └── 📄 relay-controller.service # Systemd service file
│
├── 🐳 Docker Support
│   ├── 📄 Dockerfile              # Docker image definition
│   └── 📄 docker-compose.yml      # Docker Compose configuration
│
├── 🔧 Core Application
│   ├── 📄 server.py               # Main Flask web server
│   ├── 📄 relay_lib.py            # GPIO relay control library
│   ├── 📄 channels.json           # Relay configuration
│   └── 📄 reset_gpio.py           # GPIO reset utility
│
├── 🌐 Web Interface
│   ├── 📁 templates/              # HTML templates
│   │   ├── 📄 index.html          # Main dashboard
│   │   └── 📄 login.html          # Login page
│   └── 📁 static/                 # Static web assets
│       ├── 📁 css/                # Stylesheets
│       │   └── 📄 sticky-footer-navbar.css
│       └── 📁 js/                 # JavaScript files
│           └── 📄 index.js        # Main application logic
│
├── 🛠️ Management & Debug
│   ├── 📄 manage_relay_service.sh # Service management script
│   └── 📄 debug_relay.html       # Debug interface
│
└── 📸 Documentation
    └── 📁 screenshots/            # Project screenshots
        └── 📄 README.md           # Screenshot guidelines
```

## 📋 File Descriptions

### 🚀 Installation Files
- **requirements.txt**: Production Python dependencies
- **requirements-dev.txt**: Development and testing dependencies
- **install.sh**: Comprehensive installation with error handling
- **quick_install.sh**: One-command installation for users
- **check_system.py**: Pre-installation system compatibility check

### 🔧 Core Application
- **server.py**: Flask web server with authentication and API endpoints
- **relay_lib.py**: Hardware abstraction layer for GPIO control
- **channels.json**: Relay configuration (names, visibility, etc.)
- **reset_gpio.py**: Utility to reset GPIO pins if stuck

### 🌐 Web Interface
- **templates/**: Jinja2 HTML templates with modern design
- **static/**: CSS and JavaScript for responsive interface
- **index.html**: Main dashboard with relay controls
- **login.html**: Secure authentication page

### 🛠️ Management Tools
- **manage_relay_service.sh**: Service start/stop/status/logs
- **debug_relay.html**: Standalone debugging interface
- **relay-controller.service**: Systemd service configuration

### 📚 Documentation
- **README.md**: Comprehensive project documentation
- **CHANGELOG.md**: Version history and feature additions
- **CONTRIBUTING.md**: Guidelines for contributors
- **TROUBLESHOOTING.md**: Common issues and solutions

### 🐳 Containerization
- **Dockerfile**: Container image for advanced deployments
- **docker-compose.yml**: Multi-container orchestration

## 🎯 Design Principles

### 📦 Modular Architecture
- Separated concerns (web, GPIO, configuration)
- Reusable components
- Easy to extend and modify

### 🔒 Security First
- Authentication on all endpoints
- Secure session management
- Input validation and sanitization

### 🌍 User Experience
- Responsive design for all devices
- Arabic and English support
- Intuitive interface with visual feedback

### 🛠️ Maintainability
- Clean, documented code
- Comprehensive error handling
- Extensive logging and debugging tools

### 🚀 Production Ready
- Systemd service integration
- State persistence
- Automatic recovery mechanisms

This structure ensures the project is professional, maintainable, and easy to understand for contributors and users alike.
