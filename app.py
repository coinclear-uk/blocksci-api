import itertools
import blocksci
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
    chain = blocksci.Blockchain(settings.BLOCKSCI_CONFIG)
    address = chain.address_from_string(address_string)
    data['type'] = str(address.type)
    data['balance'] = address.balance()
    data['transactions']['first'] = str(address.first_tx.hash)
    data['transactions']['total'] = {}
    data['transactions']['total']['in'] = address.in_txes_count()
    data['transactions']['total']['out'] = address.out_txes_count()
    #data['equivalent'] = []
    #for address in address.equiv().addresses:
    #    if address.type not in [blocksci.address_type.nonstandard, blocksci.address_type.nulldata]:
    #        address_data = {'type': address.type, 'address': address.address_string}
    #        data['equivalent'].append(address_data)
    return json_success(data)


#@auth_basic(check)
@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/from/')
def address_transactions_from(address):
	return address_transactions_pagnated(True, address, 1)


#@auth_basic(check)
@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/from/<page:int>/')
def address_transactions_from(address,page):
	return address_transactions_pagnated(True, address, page)


#@auth_basic(check)
@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/to/')
def address_transactions_to(address):
	return address_transactions_pagnated(False, address, 1)


#@auth_basic(check)
@route('/address/<address:re:[13][a-km-zA-HJ-NP-Z1-9]{25,34}>/transactions/to/<page:int>/')
def address_transactions_to(address,page):
	return address_transactions_pagnated(False, address, page)


def address_transactions_pagnated(is_from, address_string, page):
    chain = blocksci.Blockchain(settings.BLOCKSCI_CONFIG)
    try:
        address = chain.address_from_string(address_string)
    except AttributeError:
        return json_not_found()
    if is_from:
    	transactions_as_list = list(address.out_txes)
    else:
        transactions_as_list = list(address.in_txes)
    start = (page - 1) * settings.RESULTS_PER_PAGE
    end = page * settings.RESULTS_PER_PAGE
    data = {
        'start': start,
        'end': end,
        'total': len(transactions_as_list),
        'result': []
    }
    for transaction in transactions_as_list[start:end]:
        t = {
            'hash': str(transaction.hash),
            'block': transaction.block_height,
            'timestamp': transaction.block_time.strftime("%H:%m %d/%m/%Y"),
            'fee': transaction.fee,
            'inputs': [],
            'outputs': [],
        }
        #if transaction.change_output is not None:
        #    t['change_address'] = str(transaction.change_output.address)
        for tx_input in transaction.inputs:
            input_data = {'address':tx_input.address.address_string,'value':in_bitcoins(tx_input.value)}
            t['inputs'].append(input_data)
        for tx_output in transaction.outputs:
            output_data = {'address':tx_output.address.address_string,'value':in_bitcoins(tx_output.value),'spent':tx_output.is_spent}
            t['outputs'].append(output_data)
        data['result'].append(t)
    return json_success(data)


def in_bitcoins(satoshis):
    return float(satoshis)/100000000


debug(settings.DEBUG)

run(server=settings.SERVER, host=settings.HOST, port=settings.PORT, reloader=settings.RELOAD)
