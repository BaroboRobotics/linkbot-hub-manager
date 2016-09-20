#!/usr/bin/env python3

import bottle
from passlib.hash import sha256_crypt as sha256
import re
import subprocess

def check(user, pw):
    print("{}:{}", user, pw)
    return True

@bottle.route('/')
@bottle.auth_basic(check)
def main_page():
    try:
        dpkg_status = subprocess.check_output(['dpkg', '-s', 'linkbotd']).decode()
    except subprocess.CalledProcessError as e:
        dpkg_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    try:
        linkbotd_status = subprocess.check_output(['systemctl', 'status', 'linkbotd']).decode()
    except subprocess.CalledProcessError as e:
        linkbotd_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    try:
        prex_status = subprocess.check_output(['systemctl', 'status', 'prex']).decode()
    except subprocess.CalledProcessError as e:
        prex_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())
        
    linkbotd_status = """
        <h1> Status </h1>
        <h2> linkbotd </h2>
        <h3> Package Info </h3>
        <pre>
        {}
        </pre>
        <h3> Daemon Status </h3>
        <pre>
        {}
        </pre>
    """.format(
        dpkg_status,
        linkbotd_status)

    prex_status = """
        <h2> prex </h2>
        <pre>
        {}
        </pre>
    """.format(
        prex_status )

    return linkbotd_status + prex_status + """
        <h1> Change Password </h1>
        <form action="/change_password" method="post">
            New Password: <input name="password" type="password" />
            Repeat new password: <input name="repeat_password" type="password" />
        </form>
    """

@bottle.route('/<module>/<function>')
@bottle.auth_basic(check)
def handle_all(module, function):
    if function == 'version':
        if module in ['liblinkbot', 'linkbotd', 'linkbot-firmware']:
            return handle_dpkg_version(module)
        elif module in ['prex', 'pylinkbot3']:
            return handle_pip_version(module)
        else:
            return "Cannot get version of module: {}".format(module)

    if function == 'restart':
        if module in ['linkbotd', 'prex']:
            return handle_restart(module)
        else:
            return "Cannot restart module: {}".format(module)

    if function == 'stop':
        if module in ['linkbotd', 'prex']:
            return handle_stop(module)
        else:
            return "Cannot stop module: {}".format(module)

    if function == 'stop':
        if module in ['linkbotd', 'prex']:
            return handle_start(module)
        else:
            return "Cannot stop module: {}".format(module)

    if function == 'reboot':
        try:
            output = subprocess.check_output(['reboot'])
            return 'OK'
        except Exception as e:
            return 'Could not restart {}: {}'.format(module, e)
        

def handle_dpkg_version(module):
    try:
        output = subprocess.check_output(['dpkg', '-s', module])
        m = re.search('Version: (.*)', output.decode())
        return m.group(1)
    except Exception as e:
        return "Could not get version on module '{}'".format(module) + str(e)
            
def handle_pip_version(module):
    try:
        output = subprocess.check_output(['pip3', 'show', module])
        m = re.search('Version: (.*)', output.decode())
        return m.group(1)
    except:
        return "Could not get version on module '{}'".format(module)

def handle_restart(module):
    try:
        output = subprocess.check_output(['systemctl', 'restart', module])
        return 'OK'
    except Exception as e:
        return 'Could not restart {}: {}'.format(module, e)

def handle_stop(module):
    try:
        output = subprocess.check_output(['systemctl', 'stop', module])
        return 'OK'
    except Exception as e:
        return 'Could not stop {}: {}'.format(module, e)

def handle_start(module):
    try:
        output = subprocess.check_output(['systemctl', 'start', module])
        return 'OK'
    except Exception as e:
        return 'Could not start {}: {}'.format(module, e)

bottle.run(host='localhost', port=8080, debug=True)
