from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def main():
    return "starter code"

@app.route('/<site>/<filename>', methods=['GET'])
def add(site, filename):
    return f"{site} {filename} {json.dumps(request.args)}"

if __name__ == "__main__":
    app.run(debug=True)