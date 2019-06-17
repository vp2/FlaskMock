from multiprocessing.pool import ThreadPool

from flask import Flask, request, Response, jsonify

from requestprocessor.requestprocessor import RequestProcessor

app = Flask(__name__)

thread_limit = 3
req_processor = RequestProcessor(ThreadPool(thread_limit))


@app.route("/api/task/async-apply/sample-endpoint", methods=["GET", "POST"])
def run_sum():
    res = req_processor.process_request(request)
    return res if isinstance(res, Response) else jsonify(res)


@app.route("/api/task/callback", methods=["GET", "POST"])
def get_callback():
    print("Callback route called with data:")
    print(request.data)
    return "OK"
