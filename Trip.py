import uuid
import datetime as dt
import db
import TripMember

class Trip:

    def __init__(self, tripName, tripDescription):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.tripMemberIDs = []
        self.tripName = tripName
        self.tripDescription = tripDescription

    # Returns true on successful insertion
    # dbFunction
    def writeToDB(self):
        db.tripsByID[self.ID] = self
        success = getTripByID(self.ID) != None

        return success

    def includesAccount(self, accountID):
        tripMemberID = TripMember.getTripMemberID(accountID, self.ID)
        return tripMemberID in self.tripMemberIDs

# dbFunction
def getTripByID(tripID):

    if tripID in db.tripsByID:
        return db.tripsByID[tripID]
    else:
        return None

def createTrip(accountIDs, tripName, tripDescription=None):
    newTrip = Trip(tripName, tripDescription)
    tripMembers = [TripMember.createTripMember(accountID, newTrip.ID) for accountID in accountIDs]
    if any([tripMember == None for tripMember in tripMembers]):
        TripMember.removeTripMembersFromDB(tripMembers) # to keep transaction atomic
        return None

    newTrip.tripMemberIDs = [tripMember.ID for tripMember in tripMembers]
    return newTrip if newTrip.writeToDB() else None
