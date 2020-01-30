#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response, stream_with_context
from requests import request as make_request
from requests.exceptions import ConnectionError as ConnError, \
                                MissingSchema, InvalidURL

from errors import err_bad_request, err_gateway_timeout
from utils import find_req

###
import sys
sys.path.append('../')
###
from cors_api_proxy import GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS


app = Flask(__name__)

watch_reqs = False

@app.route('/<path:url>', methods=[GET, POST, PUT,
                                   PATCH, DELETE, HEAD, OPTIONS])
def proxy (url):
    res = reqid = None
    if watch_reqs and request.method != OPTIONS:
        res, reqid, _ = find_req(request)

    if not res:
        try:
            req = make_request(request.method,
                               url,
                               params=request.args,
                               data=request.data,
                               cookies=request.cookies,
                               files=request.files,
                               stream=True)
            res = Response(stream_with_context(
                               req.iter_content(chunk_size=2048)
                           ),
                           #content_type=req.headers['content-type'],
                           status=req.status_code)
            for par in ['Date', 'Server', 'Content-Type',
                        'Content-Disposition', 'Content-Length']:
                if par in req.headers: res.headers[par] = req.headers[par]
            origin = request.environ.get('HTTP_ORIGIN', False)
            if origin:
                res.headers['Access-Control-Allow-Origin'] = origin
                res.headers['Access-Control-Allow-Credentials'] = 'true'

        except (MissingSchema, InvalidURL):
            res = err_bad_request('Invalid url "{}"'.format(url))
        except (ConnError, ConnectionError):
            res = err_gateway_timeout("Proxy can't establish connection "
                                      "with remote server")

        if reqid:
            remove_req(reqid)
    return res

if __name__ == '__main__':
    import sys
    if 'watch_reqs' in sys.argv:
        watch_reqs = True
    if 'prod' in sys.argv:
        app.run(host='0.0.0.0', port=5050, debug=True)
    else:
        from wsgiref.simple_server import make_server
        make_server('localhost', 8000, app).serve_forever()
