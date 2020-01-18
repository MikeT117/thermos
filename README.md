# Thermos

My attempt at an extremely basic http server, influenced from my use of the Flask framework (the name may have been a clue).

Thermos server defaults:
Port = 5000
Address = 127.0.0.1
Static Folder = ./static
Template Folder = ./templates

## Usage

Create an instance of Thermos

```
server = Thermos(Port, Address, Static, Templates)
```

### Adding a route

Similar to Flask a route is added with a route decorator, you provide a function for your return, the request is accessible as an argument in your function.

```
@server.route("/", methods=['GET'])
def function(request):
    return server.render_template("index.html")
```

#### Returning json

You can return a json response using the jsonify function, this will encode your return data to json and return the result to the client.

```
@server.route("/json", methods=['GET'])
def function(request):
    return jsonify({"id": 1, "username"; "jdoe"})
```

#### Accessing request data

The request data is accessible as an argument from the route function e.g. below, This allows you to access, the request location, headers and body/json.

```
@app.route("/", methods=['POST'])
def handle_post(request):
    print(request.json[''])
    print(request.location)
```

#### Custom response

You can construct a custom response utilising make_respose, it takes http_version, status_code, status_text, data, content_type and headers as arguments e.g.
Note: Content-type is already added based on the provided content type argument

```
@server.route("/", methods=['GET'])
def function(request):
    return make_response(1.1, 200, "OK", jsonify({id: 1}), "json" , headers={"access-control-allow-origin": "*"})
```

#### Static files

You can send static files from the defined static directory using send_static_file e.g.

```
@server.route("/", methods=['GET'])
def function(request):
    return server.send_static_file("script.js")
```
