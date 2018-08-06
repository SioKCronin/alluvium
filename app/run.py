#!/usr/bin/env python
from app import get_alluvium_app
import redis

if __name__=="__main__":

    with open("../config/config.properties", "r") as f:
        lines = f.readlines()

    config={}
    for line in lines:
        if line.find("=")!=-1:
            ls = line.split("=")
            config[ls[0]]=ls[1]
    config["debug"]=args.debug

    # get the app and clear the redis db
    app = get_alluvium_app(config)
    redis_connection = redis.Redis(connection_pool=app.pool)
    redis_connection.flushall()
    sockeio.run(app)
    app.run(host='0.0.0.0', port=5000, debug = args.debug)

