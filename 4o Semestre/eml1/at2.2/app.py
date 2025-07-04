from flask import Flask, request

app = Flask(__name__)

@app.route('/soma')
def soma():
    if 'op1' in request.args:
        x = int(request.args['op1'])
    else:
        return "op1 não informado", 400
    if 'op2' in request.args:
        y = int(request.args['op2'])
    else:
        return "op2 não informado", 400
    res = x + y
    return '{} + {} = {}'.format(x,y,res)

@app.route('/subtracao')
def subtracao():
    if 'op1' in request.args:
        x = int(request.args['op1'])
    else:
        return "op1 não informado", 400
    if 'op2' in request.args:
        y = int(request.args['op2'])
    else:
        return "op2 não informado", 400
    res = x - y
    return '{} - {} = {}'.format(x,y,res)