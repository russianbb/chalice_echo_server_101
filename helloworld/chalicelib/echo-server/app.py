from boto3.session import Session
from chalice import Chalice
from chalice import WebsocketDisconnectedError

app = Chalice(app_name='echo-server')
app.websocket_api.session = Session()
app.experimental_feature_flags.update([
    'WEBSOCKETS'
])

@app.on_ws_message()
def message(event):
    try:
        app.websocket_api.send(
            connection_id=event.connection_id,
            message=f'Message is: {event.body}',
        )
    except WebsocketDisconnectedError as e:
        pass

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
