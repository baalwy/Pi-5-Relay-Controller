#!/bin/bash

# Pi-5 Relay Controller Installation Script
# This script installs and configures the relay controller as a system service

set -e

echo "🚀 Pi-5 Relay Controller Installation"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    print_error "This script is designed for Raspberry Pi only!"
    exit 1
fi

# Check if running as root for service installation
if [[ $EUID -eq 0 ]]; then
    print_error "Please run this script as a regular user (not root)"
    print_status "The script will ask for sudo password when needed"
    exit 1
fi

print_status "Checking system requirements..."

# Update system packages
print_status "Updating system packages..."
sudo apt update

# Install required system packages
print_status "Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    build-essential \
    git \
    curl \
    wget \
    libgpiod2 \
    libgpiod-dev \
    gpiod \
    python3-libgpiod \
    nginx-light \
    supervisor

# Add user to gpio group
print_status "Adding user to gpio group..."
sudo usermod -a -G gpio $USER

# Create virtual environment (recommended)
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install requirements with error handling
if pip install -r requirements.txt; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    print_status "Trying alternative installation method..."

    # Try installing gpiod from system packages if pip fails
    sudo apt install -y python3-libgpiod

    # Install other requirements without gpiod
    pip install Flask Flask-Bootstrap Werkzeug gunicorn click itsdangerous Jinja2 MarkupSafe

    print_warning "Some packages installed via system package manager"
fi

deactivate

# Make scripts executable
print_status "Setting up executable permissions..."
chmod +x manage_relay_service.sh
chmod +x reset_gpio.py

# Install systemd service
print_status "Installing systemd service..."
sudo cp relay-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable relay-controller.service

# Create state file directory
print_status "Setting up state persistence..."
touch relay_states.json
chmod 666 relay_states.json

# Test GPIO access
print_status "Testing GPIO access..."
python3 -c "import gpiod; print('GPIO access: OK')" || {
    print_warning "GPIO access test failed. You may need to reboot for group changes to take effect."
}

# Start the service
print_status "Starting relay controller service..."
sudo systemctl start relay-controller.service

# Check service status
if sudo systemctl is-active --quiet relay-controller.service; then
    print_success "Service started successfully!"
else
    print_error "Service failed to start. Check logs with: sudo journalctl -u relay-controller.service"
    exit 1
fi

# Get IP address
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo ""
echo "🎉 Installation completed successfully!"
echo "====================================="
echo ""
echo "📱 Access your relay controller at:"
echo "   http://localhost:5000"
echo "   http://$IP_ADDRESS:5000"
echo ""
echo "🔐 Default login credentials:"
echo "   Username: admin"
echo "   Password: relay123"
echo ""
echo "🔧 Management commands:"
echo "   ./manage_relay_service.sh status    # Check service status"
echo "   ./manage_relay_service.sh restart   # Restart service"
echo "   ./manage_relay_service.sh logs      # View logs"
echo "   ./manage_relay_service.sh test      # Test system"
echo ""
echo "📚 For debugging, open debug_relay.html in your browser"
echo ""
print_warning "IMPORTANT: Change the default password after first login!"
print_warning "If GPIO access fails, reboot your Raspberry Pi and try again."
echo ""
print_success "Happy controlling! 🎛️"
