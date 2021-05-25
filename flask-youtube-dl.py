from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return "starter code"

@app.route('/<site>/<filename>')
def add(site, filename):
    return f"{site} {filename}"

if __name__ == "__main__":
    app.run(debug=True)