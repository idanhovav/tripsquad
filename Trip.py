import uuid
import datetime as dt
import db
import TripMember

class Trip:

    def __init__(self, accountIDs, tripName, tripDescription):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        tripMembers =  set([TripMember.TripMember(accountID, self.ID) for accountID in accountIDs])
        self.tripMemberIDs = [tripMember.ID for tripMember in tripMembers]
        self.tripName = tripName
        self.tripDescription = tripDescription

    # Returns true on successful insertion
    def writeToDB(self):
        db.tripsByID[self.ID] = self
        success = getTripByID(self.ID) != None

        return success

    def includesAccount(self, accountID):
        tripMemberID = TripMember.getTripMemberID(accountID, self.ID)
        return tripMemberID in self.tripMemberIDs

def getTripByID(tripID):

    if tripID in db.tripsByID:
        return db.tripsByID[tripID]
    else:
        return None

def createTrip(accountIDs, tripName, tripDescription=None):
    newTrip = Trip(accountIDs, tripName, tripDescription)

    return newTrip if newTrip.writeToDB() else None
