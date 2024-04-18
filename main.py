"""
file written by : cool-dev-guy
based on ciarands vidsrc resolver's.
This is an ASGI made using fastapi as a proof of concept and for educational uses.The writer/dev is not responsible for any isues caused by this project.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware  # CORS
import gzip

from redis import Redis

#from redis import Redis

from models import vidsrctoget, vidsrcmeget, info, fetch
from io import BytesIO
from fastapi.responses import StreamingResponse, FileResponse
from models import stremio_addon,m3u8_parser, redis_checker

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
redcon: Redis = redis_checker.get_redis_connection()

@app.get('/')
async def index():
    return await info()


@app.get('/vidsrc/{dbid}')
async def vidsrc(dbid: str, s: int = None, e: int = None):
    if dbid:
        return {
            "status": 200,
            "info": "success",
            "sources": await vidsrctoget(dbid, s, e)
        }
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")


@app.get('/vsrcme/{dbid}')
async def vsrcme(dbid: str = '', s: int = None, e: int = None, l: str = 'eng'):
    if dbid:
        return {
            "status": 200,
            "info": "success",
            "sources": await vidsrcmeget(dbid, s, e)
        }
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")

# imDB id
@app.get('/streams/{dbid}')
async def streams(dbid: str = '', s: int = None, e: int = None):
    if dbid:
        try:
            return {
                "status": 200,
                "info": "success",
                "sources": await vidsrcmeget(dbid, s, e) + await vidsrctoget(dbid, s, e)
            }
        except:
            return []
    else:
        #raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")
        return []


@app.get("/subs")
async def subs(url: str):
    try:
        response = await fetch(url)
        with gzip.open(BytesIO(response.content), 'rt', encoding='utf-8') as f:
            subtitle_content = f.read()

        async def generate():
            yield subtitle_content.encode("utf-8")

        return StreamingResponse(generate(), media_type="application/octet-stream",
                                 headers={"Content-Disposition": "attachment; filename=subtitle.srt"})

    except:
        raise HTTPException(status_code=500, detail=f"Error fetching subtitle")


@app.get('/manifest.json')
async def get_manifest(request: Request):
    # Building the URL from request data
    url_scheme = request.url.scheme  # 'http' or 'https'
    server_host = request.headers.get("host")  # Get the host header
    full_url = f"{url_scheme}://{server_host}"
    #return {"URL": full_url}
    return stremio_addon.get_manifest(full_url)

@app.get('/stream/{type}/{id}.json')
async def get_stream(type: str, id: str):
    stored_json = redis_checker.check_redis(redcon,id)
    if stored_json == -1 or stored_json == 0:
        #return f"<h1>{type} {stremio_addon.transform_string(id)}"
        response = await streams( *stremio_addon.transform_string(id))
        if len(response) == 0:
            return []
        streamsList = [
            {'title': source['name'], 'type': type, 'url': source['data']['stream']}
            for source in response.get('sources', [])
            if source['data']['stream'] and source['data']['stream'].strip()
        ]
        m3u8_lists = m3u8_parser.getJSONs({'streams': streamsList})
        redis_checker.store_json(redcon,id,m3u8_lists)
        return m3u8_lists
    else:
        print("returned stored ")
        return stored_json

@app.get("/getlogo/")
def get_file():
    return FileResponse("vid-min.png", media_type='image/png', filename="vid-min.png")



