# 🔧 Troubleshooting Guide

This guide helps resolve common issues with Pi-5 Relay Controller.

## 🚨 Common Issues

### Installation Problems

#### ❌ "gpiod not found" Error
```bash
# Solution 1: Install system packages
sudo apt update
sudo apt install libgpiod2 libgpiod-dev gpiod python3-libgpiod

# Solution 2: Use system Python package
pip uninstall gpiod
sudo apt install python3-libgpiod
```

#### ❌ "Permission denied" for GPIO
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Reboot to apply changes
sudo reboot

# Check group membership
groups $USER
```

#### ❌ "Port 5000 already in use"
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process (replace PID)
sudo kill -9 <PID>

# Or use different port in server.py
```

#### ❌ Virtual environment issues
```bash
# Remove and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Runtime Problems

#### ❌ Service won't start
```bash
# Check service status
sudo systemctl status relay-controller.service

# View detailed logs
sudo journalctl -u relay-controller.service -f

# Restart service
sudo systemctl restart relay-controller.service
```

#### ❌ GPIO "Device or resource busy"
```bash
# Reset GPIO pins
python3 reset_gpio.py

# Check what's using GPIO
sudo lsof /dev/gpiochip0

# Restart service
sudo systemctl restart relay-controller.service
```

#### ❌ Web interface not loading
```bash
# Check if service is running
./manage_relay_service.sh status

# Test local connection
curl http://localhost:5000

# Check firewall
sudo ufw status
```

#### ❌ Relays not responding
```bash
# Test GPIO directly
gpioinfo gpiochip0

# Check wiring connections
# Verify relay module power
# Test with debug interface
```

### Login Issues

#### ❌ "Invalid username or password"
- Default credentials: `admin` / `relay123`
- Check for typos
- Clear browser cache
- Try incognito/private mode

#### ❌ Session expires quickly
- Check system time: `date`
- Restart service: `sudo systemctl restart relay-controller.service`

## 🔍 Diagnostic Commands

### System Information
```bash
# Check Pi model
cat /proc/cpuinfo | grep "Model"

# Check OS version
cat /etc/os-release

# Check Python version
python3 --version

# Check available GPIO
gpioinfo
```

### Service Diagnostics
```bash
# Service status
sudo systemctl status relay-controller.service

# Service logs
sudo journalctl -u relay-controller.service --no-pager

# Test system
./manage_relay_service.sh test

# Check system requirements
python3 check_system.py
```

### Network Diagnostics
```bash
# Check listening ports
sudo netstat -tlnp | grep :5000

# Test local access
curl -I http://localhost:5000

# Check IP address
hostname -I
```

### GPIO Diagnostics
```bash
# List GPIO chips
gpiodetect

# Show GPIO info
gpioinfo gpiochip0

# Test GPIO pin (example: pin 10)
gpioset gpiochip0 10=1
gpioget gpiochip0 10
```

## 🛠️ Advanced Troubleshooting

### Enable Debug Mode
Edit `server.py` and change:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Manual Testing
```bash
# Test individual components
python3 -c "import flask; print('Flask OK')"
python3 -c "import gpiod; print('GPIO OK')"
python3 -c "from relay_lib import *; print('Relay lib OK')"

# Test web server manually
python3 server.py
```

### Reset Everything
```bash
# Stop service
sudo systemctl stop relay-controller.service

# Reset GPIO
python3 reset_gpio.py

# Clear state file
rm -f relay_states.json

# Restart service
sudo systemctl start relay-controller.service
```

### Reinstall from Scratch
```bash
# Remove service
sudo systemctl stop relay-controller.service
sudo systemctl disable relay-controller.service
sudo rm /etc/systemd/system/relay-controller.service

# Clean up
rm -rf venv
rm -f relay_states.json

# Reinstall
./quick_install.sh
```

## 📞 Getting Help

### Before Asking for Help
1. Run system check: `python3 check_system.py`
2. Check service logs: `sudo journalctl -u relay-controller.service`
3. Test with debug interface: Open `debug_relay.html`
4. Try the solutions above

### Information to Include
- Raspberry Pi model and OS version
- Error messages (exact text)
- Output of `python3 check_system.py`
- Service logs: `sudo journalctl -u relay-controller.service --no-pager`
- What you were trying to do when the error occurred

### Where to Get Help
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/Pi-5-Relay-Controller/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/Pi-5-Relay-Controller/discussions)
- **Reddit**: r/raspberry_pi community

## 🔄 Recovery Procedures

### Complete System Recovery
```bash
# 1. Backup current state (if needed)
cp relay_states.json relay_states.backup

# 2. Stop all services
sudo systemctl stop relay-controller.service

# 3. Reset GPIO
python3 reset_gpio.py

# 4. Clean installation
rm -rf venv
./quick_install.sh

# 5. Restore state (if needed)
cp relay_states.backup relay_states.json
sudo systemctl restart relay-controller.service
```

### Emergency GPIO Reset
```bash
# If GPIO is completely stuck
sudo systemctl stop relay-controller.service
echo "Resetting all GPIO pins..."
for pin in 10 12 13 14 15 6 17 18 19 20 21 22 23 24 25 26; do
    echo $pin > /sys/class/gpio/unexport 2>/dev/null || true
done
python3 reset_gpio.py
sudo systemctl start relay-controller.service
```

Remember: Most issues can be resolved by running `./quick_install.sh` again! 🔄
