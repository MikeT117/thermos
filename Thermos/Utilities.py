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

    # Determining content type, Defaults to HTML
    content_types = {
        "css": b"Content-Type: text/css",
        "html": b"Content-Type: text/html",
        "js": b"Content-Type: application/javascript",
        "json": b"Content-Type: application/json",
        "jpg": b"Content-Type: image/jpg",
        "jpeg": b"Content-Type: image/jpeg",
        "gif": b"Content-Type: image/gif",
        "png": b"Content-Type: image/png",
        "jpg": b"Content-Type: image/jpg",
        "ico": b"Content-Type: image/ico",
    }

    # Set 'Content-Type' header based on extension, return html as default
    if content_type is None:
        content_type = content_types["html"]
    else:
        content_type = content_types[content_type]

    # Return response
    ret = b"HTTP/%b %b %b\n%b\n" % (
        http_version.encode(),
        status_code.encode(),
        status_text.encode(),
        content_type,
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
    except TypeError as err:
        print(err)
        return False

    try:
        file = open(filename, "rb")
        ret = b""
        while True:
            line = file.readline()
            if len(line) <= 0:
                break
            ret += line
        return ret

    except FileNotFoundError as err:
        print("%s not found" % filename)
        return False


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