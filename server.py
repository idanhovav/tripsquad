from flask import Flask, json, abort, request

import Account, Trip, TripMember, Purchase

import db, utils

tripSquadAPI = Flask(__name__)

@tripSquadAPI.route('/')
def homePage():

    return json.jsonify("Server is up.")

@tripSquadAPI.route('/account/create', methods=["POST"])
def createAccount():
    requiredParams = ["name", "emailAddress", "password"]
    if not utils.hasExpectedParams(requiredParams, request):
        tripSquadAPI.logger.error("createAccount -- Required params not found in request")
        abort(400)

    (accountName, accountEmail, accountPassword) = utils.parseParams(requiredParams, request)
    newAccount = Account.createAccount(accountName, accountEmail, accountPassword)

    if not newAccount:
        tripSquadAPI.logger.error("createAccount -- failure in db insertion")
        abort(500)

    tripSquadAPI.logger.info("createAccount -- new Account: ID: %s, name: %s, email: %s" % (newAccount.ID, newAccount.name, newAccount.email))
    response = {"accountID" : newAccount.ID}
    return json.jsonify(response)

@tripSquadAPI.route('/account/<accountID>/info', methods=["POST"])
def getAccountInfo(accountID):
    requiredParams = ["password"]
    if not utils.hasExpectedParams(requiredParams, request):
        tripSquadAPI.logger.error("getAccountInfo -- Required params not found in request")
        abort(400)

    [password] = utils.parseParams(requiredParams, request)
    print("%s" % password)
    if not Account.validateAccount(accountID, password):
        tripSquadAPI.logger.error("getAccountInfo -- Incorrect password given.")
        abort(400)

    account = Account.getAccountByID(accountID)
    if not account:
        tripSquadAPI.logger.error("getAccountInfo -- accountID %s not found" % accountID)
        abort(500)

    tripSquadAPI.logger.info("getAccountInfo -- Account ID: %s, Name: %s, Email: %s" % (account.ID, account.name, account.email))
    accountInfo = {"accountID" : account.ID, "name": account.name, "emailAddress": account.email}
    return json.jsonify(accountInfo)

# TODO: add better auth for trip creation
@tripSquadAPI.route('/trip/create', methods=["POST"])
def createTrip():
    expectedParams = ["creatorAccountID", "creatorAccountPassword", "tripName", "tripMemberAccountIDs"]
    if not utils.hasExpectedParams(expectedParams, request):
        tripSquadAPI.logger.error("createTrip -- Required params not found in request")
        abort(400)

    (creatorAccountID, creatorPassword, tripName, tripMemberAccountIDsStr) = utils.parseParams(expectedParams, request)
    tripMemberAccountIDs = tripMemberAccountIDsStr.split(",")

    if not Account.validateAccount(creatorAccountID, creatorPassword):
        tripSquadAPI.logger.error("createTrip -- %s User not validated" % creatorAccountID)
        abort(400)

    newTrip = Trip.createTrip(tripMemberAccountIDs, tripName=tripName)

    if not newTrip:
        tripSquadAPI.logger.error("createTrip -- failure in db insertion")
        abort(500)

    response = {"tripID": newTrip.ID}
    return json.jsonify(response)

# TODO add some authorization or limitation to who can reach this endpoint
@tripSquadAPI.route('/trip/<tripID>/addPurchase', methods=["POST"])
def addPurchase(tripID):
    requiredParams = ["purchaserAccountID", "purchaserAccountPassword", "purchaseAmount"]
    if not utils.hasExpectedParams(requiredParams, request):
        tripSquadAPI.logger.error("addPurchase -- Required params not found in request")
        abort(400)

    allParams = requiredParams + ["description"]
    (purchaserAccountID, purchaserAccountPassword, purchaseAmountStr, purchaseDescription) = utils.parseParams(allParams, request)
    purchaseAmount = 0
    try:
        purchaseAmount = int(purchaseAmountStr)
    except ValueError:
        tripSquadAPI.logger.error("addPurchase -- %s purchaseAmount not valid" % purchaseAmountStr)
        abort(400)

    if not Account.validateAccount(purchaserAccountID, purchaserAccountPassword):
        tripSquadAPI.logger.error("addPurchase -- %s User not validated" % purchaserAccountID)
        abort(400) 

    trip = Trip.getTripByID(tripID)
    if not trip:
        tripSquadAPI.logger.error("addPurchase -- %s trip not valid" % tripID)
        abort(400)

    if not trip.includesAccount(purchaserAccountID):
        tripSquadAPI.logger.error("addPurchase -- %s ID not validated" % purchaserAccountID)
        abort(400)

    tripMemberID = TripMember.getTripMemberID(purchaserAccountID, tripID)
    newPurchase = Purchase.createPurchase(tripMemberID, purchaseAmount, description=purchaseDescription)

    if not newPurchase:
        tripSquadAPI.logger.error("addPurchase -- failure in db insertion")
        abort(500)

    response = {"purchaseID": newPurchase.ID}
    return json.jsonify(response)

@tripSquadAPI.route('/trip/<tripID>/getTotal', methods=["POST"])
def getTripTotal(tripID):
    requiredParams = ["accountID", "password"]
    if not utils.hasExpectedParams(requiredParams, request):
        tripSquadAPI.logger.error("getTripTotal -- Required params not found in request")
        abort(400)

    (accountID, password) = utils.parseParams(requiredParams, request)

    if not Account.validateAccount(accountID, password):
        tripSquadAPI.logger.error("getTripTotal -- Incorrect password given.")
        abort(400)

    trip = Trip.getTripByID(tripID)
    if not trip:
        tripSquadAPI.logger.error("getTripTotal -- %s trip not validated" % tripID)
        abort(400)

    if not trip.includesAccount(accountID):
        tripSquadAPI.logger.error("addPurchase -- %s ID not validated" % accountID)
        abort(400)

    tripPurchases = Purchase.getPurchasesByTripID(trip.ID)
    # TODO: totalPurchasesByPerson = Purchases.getPurchasesByPerson(totalPurchases)
    totalPurchaseSum = sum([int(purchase.purchaseAmount) for purchase in tripPurchases])

    response = {"tripID": tripID, "total": totalPurchaseSum}

    return json.jsonify(response)
