from flask import Flask, json, abort, request

import Account, Trip, Purchase

import db, utils

tripSquadAPI = Flask(__name__)

@tripSquadAPI.route('/')
def homePage():

	return json.jsonify("Server is up.")

@tripSquadAPI.route('/account/create', methods=["POST"])
def createAccount():
	expectedParams = ["name", "emailAddress"]
	if not utils.hasExpectedParams(expectedParams, request):
		tripSquadAPI.logger.error("createAccount -- Required params not found in request")
		abort(400)
 
	requestParams = request.values
	newAccount = Account.Account(requestParams["name"], requestParams["emailAddress"])
	tripSquadAPI.logger.info("createAccount -- new Account: ID: %s, name: %s, email: %s" % (newAccount.AccountID, newAccount.name, newAccount.email))

	if not Account.getAccountByID(newAccount.AccountID):
		tripSquadAPI.logger.error("createAccount -- failure in db insertion")
		abort(500)
	response = {"accountID" : newAccount.AccountID}
	return json.jsonify(response)

@tripSquadAPI.route('/account/<accountID>/info')
def getAccountInfo(accountID):

	account = Account.getAccountByID(accountID)
	if not account:
		tripSquadAPI.logger.error("getAccountInfo -- accountID %s not found" % accountID)
		abort(500)

	tripSquadAPI.logger.info("Account ID: %s, Name: %s, Email: %s" % account.AccountID, account.name, account.email)
	accountInfo = {"accountID" : account.AccountID, "name": account.name, "emailAddress": account.email}
	return json.jsonify(accountInfo)

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
