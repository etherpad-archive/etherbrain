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
FORK_ME = """<a href="https://github.com/etherpad-archive/etherbrain"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/365986a132ccd6a44c23a9169022c0b5c890c387/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f7265645f6161303030302e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"></a>"""

app = Flask(__name__)
app.debug = True


@app.route('/moz/<path:path>/')
def moz_pad(path):
    ether_path = "https://public.etherpad-mozilla.org/p/{}".format(path)
    req = requests.get(ether_path + "/export/txt")
    
    gh = login('etherbrain', token=GH_TOKEN)
    r = gh.repository('etherpad-archive', 'etherpad-archive.github.io')
    contents = r.contents(path='moz')

    print(contents)
    fname = path + ".md"
    if contents is None or fname not in contents:
        # create it for the first time
        r.create_file("moz/{}.md".format(path),
                      'etherpad from {}'.format(ether_path),
                      content=req.content)

    else:
        # update the file
        f = contents[fname]
        f.update('updated etherpad from {}'.format(ether_path),
                 content=req.content)
    
    return Response(
        'Check out: <a href="http://etherpad-archive.github.io/moz/{path}.md"'
        '>http://etherpad-archive.github.io/moz/{path}.md</a>'.format(path=path)
    )

@app.route('/')
def index():
    return Response("<html><head><title>Etherpad brain</title></head><body><h1>Hello I am the etherpad brain</h1>"
                    "<p>To archive https://public.etherpad-mozilla.org/p/XXX visit"
                    " https://etherbrain.herokuapp.com/moz/XXX/</p>{}</body></html>".format(FORK_ME))


if __name__ == "__main__":
    app.run(debug=True)
