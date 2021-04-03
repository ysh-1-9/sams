# pupupu
# monal trying to make changes to ysh/sams/master/main.py
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from datetime import datetime

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


class Show:  # keep separate balcony normal arrays if we can. add a construct from excel method
    def __init__(self, starttime, endtime,audiNum, name, nB, nN, priceB, priceN):
        self.startTime = starttime                                                      #DISPALY ERROR MESSSAGE IF START TIME> END TIME
        self.endTime = endtime
        self.name = name
        self.priceBalcony = priceB                                                      ##MUST BE VALID NUMBERS
        self.priceNormal = priceN
        self.seats = [Seat(x, 'Balcony' if x < nB else 'Normal') for x in                 #CHANGE TO BSEATS AND NSEATS
                      range(0, nB + nN)]  # seat numbers [0,nB-1] are balcony seats
        #self.nseats =                                                                          #EDIT       
        self.audino = audiNum

    def showAvailableSeats(self):  # differs from SRS prototype
        return [x for x in self.seats if x.isAvailable()]

    def percentageOccupied(self):  # shorten this code
        balconies = 0
        nB = 0
        normals = 0
        nN = 0
        for x in self.seats:
            if x.seatType == 'Balcony':
                nB += 1
                if x.isAvailable():
                    balconies += 1
            else:
                nN += 1
                if x.isAvailable():
                    normals += 1

        return [balconies, nB, normals, nN]  # if we can diverge from srs prototypes, nahi toh calculate karke print kardo



class Auditorium:
    def __init__(self):
        self.shows = []
        # read excel file & create shows list

    def addshow(self, show):
        self.shows.append(show)
        # update shows list

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
        # create file
        # self.df = pd.dataframe("hdkf.csv")

    # def getTransactions(self,ledgy):                              #redundant function? prototype differs from SRS
    #     ledgy.printTransactions(self.transactions)

    def insertTransaction(self, ID):
        self.transactions.append(ID)
        # update excel file


class Transaction:
    def __init__(self, price, ID, name, date):
        self.value = price
        self.transactionID = ID
        self.name = name
        self.date = date
        # update excel file

    def print(self):
        print("Transaction ID: ", self.transactionID)
        print(self.name)
        print("Amount (Credited): ", self.value)
        print("Date: ", self.date)


class Ledger:
    def __init__(self):
        self.transactions = {}  # dictionary : transactionID -> transaction
        self.showRevenue = {}  # time adn audiNo as keys
        # name and revenue generated as values
        # read excel file + initialize trassactions dictionary

    def printTransactions(self, transactionIDs):  # return type differs from SRS prototype
        return [self.transactions[x] for x in transactionIDs]
        # for x in transactionIDs:
        #     self.transactions[x].print()

    def addExpense(self, name, value, date):  # prototype differs from SRS
        self.transactions[name] = Transaction(value, len(self.transactions), name, date)
        # update excel file


class ManagementSystem:
    def __init__(self):
        self.auditoriums = Auditorium()  # SRS says auditorium array
        self.ledger = Ledger()
        self.employees = []
        # read excel file + initialize employee array

    '''def read(self, ledgerfile, loginfile, auditoriumfile):  # method not in SRS
        pass  # TBD'''

    def createshow(self, frame, name, audiN, start, end, nBalcony, nNormal, priceBalc, priceNormal):
        newf = Frame(frame, bg = "#ffd6d6")
        newf.place(relx = 0.05, rely = 0.14, relwidth = 0.9, relheight = 0.81)
        show = Show(name,audiN,datetime.strptime(start, '%m/%d/%y %H:%M'),datetime.strptime(end, '%m/%d/%y %H:%M'),int(nBalcony),int(nNormal),int(priceBalc),int(priceNormal))
        for x in self.auditoriums.shows:
            if x.name is name and x.startTime is show.startTime and x.audino is audiN:
                label = Label(newf, text="Show Exists Already", bg="#ffd6d6")
                label.place(relx=0, rely=0, relheight=1, relwidth=1)
                return
        self.auditoriums.addshow(show)
        label = Label(newf, text="Show Added", bg="#ffd6d6")
        label.place(relx=0, rely=0, relheight=1, relwidth=1)
        return


    def createSP(self, frame, loginID, password, rate):
        # create a new window saying create hua ya nahi
        frame.destroy()

    def login(self, ID, passw):  # prototype differs from SRS
        for emp in self.employees:
            if emp.loginID is ID and emp.password is passw:
                return True
        # read excel file

    def ShowManagerMenu(self):
        root = Tk()

        canvas = Canvas(root, height=300, width=750)
        canvas.pack()

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        def createshowUI():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            label1 = Label(newframe, text="Name:", bg="#ffd6d6")
            label1.place(relx=0.05, rely=0.14, relwidth=0.15, relheight=0.12)

            entry1 = Entry(newframe)
            entry1.place(relx=0.25, rely=0.14, relwidth=0.2, relheight=0.12)

            label2 = Label(newframe, text="Auditorium Number:", bg="#ffd6d6")
            label2.place(relx=0.5, rely=0.14, relwidth=0.2, relheight=0.12)

            entry2 = Entry(newframe)
            entry2.place(relx=0.75, rely=0.14, relwidth=0.2, relheight=0.12)

            label3 = Label(newframe, text="Start Time:", bg="#ffd6d6")
            label3.place(relx=0.05, rely=0.30, relwidth=0.15, relheight=0.12)

            entry3 = Entry(newframe)
            entry3.place(relx=0.25, rely=0.30, relwidth=0.2, relheight=0.12)

            label4 = Label(newframe, text="End Time:", bg="#ffd6d6")
            label4.place(relx=0.55, rely=0.30, relwidth=0.15, relheight=0.12)

            entry4 = Entry(newframe)
            entry4.place(relx=0.75, rely=0.30, relwidth=0.2, relheight=0.12)

            label5 = Label(newframe, text="Balcony Seats:", bg="#ffd6d6")
            label5.place(relx=0.05, rely=0.46, relwidth=0.15, relheight=0.12)

            entry5 = Entry(newframe)
            entry5.place(relx=0.25, rely=0.46, relwidth=0.2, relheight=0.12)

            label6 = Label(newframe, text="Normal Seats:", bg="#ffd6d6")
            label6.place(relx=0.55, rely=0.46, relwidth=0.15, relheight=0.12)

            entry6 = Entry(newframe)
            entry6.place(relx=0.75, rely=0.46, relwidth=0.2, relheight=0.12)

            label7 = Label(newframe, text="Price Balcony:", bg="#ffd6d6")
            label7.place(relx=0.05, rely=0.66, relwidth=0.15, relheight=0.12)

            entry7 = Entry(newframe)
            entry7.place(relx=0.25, rely=0.66, relwidth=0.2, relheight=0.12)

            label8 = Label(newframe, text="Price Normal:", bg="#ffd6d6")
            label8.place(relx=0.55, rely=0.66, relwidth=0.15, relheight=0.12)

            entry8 = Entry(newframe)
            entry8.place(relx=0.75, rely=0.66, relwidth=0.2, relheight=0.12)

            button1 = Button(newframe, text="Create",
                             command=lambda: self.createshow(newframe, entry1.get(), entry2.get(), entry3.get(),
                                                             entry4.get(), entry5.get(), entry6.get(), entry7.get(),
                                                             entry8.get()))
            button1.place(relx=0.45, relwidth=0.1, rely=0.86, relheight=0.1)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        def createSPUI():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            label1 = Label(newframe, text="Login ID:", bg="#ffd6d6")
            label1.place(relx=0.05, rely=0.235, relwidth=0.425, relheight=0.12)

            entry1 = Entry(newframe)
            entry1.place(relx=0.525, rely=0.235, relwidth=0.425, relheight=0.12)

            label2 = Label(newframe, text="Password:", bg="#ffd6d6")
            label2.place(relx=0.05, rely=0.44, relwidth=0.425, relheight=0.12)

            entry2 = Entry(newframe)
            entry2.place(relx=0.525, rely=0.44, relwidth=0.425, relheight=0.12)

            label3 = Label(newframe, text="Commission Rate:", bg="#ffd6d6")
            label3.place(relx=0.05, rely=0.645, relwidth=0.425, relheight=0.12)

            entry3 = Entry(newframe)
            entry3.place(relx=0.525, rely=0.645, relwidth=0.425, relheight=0.12)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

            button1 = Button(newframe, text="Create",
                             command=lambda: self.createSP(newframe, entry1.get(), entry2.get(), entry3.get()))
            button1.place(relx=0.45, relwidth=0.1, rely=0.85, relheight=0.1)

        def schedule():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

            label1 = Label(newframe, text="Enter Auditorium Number:", bg="#ffd6d6")
            label1.place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.1)

            entry1 = Entry(newframe)
            entry1.place(relx=0.45, rely=0.2, relwidth=0.2, relheight=0.1)

            button1 = Button(newframe, text="View Schedule", command=lambda: display(entry1.get()))
            button1.place(relx=0.75, relwidth=0.2, rely=0.2, relheight=0.1)

            box = Frame(newframe, bg="#ffd6d6")
            box.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.6)

            def display(audi):
                listbox = Listbox(box)

                for x in self.auditoriums.shows:
                    if x.audino is audi:
                        listbox.insert(listbox.size() + 1, x.name + " from " + x.startTime.strftime("%c") + " to " + x.endTime.strftime("%c"))

                listbox.place(relx=0, rely=0, relheight=1, relwidth=1)

        def transactionHistory():
            pass

        def balanceSheet():
            pass

        button1 = Button(frame, text="Create a Show", command=createshowUI)
        button1.place(relx=0.05, rely=0.2, relwidth=0.425, relheight=0.2)

        button2 = Button(frame, text="Create a Sales Person Account", command=createSPUI)
        button2.place(relx=0.525, rely=0.2, relwidth=0.425, relheight=0.2)

        button3 = Button(frame, text="View Auditorium Schedule", command=schedule)
        button3.place(relx=0.05, relwidth=0.425, rely=0.45, relheight=0.2)

        button4 = Button(frame, text="View Sales Person Transaction History", command=transactionHistory)
        button4.place(relx=0.525, relwidth=0.425, rely=0.45, relheight=0.2)

        button5 = Button(frame, text="View Balance Sheet", command=balanceSheet)
        button5.place(relx=0.2875, relwidth=0.425, rely=0.7, relheight=0.2)

        button6 = Button(frame, text="Logout", command=root.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        root.mainloop()

        # to create employees with id and password
        # username must be unique
        # update excel file
        # add shows
        '''//starttime<end time
//audi should be empty
//no duplicates
//audi number should be valid'''

    def SalesPersonMenu(self):
        pass  # TBD

    # book-> update seat allotment excel files for the particular show

    def AuditClerkMenu(self):
        pass  # TBD

    def SpectatorMenu(self):  # differs from SRS
        pass  # TBD


sys = ManagementSystem()

sys.ShowManagerMenu()

# write save methods for shows, auditoriums, ledgers, employees. maybe add a filename field everywhere so you know
# where to save.

# Press the green button in the gutter to run the script.
