import json
import requests
import m3u8
from urllib.parse import urljoin, urlparse

# Function to get base URL from the full URL of the M3U8 file
def get_base_url(full_url):
    parsed_url = urlparse(full_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}/"
    return base_url

# Function to download and parse M3U8 content from a URL
def download_and_parse_m3u8(url):
    response = requests.get(url)
    if response.status_code == 200:
        return m3u8.loads(response.text)
    else:
        print(f"Failed to download M3U8 file from {url}. Status code:", response.status_code)
        return None

# Main function to process the streams
def process_streams(streams_json):
    results = []
    for stream in streams_json["streams"]:
        title = stream["title"]
        type_ = stream["type"]
        url = stream["url"]
        parsed_playlist = download_and_parse_m3u8(url)
        if parsed_playlist:
            base_url = get_base_url(url)
            for variant in parsed_playlist.playlists:
                resolution = str(variant.stream_info.resolution) if variant.stream_info.resolution else "unknown"
                full_url = urljoin(base_url, variant.uri)
                results.append({
                    "title": f"{title} {resolution.replace(', ','x')}",
                    "type": type_,
                    "url": full_url
                })

            if 'play' in title:
                results.append({
                    "title": f"{title} All-Adaptive",
                    "type": type_,
                    "url": url
                })
        else:
            print(f"Could not load M3U8 content for {title}")
    return results

# Sample JSON input
input_json = """
{
  "streams": [
    {
      "title": "Vidplay",
      "type": "movie",
      "url": "https://ewal.v44381c4b81.site/_v2-wwdo/12a3c523fe105800ed8c394685aeeb0b902ea15c58e4bfed0b197baea93ece832257df1a4b6125fcfa38c35da05dee86aad28d46d73fc4e9d4e5a53b5277f1d634c711e30918b40a13c1b4bc6e4e7d11662686271c4675c39085fb09cea322992b15f541532ba10eabbb/h/list;15a38634f803584ba8926411d7bee906856cab0654b5b7.m3u8"
    },
    {
      "title": "Filemoon",
      "type": "movie",
      "url": "https://be4242.rcr52.ams03.cdn112.com/hls2/01/00120/z5iyz1joqxj1_x/master.m3u8?t=o8WZKaDU99TRuBK0qVZ-SHUY-53t4VfQtdwVbSxxlmM&s=1713421440&e=43200&f=603942&srv=10&asn=212238&sp=5500"
    }
  ]
}
"""

def getJSONs(streams_json_in):
    output_streams = process_streams(streams_json_in)
    return {"streams": output_streams}

