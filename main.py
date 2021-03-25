# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


class Seat:
    def __init__(self, seatnumber, seattype):
        self.seatNumber = seatnumber
        self.seatType = seattype
        self.transactionID = None
        self.allotmentStatus = False

    def allot(self, ID):
        self.allotmentStatus = True
        self.transactionID = ID

    def isAvailable(self):
        return not self.allotmentStatus

    def print(self):
        print("Seat Number: " + self.seatNumber + ", Seat Type: " + self.seatType)

    def cancel(self):
        self.allotmentStatus = False
        self.transactionID = None


class Show:                                                 # keep separate balcony normal arrays if we can. add a construct from excel method
    def __init(self, starttime, endtime, name, nB, nN, priceB, priceN):
        self.startTime = starttime
        self.endTime = endtime
        self.name = name
        self.priceBalcony = priceB
        self.priceNormal = priceN
        self.seats = [Seat(x, 'Balcony' if x < nB else 'Normal') for x in
                      range(0, nB + nN)]  # seat numbers [0,nB-1] are balcony seats

    def showAvailableSeats(self):
        return [x for x in self.seats if x.isAvailable()]

    def percentageOccupied(self):                   #shorten this code
        balconies = 0
        nB = 0
        normals = 0
        nN = 0
        for x in self.seats:
            if x.seatType is 'Balcony':
                nB += 1
                if x.isAvailable():
                    balconies += 1
            else:
                nN += 1
                if x.isAvailable():
                    normals += 1

        return [balconies, nB, normals,nN]                                  # if we can diverge from srs prototypes, nahi toh calculate karke print kardo


class Auditorium:
    def __init__(self):
        self.shows = []

    def addshow(self, show):
        self.shows.append(show)

    def findShow(self, name):
        return [x for x in self.shows if x.name is name]



class Employee:
    def __init__(self, ID, passw):
        self.loginID = ID
        self.password = passw


class ShowManager(Employee):
    pass


class AuditClerk(Employee):
    pass


class SalesPerson(Employee):
    def __init__(self, ID, passw, rate):
        self.transactions = []
        self.commission = 0
        self.commissionRate = rate
        Employee.__init__(self, ID, passw)

    # def getTransactions(self,ledgy):                              #redundant function?
    #     ledgy.printTransactions(self.transactions)

    def addTransaction(self, ID):
        self.transactions.append(ID)


class Transaction:
    def __init__(self, price, ID, name, date):
        self.value = price
        self.transactionID = ID
        self.name = name
        self.date = date

    def print(self):
        print("Transaction ID: ",self.transactionID)
        print(self.name)
        print("Amount (Credited): ",self.value)
        print("Date: ",self.date)

class Ledger:
    def __init(self):
        self.transactions = {}         #dictionary : transactionID -> transaction

    def printTransactions(self,transactionIDs):                          # return type differs from SRS prototype
        return [self.transactions[x] for x in transactionIDs]
        # for x in transactionIDs:
        #     self.transactions[x].print()

    def addExpense(self,name,value,date):
        self.transactions[name] = Transaction(value,len(self.transactions),name,date)


class ManagementSystem:
    def __init__(self):








# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
