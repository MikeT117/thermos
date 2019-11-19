# Thermos

My attempt at an extremely basic http server, influenced from my use of the Flask framework.

Defaults:
Port = 5000
Address = 127.0.0.1
Static Folder = ./static
Template Folder = ./templates

## Usage

Create an instance of Thermos
`server = Thermos(Port, Address, Static, Templates)`

### Adding a route

Similar to Flask a route is added with a route decorator with a function for your return, The request is returned as an argument to your function.

`@server.route("/", methods=['GET']) def function(request): return server.render_template("index.html")`

#### Returning json

You can return a json response using the jsonify function, this will encode your return data to json and return the result to the client.

`@server.route("/json", methods=['GET']) def function(request): return jsonify({"id": 1, "username"; "jdoe"})`

#### Accessing request data

The request data is accessible as an argument from the route function e.g. below, This allows you to access, the request location, headers and body/json.

`@app.route("/", methods=['POST']) def handle_post(request): print(request.json['']) print(request.location)`

#### Custom response

    You can create a custom response utilising make_respose

#### Static files

    You can send static files from the defined static directory using send_static_file
