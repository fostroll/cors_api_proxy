# -*- coding: utf-8 -*-

reqs = set()
def add_req (req): reqs.add(req)
def remove_req (req): reqs.discard(req)
def has_req(req): return req in reqs
def find_req (request):
    res = False
    args = request.args.to_dict(flat=False)
    reqid = args.get('reqid', [None])[0]
    need_test = args.get('test', [None])[0] == 'true'
    if reqid:
        if need_test:
            res = ('', 204) if has_req(reqid) else err_not_found(None)
        else:
            add_req(reqid)
            print('reqid {} start'.format(reqid))
    return res, reqid, args
