from Thermos import Thermos, make_response, not_found

server = Thermos()


@server.route("/")
def test(request):
    """Need the request to be accessible here"""
    http_file = server.parse_response_file("test")
    print("FILE: ", http_file)
    if not http_file:
        return not_found()
    else:
        print("TEST", request.content_type)
        return make_response(
            request.http_version, "200", "OK", http_file, request.content_type
        )


server.initialise_server()

