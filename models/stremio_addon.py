import requests

# Define the base API URL
vidsrc_api = 'http://localhost:8000'

# Define the manifest
MANIFEST_STREMIO = {
    "id": "org.rageshantony.vidsrc",
    "version": "1.0.0",
    "name": "VidSRC",
    "description": "This addon provides HLS links from VidSRC. Users can select from any one of the HLS sources. \n\n"
                   " Note: Many ISPs block VidSRC. If the file fails always, try opening https://vidsrc.to/ in web browser. "
                   "if fails, then use VPN. \n\n By Ragesh D Antony",
    "logo" : "/getlogo",
    "resources": ["stream"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt"],
    'catalogs': [
        {'type': 'movie', 'id': 'Hello, Python'},
        {'type': 'series', 'id': 'Hello, Python'}
    ],
}

def get_manifest(base):
    man = MANIFEST_STREMIO
    # replace "logo" : "/getlogo" in MANIFEST_STREMIO as base +
    man["logo"] = f"{base}/getlogo"
    return  man
def transform_string(input):
    # Split the input string by colon into an array
    parts = input.split(':')

    # Check if the split operation gave us exactly three parts
    if len(parts) == 3:
        ID, S, E = parts
        # Return the new formatted string
        #return f"{ID}?s={S}&e={E}"
        return ID, S, E
    else:
        # Return an error message if the input format is not as expected
        return input,None,None


def get_stream_url(type, id):
    print('getStreamURL', type, id)
    try:
        url = ''
        if type == 'movie':
            url = f"{vidsrc_api}/vidsrc/{id}"
        elif type == 'series':
            url = f"{vidsrc_api}/vidsrc/{transform_string(id)}"
            print(url)
        else:
            url = f"{vidsrc_api}/vidsrc/{id}"

        response = requests.get(url)

        if response.status_code == 200 and response.json().get('status') == 200 and response.json().get(
                'info') == "success":
            streams = [{'title': source['name'], 'type': type, 'url': source['data']['stream']} for source in
                       response.json().get('sources', [])]

            return {'streams': streams}
        else:
            # Handle unexpected response structure or error status
            print('Unexpected response or error status:', response)
            return {'streams': []}
    except Exception as error:
        # Handle errors like network issues
        print('Error fetching stream data:', error)
        return {'streams': []}
