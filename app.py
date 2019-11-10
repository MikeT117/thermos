import json
from Thermos import Thermos, make_response

server = Thermos()


@server.route("/", methods={"GET", "POST"})
def root(request):
    return server.render_template("test.html")


@server.route("/test", methods={"POST"})
def test(request):
    data = json.dumps({"id": 1, "name": "James Smith"})
    return make_response(
        "1.1", "200", "OK", data.encode(), "json"
    )


server.thermos_run()

