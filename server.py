from flask import Flask, json, abort, request

tripSquadAPI = Flask(__name__)

@tripSquadAPI.route('/')
def homePage():

	return json.jsonify("Server is up.")

@tripSquadAPI.route('/account/create', methods=["POST"])
def createAccount():
	requestJson = request.get_json()
	if "name" not in requestJson or "emailAddress" not in requestJson:
		return json.jsonify("404 must include 'name' and 'emailAddress'")
 
	return json.jsonify("create Account endpoint.")

@tripSquadAPI.route('/account/<accountID>')
def getAccountInfo(accountID):

	return json.jsonify("account info endpoint")

@tripSquadAPI.route('/trip/create', methods=["POST"])
def createTrip():
	requestJson = request.get_json()

	if "tripName" not in requestJson or "accountIDs" not in requestJson:
		return json.jsonify("404 must include 'tripName' and 'accountIDs'")

	return json.jsonify("create trip endpoint")

@tripSquadAPI.route('/trip/<tripID>/addPurchase', methods=["POST"])
def addPurchase(tripID):

	return json.jsonify("add purchase endpoint")

@tripSquadAPI.route('/trip/<tripID>/getTotal')
def getTripTotal(tripID):

	return json.jsonify("get trip total endpoint")
