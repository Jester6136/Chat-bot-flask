from flask import Flask,render_template,request,jsonify
from sqlalchemy import true

from chatbot import response_msg

app = Flask(__name__)

@app.route('/',methods=["GET"])

def index_get():
    return render_template('base.html')


@app.route('/predict',methods=["POST"])
def predict():
    text = request.get_json().get("message")

    response = response_msg(text)
    message = {"answer":response}
    return jsonify(message)

if __name__ =='__main__':
    app.run(debug=True)