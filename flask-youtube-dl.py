from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def main():
    return "starter code"

@app.route('/<site>', methods=['GET'])
def add(site):
    filepath = os.path.join(site,request.args['filepath'])
    filename = request.args['filename']
    url = request.args['url']
    return f'added {filename}'

if __name__ == "__main__":
    app.run(debug=True)
