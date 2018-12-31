import requests
import unittest
from unittest import TestCase
import json
import subprocess
import time
import sys

global sleepTimer
sleepTimer = 2 # seconds

serverURL = "http://0.0.0.0:5000"

testAccounts = [
    {"name": "Dan", "emailAddress": "dan@dan.com", "password": "abcdef"},
    {"name": "Bob", "emailAddress": "bob@bob.com", "password": "123456"},
    {"name": "Jim", "emailAddress": "jim@jim.com", "password": "nopqrs"}
]

class TestAPI(TestCase):
    serverProcess = None

    @classmethod
    def setUpClass(cls):
        print("Starting API server")
        # start the API server
        TestAPI.serverProcess = subprocess.Popen("flask run --host=0.0.0.0".split())
        # wait for server to initialize before running tests
        time.sleep(sleepTimer)
        # check it's running
        print(requests.get(serverURL + "/").text)

    @classmethod
    def tearDownClass(cls):
        if TestAPI.serverProcess:
            print("Terminating API server")
            TestAPI.serverProcess.terminate()

    def testCreateAccount(self):
        for i in range(len(testAccounts)):
            testAccount = testAccounts[i]
            accountInfo = self.createAccount(testAccount)
            self.assertTrue(accountInfo["name"] == testAccount["name"])
            self.assertTrue(accountInfo["emailAddress"] == testAccount["emailAddress"])
            self.assertTrue(accountInfo["accountID"])

    def testCreateTrip(self):
        accountIDs = [self.createAccount(account)["accountID"] for account in testAccounts[0:2]]
        password = testAccounts[0]["password"]
        tripID = self.createTrip(accountIDs, password, "testCreateTrip")
        self.assertTrue(tripID)

    def testAddPurchase(self):
        accountIDs = [self.createAccount(account)["accountID"] for account in testAccounts]
        tripCreatorPassword = testAccounts[0]["password"]
        tripID = self.createTrip(accountIDs, tripCreatorPassword, "testAddPurchase")

        for i in range(len(testAccounts)):
            testAccount = testAccounts[i]
            password = testAccount["password"]
            purchaseID = self.addPurchase(accountIDs[i], tripID, password, 10**i, "purchase" + str(i))
            self.assertTrue(purchaseID)

    def testGetTripTotal(self):
        accountIDs = [self.createAccount(account)["accountID"] for account in testAccounts]

        tripCreatorPassword = testAccounts[0]["password"]
        tripID = self.createTrip(accountIDs, tripCreatorPassword, "testAddPurchase")

        for i in range(len(testAccounts)):
            testAccount = testAccounts[i]
            password = testAccount["password"]
            purchaseID = self.addPurchase(accountIDs[i], tripID, password, 10**i, "purchase" + str(i))
            self.assertTrue(purchaseID)

        getTripTotalParams = {"accountID": accountIDs[0], "password": testAccounts[0]["password"]}
        getTripTotalJson = self.sendRequest("/trip/" + tripID + "/getTotal", getTripTotalParams, ["total"])
        tripTotal = getTripTotalJson["total"]
        self.assertTrue(tripTotal == 111)

    def createAccount(self, params):
        createAccountJson = self.sendRequest("/account/create", params, ["accountID"])
        newAccountID = createAccountJson["accountID"]

        getAccountInfoJson = self.sendRequest("/account/" + newAccountID + "/info", params, ["name", "emailAddress", "accountID"])
        return getAccountInfoJson

    def createTrip(self, accountIDs, password, tripName):
        tripMemberAccountIDs = ",".join(accountIDs)
        params = {"creatorAccountID": accountIDs[0], 
            "creatorAccountPassword": password, 
            "tripName": tripName, 
            "tripMemberAccountIDs": tripMemberAccountIDs}
        createTripJson = self.sendRequest("/trip/create", params, ["tripID"])
        tripID = createTripJson["tripID"]
        self.assertTrue(tripID)
        return tripID

    def addPurchase(self, accountID, tripID, password, amount, description):
        params = {"purchaserAccountID": accountID,
            "purchaserAccountPassword": password, 
            "purchaseAmount": amount, 
            "description": description}

        addPurchaseJson = self.sendRequest("/trip/" + tripID + "/addPurchase", params, ["purchaseID"])
        purchaseID = addPurchaseJson["purchaseID"]
        self.assertTrue(purchaseID)
        return purchaseID

    def checkResponseJson(self, responseJson, expectedResponseKeys):

        self.assertTrue(all([key in responseJson for key in expectedResponseKeys]))

    def sendRequest(self, path, data, expectedResponseKeys):
        receivedResponse = requests.post(serverURL + path, data=data)
        self.assertTrue(receivedResponse.status_code == 200)
        responseJson = receivedResponse.json()
        self.checkResponseJson(responseJson, expectedResponseKeys)
        return responseJson

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sleepTimer = int(sys.argv[1])
    unittest.main(argv=[sys.argv[0]])
