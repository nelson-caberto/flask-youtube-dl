from flask import Flask, request, json, jsonify
from mydl import dl
import os

app = Flask(__name__)

DL = {}

#for debugging
@app.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/', methods=['POST', 'GET'])
@app.route('/<data>')
def root(data=None):
    method = request.method

    if method == 'POST' and request.headers['Content-Type'] == 'application/json':
        data = request.json

    elif method == 'GET' and request.args:
        data = dict(request.args)

    elif data:
        # data "may" be base64
        pass

    else:
        return "no data received"
    
    # Example:
    # data = {
    #     'site': 'website',
    #     'filename': '/path/to/filename',
    #     'url': 'http://www.something',
    #     'time': 'seconds'
    # }

    site = data['site']
    if not site in DL:
        DL[site] = dl(site)
    DL[site].add(data)

    return f'data received'

@app.before_first_request
def resume():
    for site in [file.split('.')[0] for file in os.listdir('.') if file.endswith(".pickle")]:
        DL[site] = dl(site)
        DL[site].resume()

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
