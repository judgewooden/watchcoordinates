import flask
import json
import redis
import datetime
from flask import render_template, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
r = redis.Redis(decode_responses=True)

@app.route('/')
def root():
    mylist=[]
    for k in r.keys("watch:*"):
        mylist.append(k[6:])
    return render_template('index.html', watches=mylist)

# @app.route('/watch/<watch_id>')
#     return render_template("index.html")

@app.route('/get')
def api_get():
    id = request.args.get('id')

    answer={}
    answer['id'] = id
    answer['lastupdated'] = r.hget("watch:" + id, "lastupdated")
    if answer['lastupdated'] is None:
        if app.config["DEBUG"]:
            print(id, "NOT FOUND")
        return "", 404

    answer['longitude'] = r.hget("watch:" + id, "longitude")
    answer['latitude'] = r.hget("watch:" + id, "latitude")

    if app.config["DEBUG"]:
        print("get", answer)
    return json.dumps(answer), 200

@app.route('/set')
def api_set():
    if app.config["DEBUG"]:
        print("set", request.args )
    
    try:
        id = request.args.get('id')
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        if id is None or latitude is None or longitude is None:
            raise Exception("BAD REQUEST")
    except Exception as e:
        if app.config["DEBUG"]:
            print("ERROR", e)
        return 'ERROR' + e, 400


    now = datetime.datetime.now()

    r.hset("watch:" + id, "lastupdated", now.strftime("%Y%m%d%H%M%S") )
    r.hset("watch:" + id, "longitude", longitude)
    r.hset("watch:" + id, "latitude", latitude)
    return '', 200

if __name__ == "__main__":
    app.run()



