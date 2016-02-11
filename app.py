import os

import requests
from github3 import login

from flask import (
    Response,
    Flask,
    g,
    request
)

GH_TOKEN = os.getenv("TOKEN")


app = Flask(__name__)
app.debug = True


@app.route('/moz/<path:path>/')
def moz_pad(path):
    ether_path = "https://public.etherpad-mozilla.org/p/{}".format(path)
    req = requests.get(ether_path + "/export/txt")
    
    gh = login('etherbrain', token=GH_TOKEN)
    r = gh.repository('etherpad-archive', 'etherpad-archive.github.io')
    contents = r.contents(path='moz')

    if contents is None or path not in contents:
        # create it for the first time
        r.create_file("moz/" + path,
                      'etherpad from {}'.format(ether_path),
                      content=req.content)

    else:
        # update the file
        return Response(
            "Check out: http://etherpad-archive.github.io/moz/{}".format(path)
        )
    
    return Response(
        "Check out: http://etherpad-archive.github.io/moz/{}".format(path)
    )

@app.route('/')
def index():
    return Response("Hello I am the etherpad brain")


if __name__ == "__main__":
    app.run(debug=True)
