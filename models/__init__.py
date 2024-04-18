from .subtitle import subfetch
VERSION = '1.0.0'
from .vidsrcme import get as vidsrcmeget
from .vidsrcto import get as vidsrctoget
from .utils import fetch
# UTILS
async def info():
    return {
    "project":"vidsrc-streamio-addon",
    "note":"Streamio addon",
    "version": VERSION,
    "developer":"Ragesh Antony"
    }
