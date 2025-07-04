from flask import Flask
app = Flask(__name__)

@app.route('/soma')
def soma():
    x = 2
    y = 2
    res = x + y
    return '{} + {} = {}'.format(x,y,res)

@app.route('/subtracao')
def subtracao():
    x = 2
    y = 2
    res = x - y
    return '{} - {} = {}'.format(x,y,res)