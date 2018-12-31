import datetime as dt
import db
import utils

class TripMember:
    def __init__(self, accountID, tripID):
        self.ID = getTripMemberID(accountID, tripID)
        self.timeStamp = str(dt.datetime.today())
        self.accountID = accountID
        self.tripID = tripID
        self.totalPurchaseAmount = 0
        db.tripMembersByID[self.ID] = self

def getTripMemberByID(tripMemberID):

    if tripMemberID in db.tripMembersByID:
        return db.tripMembersByID[tripMemberID]
    else:
        return None

def getTripAndAccountIDs(tripMemberID):

    return tripMemberID.split(utils.IDCharSeparator)

def getTripMemberID(accountID, tripID):

    return accountID + utils.IDCharSeparator + tripID

def updateTripMemberTotal(tripMemberID, purchaseAmount):
    tripMember = getTripMemberByID(tripMemberID)
    tripMember.totalPurchaseAmount += purchaseAmount
    return True
