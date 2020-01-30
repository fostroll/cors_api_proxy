#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from proxy import app

if 'watch_reqs' in sys.argv:
    watch_reqs = True
if 'prod' not in sys.argv:
    app.run(host='0.0.0.0', port=5050, debug=True)
else:
    from wsgiref.simple_server import make_server
    make_server('localhost', 8000, app).serve_forever()
