import httpx,base64
from fastapi import HTTPException
from urllib.parse import unquote

BASE = 'http://localhost:8000'

async def default():
    return ''

async def error(err:str):
    # TODO
    #    return {
    #        "status":500,
    #        "info":err,
    #        "sources":[]
    #    }
    print(err) # for understanding whats gone wrong in the deployment.viewable in vercel logs.
    return {}
async def decode_url(encrypted_source_url:str,VIDSRC_KEY:str):
    standardized_input = encrypted_source_url.replace('_', '/').replace('-', '+')
    binary_data = base64.b64decode(standardized_input)
    encoded = bytearray(binary_data)
    key_bytes = bytes(VIDSRC_KEY, 'utf-8')
    j = 0
    s = bytearray(range(256))

    for i in range(256):
      j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
      s[i], s[j] = s[j], s[i]

    decoded = bytearray(len(encoded))
    i = 0
    k = 0
    for index in range(len(encoded)):
      i = (i + 1) & 0xff
      k = (k + s[i]) & 0xff
      s[i], s[k] = s[k], s[i]
      t = (s[i] + s[k]) & 0xff
      decoded[index] = encoded[index] ^ s[t]
    decoded_text = decoded.decode('utf-8')
    print(unquote(decoded_text))
    return unquote(decoded_text)

async def fetch(url:str,headers:dict={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    },method:str="GET",data=None,redirects:bool=True):
    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        if method=="GET":
            response = await client.get(url,headers=headers)
            return response
        if method=="POST":
            response = await client.post(url,headers=headers,data=data)
            return response
        else:
            return "ERROR"
        
