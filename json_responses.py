from bottle import json_dumps, response

def json_success(data):
    return json_standard(200, 'success', data)

def json_created():
    return json_standard(201, 'success')

def json_moved(url):
    return json_standard(301, 'redirect', {'url': url})

def json_bad_request(reason):
    return json_standard(400, 'bad request', {'reason': reason})

def json_unauthorized():
    return json_standard(401, 'unauthorized')

def json_forbidden():
    return json_standard(403, 'forbidden')

def json_not_found():
    return json_standard(404, 'not found')

def json_error():
    return json_standard(500, 'server error')

def json_standard(status, message, data=[]):
    response.status = status
    response.set_header('Content-type','application/json')
    return json_dumps({
        'status': status,
        'message': message,
        'data': data
    })
