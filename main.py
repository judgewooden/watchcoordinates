import flask
import json
import redis
import datetime
from flask import render_template, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
r = redis.Redis(decode_responses=True)

@app.route('/web')
def root_web():
    mylist=[]
    for k in r.keys("watch:*"):
        mylist.append(k[6:])
    return render_template('web.html', watches=mylist)

@app.route('/')
def root_mobile():
    mylist=[]
    for k in r.keys("watch:*"):
        mylist.append(k[6:])
    return render_template('index.html', watches=mylist)

@app.route('/compass')
def compass_mobile():
    return render_template('compass.html')

@app.route('/get')
def api_get():
    id = request.args.get('id').strip()

    answer={}
    answer['id'] = id
    answer['lastupdated'] = r.hget("watch:" + id, "lastupdated")
    if answer['lastupdated'] is None or id is None or len(id) < 3:
        if app.config["DEBUG"]:
            print("NOT FOUND", id)
        return "", 404

    print("hello")
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
        id = request.args.get('id').strip()
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        if id == None or len(id) < 3:
            raise Exception("id less than 3 characters")
        if latitude is None:
            raise Exception("latidude missing")
        if longitude is None:
            raise Exception("longitude missing")
    except Exception as e:
        if app.config["DEBUG"]:
            print("BAD REQUEST", e)
        return '', 400

    now = datetime.datetime.now()

    r.hset("watch:" + id, "lastupdated", now.strftime("%Y-%m-%d %H:%M:%S") )
    r.hset("watch:" + id, "longitude", longitude)
    r.hset("watch:" + id, "latitude", latitude)
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
