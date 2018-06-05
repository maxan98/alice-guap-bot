#!/usr/bin/env python3
from api import app
from OpenSSL import SSL
context = ('185.243.131.130.crt','server.key')

app.run(host='185.243.131.130',port='443',
    debug = False, ssl_context=context)
