from flask import Flask,request

app = Flask(__name__)

@app.route('/hey', methods=['GET'])
def hey():
    val = request.args.get('fil')
    d = {
        "a": 23,
        "b": "hehe",
        "val":int(val)+23
    }
    return d
if __name__ == "__main__":
    app.run(debug=True)