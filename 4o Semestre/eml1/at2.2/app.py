from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/soma', methods=['GET','POST'])
def soma():
    if request.method == 'GET':
        if 'op1' in request.args:
            x = int(request.args['op1'])
        else:
            return "op1 não informado", 400
        if 'op2' in request.args:
            y = int(request.args['op2'])
        else:
            return "op2 não informado", 400
    else:
        request_data = request.get_json()
        if 'op1' in request_data:
            x = int(request_data['op1'])
        else:
            return "op1 não informado", 400
        if 'op2' in request_data:
            y = int(request_data['op2'])
        else:
            return "op2 não informado", 400

    res = x + y
    response = {
        'op1': x,
        'op2': y,
        'operacao': 'soma',
        'resultado': res
    }
    return jsonify(response)


@app.route('/subtracao', methods=['GET','POST'])
def subtracao():
    if request.method == 'GET':
        if 'op1' in request.args:
            x = int(request.args['op1'])
        else:
            return "op1 não informado", 400
        if 'op2' in request.args:
            y = int(request.args['op2'])
        else:
            return "op2 não informado", 400
    else:
        request_data = request.get_json()
        if 'op1' in request_data:
            x = int(request_data['op1'])
        else:
            return "op1 não informado", 400
        if 'op2' in request_data:
            y = int(request_data['op2'])
        else:
            return "op2 não informado", 400

    res = x - y
    response = {
        'op1': x,
        'op2': y,
        'operacao': 'subtracao',
        'resultado': res
    }
    return jsonify(response)