# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify
import sys
sys.path.append("customlib");
import classification
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        question_list = request.form['questions'].split(',')
        input_list = request.form['inputs'].split(',')

        question = clf.queation(question_list, input_list)
        answer = clf.answer(question_list, input_list)

        if answer == "":
            pass
        else:
            t={"Answer":str(answer)}
            return jsonify(t)

        t={"Question":question}
        return jsonify(t)
    else:
        return "hello"


if __name__ == "__main__":
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    clf = classification.classification()
    clf.load()
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.secret_key = "JJJJJJJJJJ"
    app.run(HOST, PORT)