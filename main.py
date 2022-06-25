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
    return render_template("index.html")

@app.route('/get')
def api_get():
    id = request.args.get('i')

    answer={}
    answer['id'] = id
    answer['lastupdated'] = r.hget("watch:" + id, "lastupdated")
    answer['longitude'] = r.hget("watch:" + id, "longitude")
    answer['latitude'] = r.hget("watch:" + id, "latitude")

    print(answer)
    return json.dumps(answer), 200

@app.route('/set')
def api_set():
    id = request.args.get('i')
    latitude = float(request.args.get('a'))
    longitude = float(request.args.get('b'))
    print(id, longitude, latitude )
    
    now = datetime.datetime.now()
    r.zrem("watch", id)
    r.hset("watch:" + id, "lastupdated", now.strftime("%Y%m%d%H%M%S") )
    r.hset("watch:" + id, "longitude", longitude)
    r.hset("watch:" + id, "latitude", latitude)

    return 'OK', 200

app.run()



