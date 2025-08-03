#!/usr/bin/env python3
"""
Pi-5 Relay Controller System Check
==================================
This script checks if all system requirements are met before installation.
"""

import sys
import subprocess
import importlib
import platform
import os
from pathlib import Path

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_status(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_success(message):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[⚠]{Colors.NC} {message}")

def print_error(message):
    print(f"{Colors.RED}[✗]{Colors.NC} {message}")

def check_python_version():
    """Check if Python version is 3.9 or higher"""
    print_status("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.9+")
        return False

def check_raspberry_pi():
    """Check if running on Raspberry Pi"""
    print_status("Checking if running on Raspberry Pi...")
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        if 'Raspberry Pi' in cpuinfo:
            # Try to detect Pi model
            if 'Pi 5' in cpuinfo:
                print_success("Raspberry Pi 5 detected ✓")
            elif 'Pi 4' in cpuinfo:
                print_warning("Raspberry Pi 4 detected - Pi 5 recommended")
            else:
                print_warning("Older Raspberry Pi detected - Pi 5 recommended")
            return True
        else:
            print_error("Not running on Raspberry Pi")
            return False
    except FileNotFoundError:
        print_error("Cannot detect Raspberry Pi")
        return False

def check_system_packages():
    """Check if required system packages are available"""
    print_status("Checking system packages...")
    packages = [
        ('python3-pip', 'pip3 --version'),
        ('python3-venv', 'python3 -m venv --help'),
        ('git', 'git --version'),
        ('curl', 'curl --version'),
    ]
    
    all_good = True
    for package, command in packages:
        try:
            result = subprocess.run(command.split(), 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                print_success(f"{package} ✓")
            else:
                print_error(f"{package} not working properly")
                all_good = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print_error(f"{package} not found")
            all_good = False
    
    return all_good

def check_gpio_access():
    """Check GPIO access and gpiod availability"""
    print_status("Checking GPIO access...")
    
    # Check if gpiod tools are available
    try:
        result = subprocess.run(['gpioinfo'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            print_success("gpiod tools available ✓")
        else:
            print_warning("gpiod tools not working - will be installed")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_warning("gpiod tools not found - will be installed")
    
    # Check if user is in gpio group
    try:
        import grp
        gpio_group = grp.getgrnam('gpio')
        current_user = os.getenv('USER')
        if current_user in gpio_group.gr_mem:
            print_success(f"User '{current_user}' is in gpio group ✓")
            return True
        else:
            print_warning(f"User '{current_user}' not in gpio group - will be added")
            return True
    except KeyError:
        print_warning("gpio group not found - will be created")
        return True

def check_python_packages():
    """Check if Python packages can be imported"""
    print_status("Checking Python package availability...")
    
    packages = [
        'flask',
        'werkzeug',
        'jinja2',
        'click',
    ]
    
    available = []
    missing = []
    
    for package in packages:
        try:
            importlib.import_module(package)
            available.append(package)
        except ImportError:
            missing.append(package)
    
    if available:
        print_success(f"Available packages: {', '.join(available)}")
    
    if missing:
        print_warning(f"Missing packages: {', '.join(missing)} - will be installed")
    
    return True  # We'll install missing packages

def check_network():
    """Check network connectivity"""
    print_status("Checking network connectivity...")
    try:
        result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                              capture_output=True, 
                              timeout=10)
        if result.returncode == 0:
            print_success("Network connectivity ✓")
            return True
        else:
            print_warning("Network connectivity issues")
            return False
    except subprocess.TimeoutExpired:
        print_warning("Network check timeout")
        return False

def check_disk_space():
    """Check available disk space"""
    print_status("Checking disk space...")
    try:
        statvfs = os.statvfs('.')
        free_space = statvfs.f_frsize * statvfs.f_bavail
        free_mb = free_space / (1024 * 1024)
        
        if free_mb > 500:  # 500MB minimum
            print_success(f"Available disk space: {free_mb:.0f} MB ✓")
            return True
        else:
            print_warning(f"Low disk space: {free_mb:.0f} MB - 500MB recommended")
            return True  # Warning but not blocking
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return True

def main():
    """Main system check function"""
    print("🔍 Pi-5 Relay Controller System Check")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Raspberry Pi", check_raspberry_pi),
        ("System Packages", check_system_packages),
        ("GPIO Access", check_gpio_access),
        ("Python Packages", check_python_packages),
        ("Network", check_network),
        ("Disk Space", check_disk_space),
    ]
    
    results = []
    for name, check_func in checks:
        print()
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 40)
    print("📋 System Check Summary:")
    print("=" * 40)
    
    all_passed = True
    critical_failed = False
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")
            all_passed = False
            if name in ["Python Version", "Raspberry Pi"]:
                critical_failed = True
    
    print("\n" + "=" * 40)
    
    if critical_failed:
        print_error("❌ Critical requirements not met!")
        print_error("Please fix the critical issues before installation.")
        return False
    elif all_passed:
        print_success("✅ All checks passed! Ready for installation.")
        return True
    else:
        print_warning("⚠️  Some checks failed but installation can proceed.")
        print_warning("Missing components will be installed automatically.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
