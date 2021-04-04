# pupupu
# monal trying to make changes to ysh/sams/master/main.py
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import datetime
from functools import partial
from tkinter import *
from tkcalendar import DateEntry

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
    def __init__(self, starttime, endtime, audiNum, name, nB, nN, priceB, priceN):
        self.startTime = starttime  # DISPALY ERROR MESSSAGE IF START TIME> END TIME
        self.endTime = endtime
        self.name = name
        self.priceBalcony = priceB  ##MUST BE VALID NUMBERS
        self.priceNormal = priceN
        self.seats = [Seat(x, 'Balcony' if x < nB else 'Normal') for x in  # CHANGE TO BSEATS AND NSEATS
                      range(0, nB + nN)]  # seat numbers [0,nB-1] are balcony seats
        # self.nseats =                                                                          #EDIT
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
                if not x.isAvailable():
                    balconies += 1
            else:
                nN += 1
                if not x.isAvailable():
                    normals += 1

        return 100*(balconies+normals)/float(nB+nN) # if we can diverge from srs prototypes, nahi toh calculate karke print kardo


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
        return True
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

        # 01/01/21 00:00

        newf = Frame(frame, bg="#ffd6d6")
        newf.place(relx=0.05, rely=0.14, relwidth=0.9, relheight=0.81)
        show = Show(datetime.strptime(start, '%m/%d/%y %H:%M'), datetime.strptime(end, '%m/%d/%y %H:%M'), audiN, name,
                    int(nBalcony), int(nNormal), int(priceBalc), int(priceNormal))
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
        sp = SalesPerson(loginID, password, rate)
        newf = Frame(frame, bg="#ffd6d6")
        newf.place(relx=0.05, rely=0.14, relwidth=0.9, relheight=0.81)

        for x in self.employees:
            if x.loginID is loginID:
                label = Label(newf, text="Login ID taken. Please try again", bg="#ffd6d6")
                label.place(relx=0, rely=0, relheight=1, relwidth=1)
                return

        self.employees.append(sp)
        #save employee to excel
        label = Label(newf, text="Account Created", bg="#ffd6d6")
        label.place(relx=0, rely=0, relheight=1, relwidth=1)


    def loginUI(self, root):  # prototype differs from SRS

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button6 = Button(frame, text="Go Back", command=frame.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        label1 = Label(frame, text="Login ID:", bg="#ffd6d6")
        label1.place(relx = 0.05, rely = 0.25, relwidth=0.2, relheight= 0.15)

        entry1 = Entry(frame)
        entry1.place(relx = 0.35, rely = 0.25, relwidth = 0.6, relheight = 0.15)

        label2 = Label(frame, text="Password", bg="#ffd6d6")
        label2.place(relx = 0.05, rely = 0.5, relwidth=0.2, relheight= 0.15)

        entry2 = Entry(frame)
        entry2.place(relx=0.35, rely=0.5, relwidth=0.6, relheight=0.15)

        def login(ID, passw):
            for emp in self.employees:
                if emp.loginID is ID and emp.password is passw:
                    if isinstance(emp, SalesPerson):
                        self.SalesPersonMenu(root)
                        return
                    elif isinstance(emp, AuditClerk):
                        self.AuditClerkMenu(root)
                        return
                    else:
                        self.ShowManagerMenu(root)
                        return

            print("invalid login")


        button1 = Button(frame, text = 'Login', command = lambda: login(str(entry1.get()), str(entry2.get())))
        button1.place(relx = 0.45, rely = 0.75, relwidth = 0.1, relheight=0.15)




    def homeUI(self):
        root = Tk()

        canvas = Canvas(root, height=300, width=750)
        canvas.pack()

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button1 = Button(frame, text='Employee', command = lambda: self.loginUI(root))
        button1.place(relx = 0.3, rely = 0.4, relwidth = 0.1, relheight = 0.2)

        button2 = Button(frame, text = 'Spectator', command = lambda: self.SpectatorMenu(root))
        button2.place(relx = 0.6, rely = 0.4, relwidth = 0.1, relheight = 0.2)

        root.mainloop()

    def ShowManagerMenu(self, root):
        print('Show manager menu called')
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
                listbox.insert(1, "Name" + " " * 36 + "Start Time" + " " * 30 + "End Time"+" "*32+"Percentage occupied")
                for x in self.auditoriums.shows:
                    if x.audino is audi:
                        listbox.insert(listbox.size() + 1,
                                       x.name + " " * (40 - len(x.name)) + x.startTime.strftime("%c") + " " * (
                                                   40 - len(x.startTime.strftime("%c"))) + x.endTime.strftime("%c")+ " "*(
                                                   40 - len(x.endTime.strftime("%c"))) + str(x.percentageOccupied()))

                listbox.place(relx=0, rely=0, relheight=1, relwidth=1)

        def transactionHistory():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

            label1 = Label(newframe, text="Select Sales Person:", bg="#ffd6d6")
            label1.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.1)

            listbox = Listbox(newframe)
            for x in self.employees:
                if isinstance(x,SalesPerson):
                    listbox.insert(listbox.size()+1, str(x.loginID))
            listbox.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.6)

            def getHistory(event):
                ID = str(listbox.get(listbox.curselection()))
                for x in self.employees:
                    if x.loginID is ID:
                        emp = x
                newnewframe = Frame(root, bg="#ffd6d6")
                newnewframe.place(relwidth=1, relheight=1)

                button6 = Button(newnewframe, text="Go Back", command=newnewframe.destroy)
                button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

                translist = Listbox(newnewframe)
                for x in emp.transactions:
                    y = self.ledger.transactions[x]
                    translist.insert(translist.size()+1, y.ID + " " + y.name + " " + y.date.strftime("%c") + " " + y.price)

                translist.place(relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.75)


            listbox.bind('<Double-1>', getHistory)


        def balanceSheet():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

            listbox = Listbox(newframe)
            #insert things to listbox from self.balancesheet
            listbox.place(relx = 0.05, relwidth = 0.9, rely = 0.2, relheight=0.75)

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

        button6 = Button(frame, text="Logout", command=frame.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)


        # to create employees with id and password
        # username must be unique
        # update excel file
        # add shows
        '''//starttime<end time
//audi should be empty
//no duplicates
//audi number should be valid'''

    def SalesPersonMenu(self, sproot):

        #canvas = Canvas(sproot, height=300, width=750)
        #canvas.pack()
        spframe = Frame(sproot, bg="#009933")
        spframe.place(relwidth=1, relheight=0.3)
        sproot.title("Welcome Salesperson")

        def spsearch_entry():
           e = (sptosearch.get())
           print(e)        
         
           spframe2 = Frame(sproot, bg = "#009933")
           spframe2.place(relwidth = 1, relheight = 0.7, rely = 0.3)
           
           #for i in showslistsp:        #get from excel
           #    ff
                    
           spshows = ('Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift', 'Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift', 'Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift')
           spshowslist = StringVar(value=spshows)

           splistbox = Listbox(spframe2, listvariable = spshowslist,  selectmode = 'extended', font = 'Garamond', activestyle = 'dotbox', bd = 5, relief = 'raised')
           splistbox.place(relx = 0.05, rely = 0.05, relheight = 0.85, relwidth = 0.9)

           
           spvscrollbar = Scrollbar(sproot)
           spvscrollbar.pack(side = RIGHT, fill = Y)

           sphscrollbar = Scrollbar(sproot, orient = HORIZONTAL)
           sphscrollbar.pack(side = BOTTOM, fill = X)

           splistbox.config(yscrollcommand = spvscrollbar.set, xscrollcommand = sphscrollbar.set)
           spvscrollbar.config(command = splistbox.yview)
           sphscrollbar.config(command = splistbox.xview)

           def spselected_item(event):
               value=str((splistbox.get(ANCHOR)))
               print (value)

               spframe3 = Frame(sproot, bg = "#009933")
               spframe3.place(relheight = 1, relwidth = 1)
               showname = showtiming = showauditorium = showdate = "abcd" #get from excel
               Label(spframe3, text = ("Show: " + showname + "\nDate: " + showdate+ "\nTiming: " + showtiming + "\nAuditorium number:" + showauditorium), bg = "#009933", font = ("Garamond", 12)).pack(padx = 5, pady = 5)
               
               def showseats(noofseats, num):
                   spcanvas = Canvas(sproot)
                   spcanvas.place(relx = 0.03, rely = 0.35, relheight = 0.6, relwidth = 0.94 )
                   x = 0.02
                   y = 0.02
                   statusnormal = ['booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked'] #from excel
                   statusbalcony = ['booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked'] #from excel
                   
                   if num == 0:
                       status = statusnormal
                       seattype = 'normal'
                   else:
                       status = statusbalcony
                       seattype = 'balcony'

                   for i in range(noofseats):
                   #if available = green, booked = red                   
                       if x >= 0.93:
                           x = 0.02
                           y = y + 0.12

                       if status[i] == 'booked': 
                           spbutton5 = Button(spcanvas, text = i+1 , bd = 5, bg = '#cc0000', command = partial(spbookseat, i, showname, showdate, showtiming, showauditorium, seattype, 0))
                           spbutton5.place(relx = x, rely = y, relheight = 0.1, relwidth = 0.05)

                       elif status[i] == 'unbooked':
                           spbutton5 = Button(spcanvas, text = i+1 , bd = 5, bg = '#009933', command = partial(spbookseat, i, showname, showdate, showtiming, showauditorium, seattype, 1))
                           spbutton5.place(relx = x, rely = y, relheight = 0.1, relwidth = 0.05)
                   
                       x = x + 0.07

               no_of_normals = 100  #from excel
               no_of_balcony = 20   #from excel
               spbutton1 = Button(spframe3, text = 'Normal seats' , bd = 5, command = partial(showseats, no_of_normals, 0))
               spbutton1.place(relx = 0.70, rely = 0.2, relheight = 0.1, relwidth = 0.12)

               spbutton2 = Button(spframe3, text = 'Balcony seats' , bd = 5, command = partial(showseats, no_of_balcony, 1))
               spbutton2.place(relx = 0.83, rely = 0.2, relheight = 0.1, relwidth = 0.12)

               
               def createseat(spframe4):
                    #make transaction and all, create/ cancel seat 
                    pass                  
                    

               def spbookseat(seatnumber, showname, showdate, showtiming, showaudi, seattype, num):
                   spframe4 = Frame(sproot, bg = "#009933")
                   spframe4.place(relheight = 1, relwidth = 1)

                   spbutton6 = Button(spframe4, text = 'Back' , bd = 5, command = spframe4.destroy)
                   spbutton6.place(relx = 0.03, rely = 0.05, relheight = 0.1, relwidth = 0.1)
                   if num == 0:
                       Label(spframe4, text =("Cancel seat number " + str(seatnumber + 1) + " for show " + showname), font = ("Garamond", 20), bg = "#009933").pack(padx = 25, pady = 100)
                       spbutton7 = Button(spframe4, text = 'Confirm Cancellation' , bd = 5, command = partial(createseat, spframe4))
                       spbutton7.place(relx = 0.4, rely = 0.4, relheight = 0.1, relwidth = 0.20)
                   
                   elif num ==1:
                       Label(spframe4, text =("Book seat number " + str(seatnumber + 1) + " for show " + showname), font = ("Garamond", 20), bg = "#009933").pack(padx = 25, pady = 100)
                       spbutton7 = Button(spframe4, text = 'Confirm Booking' , bd = 5, command = partial(createseat, spframe4))
                       spbutton7.place(relx = 0.4, rely = 0.4, relheight = 0.1, relwidth = 0.15)
                   
               
               def spdestroy():
                   spframe3.destroy()
                   spframe2.destroy()
                   spvscrollbar.destroy()
                   sphscrollbar.destroy()

               spbutton3 = Button(spframe3, text = 'Back' , bd = 5, command = spdestroy)
               spbutton3.place(relx = 0.03, rely = 0.05, relheight = 0.1, relwidth = 0.1)
               #
           splistbox.bind('<<ListboxSelect>>', spselected_item)

           return


        sptosearch = StringVar()

        spentry1 = Entry(spframe, textvariable = sptosearch, bd =5, width = 100, font = ("Garamond"))
        spentry1.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.66)

        spbutton1 = Button(spframe, text = 'Search', bd=5, command = spsearch_entry, font = ("Garamond"))
        spbutton1.place(relx = 0.75, rely = 0.5, relheight = 0.3, relwidth = 0.2)

        spbutton2 = Button(spframe, text = 'Logout' , bd = 5, command = spframe.destroy)
        spbutton2.place(relx = 0.05, rely = 0.1, relheight = 0.3, relwidth = 0.1)


    # book-> update seat allotment excel files for the particular show

    def AuditClerkMenu(self, root):

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button6 = Button(frame, text="Logout", command=frame.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        label1 = Label(frame, text="Enter expense name: ",bg="#ffd6d6")
        label1.place(relx = 0.05, relwidth=0.425, rely = 0.24, relheight=0.1)

        entry1 = Entry(frame)
        entry1.place(relx = 0.525, relwidth=0.425, rely = 0.24, relheight=0.1)

        label2 = Label(frame, text="Enter expense amount: ", bg="#ffd6d6")
        label2.place(relx=0.05, relwidth=0.425, rely=0.43, relheight=0.1)

        entry2 = Entry(frame)
        entry2.place(relx=0.525, relwidth=0.425, rely=0.43, relheight=0.1)

        label3 = Label(frame, text="Enter expense date: ", bg="#ffd6d6")
        label3.place(relx=0.05, relwidth=0.425, rely=0.62, relheight=0.1)

        entry3 = Entry(frame)
        entry3.place(relx=0.525, relwidth=0.425, rely=0.62, relheight=0.1)

        def save():
            if self.ledger.addExpense(entry1.get(), entry2.get(), datetime.strptime(entry3.get(), '%m/%d/%y %H:%M')):
                label4 = Label(frame, text=entry1.get()+ " Saved Successfully", bg="#ffd6d6")
                label4.place(relx = 0.55, relwidth = 0.4, rely = 0.81, relheight = 0.1)
            else:
                label4 = Label(frame, text="Could not be saved", bg="#ffd6d6")
                label4.place(relx=0.55, relwidth=0.4, rely=0.81, relheight=0.1)
            #add same for balance sheet

        button1 = Button(frame, text = "Save", command = save)
        button1.place(relx = 0.05, relwidth = 0.1, rely = 0.81, relheight=0.1)


    def SpectatorMenu(self, sproot):  # differs from SRS
        spframe = Frame(sproot, bg="#ffd6d6")
        spframe.place(relwidth=1, relheight=1)
        sproot.title("Welcome Spectator")

        def spsearch_entry():
           e = (sptosearch.get())
           print(e)        
         
           spframe2 = Frame(sproot, bg = "#009933")
           spframe2.place(relwidth = 1, relheight = 0.7, rely = 0.3)
           
           #for i in showslistsp:        #get from excel
           #    ff
           #get spshows from excel and show only those that match with e        
           spshows = ('Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift', 'Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift', 'Java', 'C#', 'C', 'C++', 'Python', 'Go', 'JavaScript', 'PHP', 'Swift')  #get from excel
           spshowslist = StringVar(value=spshows)

           splistbox = Listbox(spframe2, listvariable = spshowslist,  selectmode = 'extended', font = 'Garamond', activestyle = 'dotbox', bd = 5, relief = 'raised')
           splistbox.place(relx = 0.05, rely = 0.05, relheight = 0.85, relwidth = 0.9)

           
           spvscrollbar = Scrollbar(sproot)
           spvscrollbar.pack(side = RIGHT, fill = Y)

           sphscrollbar = Scrollbar(sproot, orient = HORIZONTAL)
           sphscrollbar.pack(side = BOTTOM, fill = X)

           splistbox.config(yscrollcommand = spvscrollbar.set, xscrollcommand = sphscrollbar.set)
           spvscrollbar.config(command = splistbox.yview)
           sphscrollbar.config(command = splistbox.xview)

           def spselected_item(event):
               value=str((splistbox.get(ANCHOR)))
               print (value)

               spframe3 = Frame(sproot, bg = "#009933")
               spframe3.place(relheight = 1, relwidth = 1)
               showname = showtiming = showauditorium = showdate = "abcd" #get from excel
               Label(spframe3, text = ("Show: " + showname + "\nDate: " + showdate+ "\nTiming: " + showtiming + "\nAuditorium number:" + showauditorium), bg = "#009933", font = ("Garamond", 12)).pack(padx = 5, pady = 5)
               
               def showseats(noofseats, num):
                   spcanvas = Canvas(spframe3)
                   spcanvas.place(relx = 0.03, rely = 0.35, relheight = 0.6, relwidth = 0.94 )
                   x = 0.02
                   y = 0.02
                   statusnormal = ['booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked', 'booked', 'booked', 'booked', 'booked', 'booked', 'unbooked', 'unbooked'] #from excel
                   statusbalcony = ['booked', 'booked', 'booked', 'unbooked','unbooked', 'booked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked','unbooked', 'unbooked', 'booked', 'unbooked', 'booked', 'unbooked', 'unbooked'] #from excel
                   
                   if num == 0:
                       status = statusnormal
                       seattype = 'normal'
                   else:
                       status = statusbalcony
                       seattype = 'balcony'

                   for i in range(noofseats):
                   #if available = green, booked = red                   
                       if x >= 0.93:
                           x = 0.02
                           y = y + 0.12

                       if status[i] == 'booked': 
                           spbutton5 = Button(spcanvas, text = i+1 , bd = 5, bg = '#cc0000')
                           spbutton5.place(relx = x, rely = y, relheight = 0.1, relwidth = 0.05)

                       elif status[i] == 'unbooked':
                           spbutton5 = Button(spcanvas, text = i+1 , bd = 5, bg = '#009933')
                           spbutton5.place(relx = x, rely = y, relheight = 0.1, relwidth = 0.05)
                   
                       x = x + 0.07

               no_of_normals = 100  #from excel
               no_of_balcony = 20   #from excel
               spbutton1 = Button(spframe3, text = 'Normal seats' , bd = 5, command = partial(showseats, no_of_normals, 0))
               spbutton1.place(relx = 0.70, rely = 0.2, relheight = 0.1, relwidth = 0.12)

               spbutton2 = Button(spframe3, text = 'Balcony seats' , bd = 5, command = partial(showseats, no_of_balcony, 1))
               spbutton2.place(relx = 0.83, rely = 0.2, relheight = 0.1, relwidth = 0.12)                
                    
               
               def spdestroy():
                   spframe3.destroy()
                   spframe2.destroy()
                   spvscrollbar.destroy()
                   sphscrollbar.destroy()

               spbutton3 = Button(spframe3, text = 'Back' , bd = 5, command = spdestroy)
               spbutton3.place(relx = 0.03, rely = 0.05, relheight = 0.1, relwidth = 0.1)
               #
           splistbox.bind('<<ListboxSelect>>', spselected_item)

           return
       

        sptosearch = StringVar()

        spentry1 = Entry(spframe, textvariable = sptosearch, bd =5, width = 100, font = ("Garamond"))
        spentry1.place(relx=0.05, rely=0.5, relheight=0.1, relwidth=0.66)

        spbutton1 = Button(spframe, text = 'Search', bd=5, command = spsearch_entry, font = ("Garamond"))
        spbutton1.place(relx = 0.75, rely = 0.5, relheight = 0.1, relwidth = 0.2)

        spbutton2 = Button(spframe, text = 'Go Back', command = spframe.destroy)
        spbutton2.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)
        
        sproot.mainloop()


def startup():
    #read from excel files and shit
    sys = ManagementSystem()
    x = ShowManager('id','pass')
    sys.employees.append(x)
    sys.homeUI()

startup()

# write save methods for shows, auditoriums, ledgers, employees. maybe add a filename field everywhere so you know
# where to save.

# Press the green button in the gutter to run the script.
