class Trip:

	def __init__(self, AccountIDs, PurchaseIDs = [], tripName="", tripDescription=""):
		self.TripID = 12345678 # TODO: import GUID
		self.timeStamp = None # TODO: import time
		self.AccountIDs = list(set(AccountIDs)) # no repeats
		self.PurchaseIDs = list(set(PurchaseIDs)) # no repeats
		self.tripName = tripName
		self.tripDescription = tripDescription
