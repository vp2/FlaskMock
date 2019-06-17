import json
import requests
from flask import Response
from objectpath import *
from time import sleep

callback_timeout = 30


def callback_func(url, method="get", payload=""):
    print("Callback thread started.")
    print("URL=", url)
    print("Method=", method)
    print("Payload=", payload)
    sleep(5)
    response = requests.request(method, url, data=payload, timeout=callback_timeout)
    print("Response=", response.status_code)
    print("Callback thread finished.")
    return response.status_code


class Processor:
    thread_pool = None

    def __init__(self, thread_pool=None):
        self.thread_pool = thread_pool

    def process(self, req):
        data = json.loads(req.data)
        tree = Tree(data)
        res = {"token": tree.execute("$.auth_token"),
               "dist_id": tree.execute("$.args.partner_distribution_id"),
               "mod_id_1": tree.execute("$.args.segments[1].modeled_id"),
               "segments": tree.execute("$.args.segments")}

        # res = Response(
        #     response=json.dumps(dict(error='err')),
        #     status=400, mimetype='application/json')

        self.thread_pool.apply_async(callback_func, ("http://localhost:5000/api/task/callback", "post", str(res)))

        return res
