import datetime as dt
import db
import utils

class TripMember:
    def __init__(self, AccountID, TripID):
        self.TripMemberID = getTripMemberID(AccountID, TripID)
        self.timeStamp = str(dt.datetime.today())
        self.AccountID = AccountID
        self.TripID = TripID
        self.totalPurchaseAmount = 0
        db.tripMembersByID[self.TripMemberID] = self

def getTripAndAccountIDs(TripMemberID):

    return TripMemberID.split(utils.IDCharSeparator)

def getTripMemberID(AccountID, TripID):

    return AccountID + utils.IDCharSeparator + TripID
