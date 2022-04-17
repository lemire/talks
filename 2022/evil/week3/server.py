from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<html><body>Hello World!</body></html>'

if __name__ == '__main__':
    app.run()