from flask import Flask, request, jsonify
from base64 import b64decode
from os.path import join as pj
import youtube_dl

app = Flask(__name__)

queue = {}

class logger(object):
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def hook(d):
    print(d)

@app.route('/')
def main():
    return jsonify(queue)

def download():
    for site in queue:
        for item in queue[site]:
            ydl_opts = {
                'outtmpl': pj(item['filepath'],item['filename']),
                'logger': logger(),
                'progress_hooks': [hook]
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([item['url']])

@app.route('/<site>', methods=['GET'])
def add(site):
    if site not in queue:
        queue[site] = []
    queue[site].append({
        'filepath': request.args['filepath'],
        'filename': request.args['filename'],
        'url': str(b64decode(request.args['url']),'utf-8')
    })
    download()
    return jsonify({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
