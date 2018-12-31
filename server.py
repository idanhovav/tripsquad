from flask import Flask, json, abort, request

import Account, Trip, TripMember, Purchase

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
    password = requestParams["password"] if "password" in requestParams else None

    newAccount = Account.Account(requestParams["name"], requestParams["emailAddress"], password)
    tripSquadAPI.logger.info("createAccount -- new Account: ID: %s, name: %s, email: %s" % (newAccount.ID, newAccount.name, newAccount.email))

    if not Account.getAccountByID(newAccount.ID):
        tripSquadAPI.logger.error("createAccount -- failure in db insertion")
        abort(500)
    response = {"accountID" : newAccount.ID}
    return json.jsonify(response)

@tripSquadAPI.route('/account/<accountID>/info')
def getAccountInfo(accountID):

    account = Account.getAccountByID(accountID)
    if not account:
        tripSquadAPI.logger.error("getAccountInfo -- accountID %s not found" % accountID)
        abort(500)

    tripSquadAPI.logger.info("Account ID: %s, Name: %s, Email: %s" % (account.ID, account.name, account.email))
    accountInfo = {"accountID" : account.ID, "name": account.name, "emailAddress": account.email}
    return json.jsonify(accountInfo)

# TODO: add better auth for trip creation
@tripSquadAPI.route('/trip/create', methods=["POST"])
def createTrip():
    expectedParams = ["creatorAccountID", "creatorAccountPassword", "tripName", "tripMemberAccountIDs"]
    if not utils.hasExpectedParams(expectedParams, request):
        tripSquadAPI.logger.error("createTrip -- Required params not found in request")
        abort(400)

    requestParams = request.values
    creatorAccountID = requestParams["creatorAccountID"]
    creatorPassword = requestParams["creatorAccountPassword"]
    if not Account.validateAccount(creatorAccountID, creatorPassword):
        tripSquadAPI.logger.error("createTrip -- %s User not validated" % creatorAccountID)
        abort(400)
    tripName = requestParams["tripName"]
    tripMemberAccountIDs = requestParams["tripMemberAccountIDs"].split(",")
    newTrip = Trip.Trip(tripMemberAccountIDs, tripName=tripName)

    if not Trip.getTripByID(newTrip.ID):
        tripSquadAPI.logger.error("createTrip -- failure in db insertion")
        abort(500)
    response = {"tripID": newTrip.ID}
    return json.jsonify(response)

# TODO add some authorization or limitation to who can reach this endpoint
@tripSquadAPI.route('/trip/<tripID>/addPurchase', methods=["POST"])
def addPurchase(tripID):
    expectedParams = ["purchaserAccountID", "purchaseAmount"]
    if not utils.hasExpectedParams(expectedParams, request):
        tripSquadAPI.logger.error("addPurchase -- Required params not found in request")
        abort(400)

    trip = Trip.getTripByID(tripID)
    if not trip:
        tripSquadAPI.logger.error("addPurchase -- %s trip not validated" % tripID)
        abort(400)

    requestParams = request.values
    purchaseAmountStr = requestParams["purchaseAmount"]
    purchaseAmount = 0
    try:
        purchaseAmount = int(purchaseAmountStr)
    except ValueError:
        tripSquadAPI.logger.error("addPurchase -- %s purchaseAmount not valid" % purchaseAmountStr)
        abort(400)

    purchaserAccountID = requestParams["purchaserAccountID"]
    purchaseDescription = requestParams["description"] if "description" in requestParams else None

    tripMemberID = TripMember.getTripMemberID(purchaserAccountID, tripID)

    if not tripMemberID in trip.tripMemberIDs:
        tripSquadAPI.logger.error("addPurchase -- %s ID not validated" % tripMemberID)
        abort(400)

    newPurchase = Purchase.Purchase(tripMemberID, purchaseAmount, description=purchaseDescription)

    if not Purchase.getPurchaseByID(newPurchase.ID):
        tripSquadAPI.logger.error("addPurchase -- failure in db insertion")
        abort(500)

    response = {"purchaseID": newPurchase.ID}
    return json.jsonify(response)

@tripSquadAPI.route('/trip/<tripID>/getTotal')
def getTripTotal(tripID):

    trip = Trip.getTripByID(tripID)
    if not trip:
        tripSquadAPI.logger.error("getTripTotal -- %s trip not validated" % tripID)
        abort(400)

    tripPurchases = Purchase.getPurchasesByTripID(trip.ID)
    # TODO: totalPurchasesByPerson = Purchases.getPurchasesByPerson(totalPurchases)
    totalPurchaseSum = sum([int(purchase.purchaseAmount) for purchase in tripPurchases])

    response = {"tripID": tripID, "total": totalPurchaseSum}

    return json.jsonify(response)
