#!/usr/bin/env python3
from bottle import route, run

import subprocess


@route('/win')
def hello():
    subprocess.run(["sudo", "python3", "print_coupon.py", "-s", "http://127.0.0.1:5000","--method","vegas"])


run(host='0.0.0.0', port=8080, debug=True)
