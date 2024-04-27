import os
import time
import datetime
import redis

keydb_connection = redis.Redis(host=os.getenv("DB_LOCATION").split(":")[0], port=int(os.getenv("DB_LOCATION").split(":")[1]), db=0)

if __name__ == "__main__":
    print("Regulator running...")
    time.sleep(60)
    while True:
        print(f"Wipe Occurrence at {datetime.datetime.now().hour}:{datetime.datetime.now().minute}")
        keydb_connection.flushdb()
        time.sleep(60)
