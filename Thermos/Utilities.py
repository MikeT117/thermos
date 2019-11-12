import json


def make_response(
    http_version, status_code, status_text, data, content_type, headers=None
):
    try:
        if (
            http_version is None
            or status_code is None
            or status_text is None
            or data is None
        ):
            raise TypeError("Malformed response data")

        if type(data) is not bytes:
            raise TypeError("Data must be bytes")
    except TypeError as err:
        print(err)
        return False

    # Basic setting of 'Content-Type' header based on file extension,
    # not robust and certainly doesn't cover all possible type/subtypes
    # but for this very basic server it gets the job done
    if content_type in {"jpg", "jpeg", "png", "ico", "webp", "gif"}:
        content_type = f"Content-type: image/{content_type}"
    elif content_type in {"html"}:
        content_type = f"Content-type: text/{content_type}; charset=UTF-8"
    elif content_type in {"css"}:
        content_type = f"Content-type: text/{content_type}; charset=UTF-8"
    elif content_type in {"json", "js"}:
        content_type = f"Content-type: application/javascript"
    else:
        content_type = b"Content_type: text/html; charset=UTF-8"

    # Return response
    ret = b"HTTP/%b %b %b\n%b\n" % (
        http_version.encode(),
        status_code.encode(),
        status_text.encode(),
        content_type.encode(),
    )

    # Parse additional headers and add to response
    if headers is not None:
        for i in headers:
            ret += i.encode() + b"\n"
    return ret + b"\n" + data


def parse_file(filename=None):
    try:
        if filename is None:
            raise TypeError("Filename not provided!")

        file = open(filename, "rb")
        ret = b""
        while True:
            line = file.readline()
            if len(line) <= 0:
                break
            ret += line
        return ret

    except (TypeError, FileNotFoundError):
        raise


def not_found():
    return make_response(
        "1.1",
        "404",
        "Not Found",
        b"<html><head></head><body><h1>404: Not found</h1></body></html>",
        "html",
    )


def server_error():
    return make_response(
        "1.1",
        "500",
        "Internal server error",
        b"<html><head></head><body><h1>500: Internal server error</h1></body></html>",
        "html",
    )


def method_not_allowed():
    return make_response(
        "1.1",
        "405",
        "Method Not Allowed",
        b"<html><head></head><body><h1>405: Method Not Allowed</h1></body></html>",
        "html",
    )


def jsonify(data):
    try:
        data = json.dumps(data)
        return make_response("1.1", "200", "OK", data.encode(), "json")
    except SyntaxError:
        raise
