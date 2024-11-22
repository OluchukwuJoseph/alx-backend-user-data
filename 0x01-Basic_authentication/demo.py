from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/home')
def home():
    print(request.authorization)
    print(type(request.authorization))

    return jsonify(str(request.authorization)), 200


if __name__ == '__main__':
    app.run(debug=True)