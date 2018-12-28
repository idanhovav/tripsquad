class Purchase:

	def __init__(self, AccountID, TripID, purchaseAmount, tag = "", description = ""):
		self.PurchaseID = 12345678 # TODO: import GUID
		self.timeStamp = None # TODO: import time
		self.AccountID = AccountID
		self.TripID = TripID
		self.purchaseAmount = purchaseAmount
		self.tag = tag
		self.description = description
