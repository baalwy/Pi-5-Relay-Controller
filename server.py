# Raspberry Pi Relay Controller

from __future__ import print_function

import sys
import time
import json

from flask import Flask, make_response, render_template, request, jsonify, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from functools import wraps
import hashlib

from relay_lib import *

error_msg = '{msg:"error"}'
success_msg = '{msg:"success"}'

# Update the following list/tuple with the port numbers assigned to your relay board
# Extended to support 16 relays for Raspberry Pi 5 - Updated GPIO pins
PORTS = [10, 12, 13, 14, 15, 6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
NUM_RELAY_PORTS = len(PORTS)

RELAY_NAME = 'Pi-5 Relay Controller'

# Authentication settings
USERNAME = 'admin'
PASSWORD_HASH = hashlib.sha256('relay123'.encode()).hexdigest()  # Default password: relay123
SECRET_KEY = 'your-secret-key-change-this-in-production'

# initialize the relay library with the system's port configuration
try:
    if init_relay(PORTS):
        # turn all of the relays off, so we're starting with a clean slate.
        relay_all_off()
    else:
        print("Port configuration error")
        # exit the application
        sys.exit(0)
except Exception as e:
    print(f"Error initializing relay system: {e}")
    print("Continuing in simulation mode...")

app = Flask(__name__)
app.secret_key = SECRET_KEY

bootstrap = Bootstrap(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

root_dir = '/home/pi/pi-relay-controller-modmypi2025'
with open('{}/channels.json'.format(root_dir)) as json_file:
    channel_config = json.load(json_file)

supported_channels = []
for channel in channel_config['channels']:
    if channel['active'] == 'true':
        print('channel: ', channel['channel'])
        supported_channels.append(PORTS[channel['channel'] - 1])
    else:
        relay_off(channel['channel'])

print(supported_channels)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username == USERNAME and password_hash == PASSWORD_HASH:
            session['logged_in'] = True
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة!', 'error')

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    print("Loading app Main page")
    return render_template('index.html', relay_name=RELAY_NAME, channel_info=channel_config['channels'])


@app.route('/status/<int:relay>')
@login_required
def api_get_status(relay):
    res = relay_get_port_status(relay)
    if res:
        print("Relay is ON")
        return make_response("1", 200)
    else:
        print("Relay is OFF")
        return make_response("0", 200)


@app.route('/toggle/<int:relay>')
@login_required
def api_toggle_relay(relay):
    print("Executing api_relay_toggle:", relay)
    relay_toggle_port(relay)
    return make_response(success_msg, 200)


@app.route('/on/<int:relay>')
@login_required
def api_relay_on(relay):
    print("Executing api_relay_on:", relay)
    if validate_relay(relay):
        print("valid relay")
        relay_on(relay)
        return make_response(success_msg, 200)
    else:
        print("invalid relay")
        return make_response(error_msg, 404)


@app.route('/off/<int:relay>')
@login_required
def api_relay_off(relay):
    print("Executing api_relay_off:", relay)
    if validate_relay(relay):
        print("valid relay")
        relay_off(relay)
        return make_response(success_msg, 200)
    else:
        print("invalid relay")
        return make_response(error_msg, 404)


@app.route('/all_on/')
@login_required
def api_relay_all_on():
    print("Executing api_relay_all_on")
    relay_all_on(supported_channels)
    return make_response(success_msg, 200)


@app.route('/all_off/')
@login_required
def api_all_relay_off():
    print("Executing api_relay_all_off")
    relay_all_off(supported_channels)
    return make_response(success_msg, 200)

@app.route('/reboot/<int:relay>')
@login_required
def api_relay_reboot(relay, sleep_time=3):
    print("Executing api_relay_reboot:", relay)
    if validate_relay(relay):
        print("valid relay")
        relay_off(relay)
        time.sleep(sleep_time)
        relay_on(relay)
        return make_response(success_msg, 200)
    else:
        print("invalid relay")
        return make_response(error_msg, 404)


@app.errorhandler(404)
def page_not_found(e):
    print("ERROR: 404")
    return render_template('404.html', the_error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    print("ERROR: 500")
    return render_template('500.html', the_error=e), 500


def validate_relay(relay):
    # Make sure the port falls between 1 and NUM_RELAY_PORTS
    return (relay > 0) and (relay <= NUM_RELAY_PORTS)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('500.html'), 403

if __name__ == "__main__":
    # On the Pi, you need to run the app using this command to make sure it
    # listens for requests outside of the device.
    print("Starting Relay Controller server on all interfaces (0.0.0.0:5000)")
    app.run(host='0.0.0.0', port=5000, debug=False)
