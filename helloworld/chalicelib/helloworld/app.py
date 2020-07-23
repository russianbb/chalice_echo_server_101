from chalice import Chalice, Response
from chalice import NotFoundError, BadRequestError
from urllib.parse import urlparse, parse_qs

app = Chalice(app_name='helloworld')
app.debug = True

CITIES_TO_STATE = {
    'sao-paulo': 'SP',
    'natal': 'RN',
    'fortaleza': 'CE'
}

OBJECTS = {
}


@app.route('/', methods=['GET'])
def index():
    return Response(
        body='hello world',
        headers={'Content-Type': 'text/plain'},
        status_code=200
    )


@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index2():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {'states': parsed.get('states', [])}

@app.route('/cities/{city}', methods=['GET'])
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError(f"Unknown city {city}. Options are: {', '.join(CITIES_TO_STATE)}")


@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    with open('bdd.txt', 'a') as f:
        f.write(value)
    return {'value': value}


@app.route('/resource', methods=['GET'])
def get_test_values():
    res = {}
    line = 0
    with open('bdd.txt', 'r') as f:
        for _ in f.readlines:
            res[line] = _
    return res


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)


@app.route('/objects', methods=['GET'])
def all_objects():
    return OBJECTS

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
