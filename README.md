# 🔌 Pi-5 Relay Controller

<div align="center">

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

**A modern, secure, and beautiful web-based relay controller for Raspberry Pi 5**

[🚀 Features](#-features) • [📦 Installation](#-installation) • [🎯 Usage](#-usage) • [📚 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Overview

Pi-5 Relay Controller is a comprehensive web-based solution for controlling 16-channel relay modules using Raspberry Pi 5. Built with modern web technologies and featuring a beautiful Arabic-supported interface, this project offers enterprise-grade reliability with home-lab simplicity.

### ✨ What Makes This Special?

- 🎨 **Modern UI/UX**: Beautiful, responsive design with smooth animations
- 🔐 **Security First**: Password-protected access with session management
- 💾 **State Persistence**: Automatically saves and restores relay states after reboot
- 🌐 **Multi-language**: Full Arabic and English support
- ⚡ **Real-time Updates**: Live status indicators with instant feedback
- 🔧 **Production Ready**: Systemd service with auto-start capabilities

---

## 🚀 Features

### 🎛️ **Relay Control**
- **16-Channel Support**: Control up to 16 relays simultaneously
- **Individual Control**: Turn ON/OFF, Toggle, or Check status of each relay
- **Bulk Operations**: Control all relays at once
- **Real-time Feedback**: Instant visual status updates

### 🔒 **Security & Authentication**
- **Login Protection**: Secure password-based authentication
- **Session Management**: Automatic session handling with Flask
- **Access Control**: All endpoints protected from unauthorized access

### 💾 **Smart State Management**
- **Auto-Save**: Automatically saves relay states on every change
- **Auto-Restore**: Restores previous states after system reboot
- **GPIO Sync**: Synchronizes with actual GPIO pin states

### 🎨 **Modern Interface**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Beautiful Animations**: Smooth transitions and hover effects
- **Arabic Support**: Full RTL support with Cairo font
- **Dark/Light Themes**: Gradient backgrounds with glassmorphism effects

### 🔧 **System Integration**
- **Systemd Service**: Runs as a system service with auto-start
- **GPIO Management**: Uses modern gpiod library for Raspberry Pi 5
- **Error Handling**: Comprehensive error handling and logging
- **Debug Tools**: Built-in debugging interface

---

## 📦 Installation

### Prerequisites

- Raspberry Pi 5 with Raspberry Pi OS
- Python 3.9 or higher
- 16-channel relay module
- Internet connection for initial setup

### 🚀 Quick Start (Recommended)

**One-command installation:**
```bash
git clone https://github.com/yourusername/Pi-5-Relay-Controller.git
cd Pi-5-Relay-Controller
chmod +x quick_install.sh && ./quick_install.sh
```

### 📋 Manual Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Pi-5-Relay-Controller.git
cd Pi-5-Relay-Controller
```

2. **Check system compatibility**
```bash
python3 check_system.py
```

3. **Run installation script**
```bash
chmod +x install.sh && ./install.sh
```

4. **Access the web interface**
```
http://your-pi-ip:5000
```

### 🐳 Docker Installation (Advanced)

```bash
# Clone repository
git clone https://github.com/yourusername/Pi-5-Relay-Controller.git
cd Pi-5-Relay-Controller

# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t pi5-relay-controller .
docker run -d -p 5000:5000 --device /dev/gpiochip0 --privileged pi5-relay-controller
```

**Default Login:**
- Username: `admin`
- Password: `relay123`

---

## 🎯 Usage

### Web Interface

1. **Login**: Navigate to the web interface and login with your credentials
2. **Control Relays**: Use the beautiful card-based interface to control individual relays
3. **Monitor Status**: Real-time status indicators show current relay states
4. **Bulk Operations**: Use the control panel for all-relay operations

### API Endpoints

The system provides RESTful API endpoints for automation:

```bash
# Turn relay ON
GET /on/<relay_number>

# Turn relay OFF  
GET /off/<relay_number>

# Toggle relay
GET /toggle/<relay_number>

# Get relay status
GET /status/<relay_number>

# Control all relays
GET /all_on/
GET /all_off/
```

### Command Line Management

```bash
# Check service status
./manage_relay_service.sh status

# Restart service
./manage_relay_service.sh restart

# View logs
./manage_relay_service.sh logs

# Test system
./manage_relay_service.sh test
```

---

## 🔧 Configuration

### GPIO Pin Mapping

Default GPIO pins for 16 relays:
```
[10, 12, 13, 14, 15, 6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
```

### Changing Default Password

Edit `server.py` and update:
```python
PASSWORD_HASH = hashlib.sha256('your_new_password'.encode()).hexdigest()
```

### Customizing Relay Names

Edit `channels.json` to customize relay names and visibility.

---

## 📚 Documentation

### 📖 Complete Guides
- **[📖 User Guide](USER_GUIDE.md)** - Comprehensive user manual with step-by-step instructions
- **[🛠️ Installation Guide](INSTALLATION_GUIDE.md)** - Detailed installation with hardware setup
- **[🔗 API Guide](API_GUIDE.md)** - Complete API documentation with examples
- **[🔧 Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[📁 Project Structure](PROJECT_STRUCTURE.md)** - Detailed file organization

### 🚀 Quick Links
- **Hardware Setup**: See [Installation Guide](INSTALLATION_GUIDE.md#-الخطوة-1-توصيل-الأجهزة)
- **Software Installation**: Run `./quick_install.sh`
- **API Usage**: Check [API Guide](API_GUIDE.md) for programming examples
- **Troubleshooting**: Visit [Troubleshooting Guide](TROUBLESHOOTING.md)

### 📱 Platform Support
- **Web Interface**: Works on all modern browsers
- **Mobile Apps**: Responsive design for phones and tablets
- **API Integration**: Support for Python, JavaScript, PHP, Bash, and more
- **Home Automation**: Compatible with most IoT platforms

---

## 📸 Screenshots

### Login Interface
Beautiful, secure login with modern design

### Main Dashboard
Responsive card-based interface with real-time status

### Mobile View
Fully responsive design works on all devices

---

## 🛠️ Technical Details

### Architecture
- **Backend**: Python Flask with modern routing
- **Frontend**: Bootstrap 5 with custom CSS3 animations
- **GPIO Control**: gpiod library for Raspberry Pi 5 compatibility
- **State Management**: JSON-based persistence
- **Security**: SHA256 password hashing with Flask sessions

### File Structure
```
Pi-5-Relay-Controller/
├── 📄 server.py              # Main Flask application
├── 📄 relay_lib.py           # GPIO control library
├── 📄 channels.json          # Relay configuration
├── 📄 requirements.txt       # Python dependencies
├── 📄 install.sh            # Installation script
├── 📄 quick_install.sh      # One-command installation
├── 📄 check_system.py       # System compatibility check
├── 📁 templates/            # HTML templates
├── 📁 static/               # CSS and JavaScript
├── 📁 screenshots/          # Project screenshots
└── 📄 TROUBLESHOOTING.md    # Problem solving guide
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed file descriptions.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Raspberry Pi Foundation for the amazing hardware
- Flask community for the excellent web framework
- Bootstrap team for the responsive framework
- All contributors and users of this project

---

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/Pi-5-Relay-Controller/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/Pi-5-Relay-Controller/discussions)
- 📧 **Email**: your.email@example.com

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

Made with ❤️ for the Raspberry Pi community

</div>
