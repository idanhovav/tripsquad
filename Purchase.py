import uuid
import datetime as dt
import db
import utils
import TripMember

class Purchase:

    def __init__(self, tripMemberID, purchaseAmount, tag, description):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.tripMemberID = tripMemberID
        [self.accountID, self.tripID] = TripMember.getTripAndAccountIDs(tripMemberID)
        self.purchaseAmount = purchaseAmount
        self.tag = tag
        self.description = description

        db.purchasesByID[self.ID] = self

    # Returns true on successful insertion
    # dbFunction
    def writeToDB(self):
        db.purchasesByID[self.ID] = self
        success = getPurchaseByID(self.ID) != None

        return success

# dbFunction
def getPurchaseByID(purchaseID):

    if purchaseID in db.purchasesByID:
        return db.purchasesByID[purchaseID]
    else:
        return None

# dbFunction
def removePurchaseFromDB(purchaseID):
    if purchaseID in db.purchasesByID:
        del db.purchasesByID[purchaseID]

# dbFunction
def getPurchasesByTripID(tripID):

    return [purchase for purchase in db.purchasesByID.values() if purchase.tripID == tripID]

def createPurchase(tripMemberID, purchaseAmount, tag=None, description=None):
    newPurchase = Purchase(tripMemberID, purchaseAmount, tag, description)

    if not newPurchase.writeToDB():
        return None

    if not TripMember.updateTripMemberTotal(tripMemberID, purchaseAmount):
        removePurchaseFromDB(newPurchase.ID) # to keep transaction atomic
        return None

    return newPurchase

