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

def decode(base):
    return str(b64decode(base),'utf-8')

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
    '''
        requires all GET parameters to be base64 encoded
        encoding is to eliminate the need to work around special characters
    '''
    if site not in queue:
        queue[site] = []
    queue[site].append({
        'filepath': decode(request.args['filepath']),
        'filename': decode(request.args['filename']),
        'url':      decode(request.args['url'])
    })
    download()
    return jsonify({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
