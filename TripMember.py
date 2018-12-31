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

    def writeToDB(self):
        db.tripMembersByID[self.ID] = self
        success = getTripMemberByID(self.ID) != None

        return success

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

def createTripMember(accountID, tripID):
    newTripMember = TripMember(accountID, tripID)

    return newTripMember if newTripMember.writeToDB() else None

def removeTripMembersFromDB(tripMembers):
    for tripMember in tripMembers:
        if tripMember.ID in db.tripMembersByID:
            del db.tripMembersByID[tripMember.ID]
