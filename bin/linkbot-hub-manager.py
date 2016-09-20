#!/usr/bin/env python3

import bottle
from passlib.hash import sha256_crypt as sha256
import subprocess

def check(user, pw):
    print("{}:{}", user, pw)
    return True

@bottle.route('/')
@bottle.auth_basic(check)
def main_page():
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
        subprocess.check_output(['dpkg', '-s', 'linkbotd']),
        subprocess.check_output(['systemctl', 'status', 'linkbotd']).decode() )
    prex_status = """
        <h2> prex </h2>
        <pre>
        {}
        </pre>
    """.format(
        subprocess.check_output(['systemctl', 'status', 'prex']).decode() )

    return linkbotd_status + """
        <h1> Change Password </h1>
        <form action="/change_password" method="post">
            New Password: <input name="password" type="password" />
            Repeat new password: <input name="repeat_password" type="password" />
        </form>
    """

bottle.run(host='localhost', port=8080, debug=True)
