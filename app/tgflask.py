from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return '<h1>Hello World!</h1>'

@app.route('/sub')
def subpage():
    with open('data/nodes.txt','r') as f:
        nodes = f.read()
    return nodes


app.run(host='0.0.0.0',port=8080)