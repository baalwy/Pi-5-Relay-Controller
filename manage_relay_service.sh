#!/bin/bash

# Relay Controller Service Management Script
# Usage: ./manage_relay_service.sh [start|stop|restart|status|logs|enable|disable]

SERVICE_NAME="relay-controller.service"

case "$1" in
    start)
        echo "Starting Relay Controller Service..."
        sudo systemctl start $SERVICE_NAME
        echo "Service started."
        ;;
    stop)
        echo "Stopping Relay Controller Service..."
        sudo systemctl stop $SERVICE_NAME
        echo "Service stopped."
        ;;
    restart)
        echo "Restarting Relay Controller Service..."
        sudo systemctl restart $SERVICE_NAME
        echo "Service restarted."
        ;;
    status)
        echo "Relay Controller Service Status:"
        sudo systemctl status $SERVICE_NAME --no-pager
        ;;
    logs)
        echo "Relay Controller Service Logs (last 50 lines):"
        sudo journalctl -u $SERVICE_NAME --no-pager -n 50
        ;;
    follow-logs)
        echo "Following Relay Controller Service Logs (Ctrl+C to exit):"
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    enable)
        echo "Enabling Relay Controller Service (auto-start on boot)..."
        sudo systemctl enable $SERVICE_NAME
        echo "Service enabled for auto-start."
        ;;
    disable)
        echo "Disabling Relay Controller Service (no auto-start on boot)..."
        sudo systemctl disable $SERVICE_NAME
        echo "Service disabled from auto-start."
        ;;
    test)
        echo "Testing Relay Controller Service..."
        echo "Checking if service is running..."
        if systemctl is-active --quiet $SERVICE_NAME; then
            echo "✅ Service is running"
            echo "Testing API..."
            response=$(curl -s http://localhost:5000/status/1)
            if [ $? -eq 0 ]; then
                echo "✅ API is responding: $response"
            else
                echo "❌ API is not responding"
            fi
        else
            echo "❌ Service is not running"
        fi
        ;;
    *)
        echo "Relay Controller Service Manager"
        echo "================================"
        echo "Usage: $0 {start|stop|restart|status|logs|follow-logs|enable|disable|test}"
        echo ""
        echo "Commands:"
        echo "  start       - Start the service"
        echo "  stop        - Stop the service"
        echo "  restart     - Restart the service"
        echo "  status      - Show service status"
        echo "  logs        - Show recent logs"
        echo "  follow-logs - Follow logs in real-time"
        echo "  enable      - Enable auto-start on boot"
        echo "  disable     - Disable auto-start on boot"
        echo "  test        - Test if service and API are working"
        echo ""
        echo "Current status:"
        if systemctl is-enabled --quiet $SERVICE_NAME; then
            echo "  Auto-start: ✅ Enabled"
        else
            echo "  Auto-start: ❌ Disabled"
        fi
        
        if systemctl is-active --quiet $SERVICE_NAME; then
            echo "  Service: ✅ Running"
        else
            echo "  Service: ❌ Stopped"
        fi
        ;;
esac
