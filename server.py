from flask import Flask, json, abort, request

import Account, Trip, Purchase, db

tripSquadAPI = Flask(__name__)

@tripSquadAPI.route('/')
def homePage():

	return json.jsonify("Server is up.")

@tripSquadAPI.route('/account/create', methods=["POST"])
def createAccount():
	requestParams = request.values
	if "name" not in requestParams or "emailAddress" not in requestParams:
		print("createAccount -- Required params not found in request")
		abort(400)
 
	newAccount = Account.Account(requestParams["name"], requestParams["emailAddress"])
	print("createAccount -- new Account: ID: %s, name: %s, email: %s" % (newAccount.AccountID, newAccount.name, newAccount.email))

	if not Account.getAccountByID(newAccount.AccountID):
		print("createAccount -- failure in db insertion")
		abort(500)
	response = {"newAccountID" : newAccount.AccountID}
	return json.jsonify(response)

@tripSquadAPI.route('/account/<accountID>')
def getAccountInfo(accountID):

	account = Account.getAccountByID(accountID)
	return json.jsonify("Account ID: %s, Name: %s, Email: %s" % account.AccountID, account.name, account.email)

@tripSquadAPI.route('/trip/create', methods=["POST"])
def createTrip():
	requestJson = request.get_json()

	if "tripName" not in requestJson or "accountIDs" not in requestJson:
		return json.jsonify("404 must include 'tripName' and 'accountIDs'")

	return json.jsonify("create trip endpoint")

@tripSquadAPI.route('/trip/<tripID>/addPurchase', methods=["POST"])
def addPurchase(tripID):

	requestJson = request.get_json()
	if "purchaseAmount" not in requestJson or "accountID" not in requestJson:
		return json.jsonify("404 must include 'purchaseAmount' and 'accountID'")


	return json.jsonify("add purchase endpoint")

@tripSquadAPI.route('/trip/<tripID>/getTotal')
def getTripTotal(tripID):

	return json.jsonify("get trip total endpoint")
