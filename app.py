from bottle import auth_basic, json_dumps, debug, error, response, route, install, run, HTTPError, HTTPResponse
from json_responses import *
import settings


def check(user, password):
	if user == settings.USER and password == settings.PASS:
		return True
	return False

@error(401)
def view_403(code):
	return json_unauthorized()

@error(403)
def view_403(code):
	return json_forbidden()

@error(404)
def view_404(code):
	return json_not_found()

@route('/address/search/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>')
#@auth_basic(check)
def address_search(address):
	return json_success('address found')

debug(settings.DEBUG)

run(server=settings.SERVER, host=settings.HOST, port=settings.PORT, reloader=settings.RELOAD)
