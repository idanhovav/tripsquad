import uuid
import datetime as dt
import db
import utils
import TripMember

class Purchase:

    def __init__(self, tripMemberID, purchaseAmount, tag = "", description = ""):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.tripMemberID = tripMemberID
        [self.accountID, self.tripID] = TripMember.getTripAndAccountIDs(tripMemberID)
        self.purchaseAmount = purchaseAmount
        self.tag = tag
        self.description = description

        db.purchasesByID[self.ID] = self
        db.tripMembersByID[self.tripMemberID].totalPurchaseAmount += self.purchaseAmount

def getPurchaseByID(purchaseID):

    if purchaseID in db.purchasesByID:
        return db.purchasesByID[purchaseID]
    else:
        return None

def getPurchasesByTripID(tripID):

    return [purchase for purchase in db.purchasesByID.values() if purchase.tripID == tripID]
