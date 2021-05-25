from flask import Flask, request
import os, json

app = Flask(__name__)

queue = {}

@app.route('/')
def main():
    return json.dumps(queue)

@app.route('/<site>', methods=['GET'])
def add(site):
    if site not in queue:
        queue[site] = []
    queue[site].append({
        'filepath': os.path.join(site,request.args['filepath']),
        'filename': request.args['filename'],
        'url': request.args['url']
    })
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
