import redis
import json
import requests

# Step 1: Establish a connection to Redis
def get_redis_connection():
    url = 'rediss://default:5626f63d709f49acbfd6ba8bad839ad5@factual-walrus-37316.upstash.io:37316'
    return redis.Redis.from_url(url)

# Step 2: Store JSON to Redis
def store_json(redis_conn, key, json_data):
    redis_conn.set(key, json.dumps(json_data))
    print("Stored ",key)

# Step 3: Retrieve JSON from Redis
def retrieve_json(redis_conn, key: str):
    print(f"KEY ====> {str(key)}")
    json_data = redis_conn.get(str(key))
    return json.loads(json_data) if json_data else None

# Step 4: Check if all URLs in the JSON resolve correctly
def check_urls(redis_conn, key: str):
    json_data = retrieve_json(redis_conn, str(key))
    if json_data == None:
        print("Not stored")
        return -1

    if json_data and 'streams' in json_data:
        # for stream in json_data['streams']:
        #     try:
        #         response = requests.head(stream['url'], allow_redirects=True, timeout=10)
        #         if response.status_code != 200:
        #             print("failed")
        #             return 0
        #     except requests.RequestException:
        #         print("failed")
        #         return 0
        result = next((stream for stream in json_data['streams'] if "Adaptive" in stream['title'] ), None)
        try:
            response = requests.head(result['url'], allow_redirects=True, timeout=10)
            if response.status_code != 200:
                print("failed")
                return 0
        except requests.RequestException:
            print("failed")
            return 0

    return json_data

# Sample JSON data
sample_json = {"streams":[{"title":"Vidplay (1920, 1080)","type":"movie","url":"https://ewal.v44381c4b81.site/_v2-wwdo/12a3c523fe105800ed8c394685aeeb0b902ea15c58e4bfed0b197baea93ece832257df1a4b6125fcfa38c35da05dee86aad28d46d73fc4e9d4e5a53b5277f1d634c711e30918b40a13c1b4bc6e4e7d11662686271c4675c39085fb09cea322992b15f541532ba10eabbb/h/ebddcbfcf4/bff;15a38634f803584ba8926411d7bee906856cab0654b5b7.m3u8"},{"title":"Vidplay (1280, 720)","type":"movie","url":"https://ewal.v44381c4b81.site/_v2-wwdo/12a3c523fe105800ed8c394685aeeb0b902ea15c58e4bfed0b197baea93ece832257df1a4b6125fcfa38c35da05dee86aad28d46d73fc4e9d4e5a53b5277f1d634c711e30918b40a13c1b4bc6e4e7d11662686271c4675c39085fb09cea322992b15f541532ba10eabbb/h/ebddcbfcf3/bff;15a38634f803584ba8926411d7bee906856cab0654b5b7.m3u8"},{"title":"Vidplay (640, 360)","type":"movie","url":"https://ewal.v44381c4b81.site/_v2-wwdo/12a3c523fe105800ed8c394685aeeb0b902ea15c58e4bfed0b197baea93ece832257df1a4b6125fcfa38c35da05dee86aad28d46d73fc4e9d4e5a53b5277f1d634c711e30918b40a13c1b4bc6e4e7d11662686271c4675c39085fb09cea322992b15f541532ba10eabbb/h/ebddcbfcf1/bff;15a38634f803584ba8926411d7bee906856cab0654b5b7.m3u8"},{"title":"Filemoon (1920, 1080)","type":"movie","url":"https://be4242.rcr52.ams03.cdn112.com/hls2/01/00120/z5iyz1joqxj1_x/index-v1-a1.m3u8?t=sYfDkAaBFD_R9y1VWzJQoOTMqWBhASdvvHpLFVs12ak&s=1713428173&e=43200&f=603942&srv=10&asn=212238&sp=5500"}]}

# Example usage
def check_redis(redis_conn, dbid: str):
    #store_json(redis_conn, store_key, sample_json)
    return check_urls(redis_conn, dbid)