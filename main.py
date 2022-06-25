import flask
from flask import render_template, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/api')
def api():
    latitude = request.args.get('a')
    longitude = request.args.get('b')
    id = request.args.get('i')
    print(id, latitude, longitude)
    return 'OK', 200

app.run()



