#import blocksci
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

@route('/address/search/<address_string:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/')
#@auth_basic(check)
def address_search(address_string):
	data = {'transactions':{}}
	'''
	chain = blocksci.Blockchain(settings.BLOCKSCI_LOCATION)
	address = chain.address_from_string(address_string)
	data['type'] = address.type
	data['balance'] = address.balance()
	data['transactions']['first'] = address.first_tx
	data['transactions']['last'] = address.last_tx
	data['transactions']['total'] = {}
	data['transactions']['total']['in'] = address.in_txes_count()
	ata['transactions']['total']['out'] = address.out_txes_count()
	data['equivalent'] = []
	for equivalent_addresses in address.equiv():
		address_data = {'type':equivalent_addresses.type}
		if equivalent_addresses.type not in ['NonStandardAddress','OpReturn']
			address_data['address'] = equivalent_addresses.address_string
	'''
	return json_success(data)

@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/from/')
#@auth_basic(check)
def address_transactions_from(address,page):
	return json_success(address_transactions_from_pagnated(address_search,1))

@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/from/<page:int>/')
#@auth_basic(check)
def address_transactions_from(address,page):
	return json_success(address_transactions_from_pagnated(address_search,page))

def address_transactions_from_pagnated(address_string, page):
	'''
	chain = blocksci.Blockchain(settings.BLOCKSCI_LOCATION)
	address = chain.address_from_string(address_string)
	data = []
	for transaction in address.in_txes():
		t = {
			'hash': transactions.hash,
			'block': transaction.block_height,
			'time_stamp': transaction.block_time.strftime("%H:%m %d/%m/%Y"),
			'fee': transaction.fee,
		}
		if t.change_output is not None:
			t['change_address'] = t.change_output.address
		for input in transaction.inputs:
			input_data = {'type':input.type}
			if input.type not in ['NonStandardAddress','OpReturn']:
				input_data['address'] = input.address_string
			t['inputs'] = input_data
		for output in transaction.outputs:
			output_data = {'type':output.type}
			if output.type not in ['NonStandardAddress','OpReturn']:
				output_data['address'] = output.address_string
			t['outputs'] = output_data
		data.append(t)
	'''
	pass

debug(settings.DEBUG)

run(server=settings.SERVER, host=settings.HOST, port=settings.PORT, reloader=settings.RELOAD)
