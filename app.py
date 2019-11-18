import json
from Thermos import Thermos, make_response, jsonify

server = Thermos()


@server.route("/", methods=["GET", "POST"])
def root(request):
    return server.render_template("test.html")


@server.route("/test", methods=["POST"])
def test(request):
    return jsonify({"id": 1, "name": "James Smith"})


server.thermos_run()

