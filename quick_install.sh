#!/bin/bash

# Pi-5 Relay Controller Quick Install
# ===================================
# One-command installation for GitHub users

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "🚀 Pi-5 Relay Controller Quick Install"
echo "======================================"

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    print_error "This installer is for Raspberry Pi only!"
    exit 1
fi

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "Please run as regular user (not root)"
    exit 1
fi

# Run system check
print_status "Running system compatibility check..."
if python3 check_system.py; then
    print_success "System check passed!"
else
    print_error "System check failed. Please review the issues above."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run main installer
print_status "Starting main installation..."
if ./install.sh; then
    print_success "Installation completed successfully!"
    
    # Get IP address
    IP_ADDRESS=$(hostname -I | awk '{print $1}')
    
    echo ""
    echo "🎉 Pi-5 Relay Controller is ready!"
    echo "================================="
    echo ""
    echo "📱 Access your controller at:"
    echo "   http://localhost:5000"
    echo "   http://$IP_ADDRESS:5000"
    echo ""
    echo "🔐 Default credentials:"
    echo "   Username: admin"
    echo "   Password: relay123"
    echo ""
    echo "🔧 Quick commands:"
    echo "   ./manage_relay_service.sh status"
    echo "   ./manage_relay_service.sh test"
    echo ""
    print_warning "Remember to change the default password!"
    echo ""
    print_success "Happy controlling! 🎛️"
    
else
    print_error "Installation failed!"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "1. Check the error messages above"
    echo "2. Run: python3 check_system.py"
    echo "3. Try manual installation steps"
    echo "4. Check GitHub issues for help"
    exit 1
fi
