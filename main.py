# pupupu
# monal trying to make changes to ysh/sams/master/main.py
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import datetime
from functools import partial
from tkinter import *
from tkcalendar import *
import csv
import os.path

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
        self.bseats = [Seat(x, 'Balcony') for x in  range(0, nB)]
        self.nseats = [Seat(x, 'Normal') for x in  range(0, nN)]
        self.audino = audiNum

    def showAvailableSeats(self):  # differs from SRS prototype
        return [x for x in self.seats if x.isAvailable()]

    def percentageOccupied(self):  # shorten this code
        balconies = 0
        nB = len(self.bseats)
        normals = 0
        nN = len(self.nseats)
        for x in self.bseats:
            if not x.isAvailable():
                 balconies += 1
        for x in self.nseats:
            if not x.isAvailable():
                normals+=1


        return 100 * (balconies + normals) / float(
            nB + nN)  # if we can diverge from srs prototypes, nahi toh calculate karke print kardo


class Auditorium:
    def __init__(self):
        self.shows = []
        # read excel file & create shows list

    def addshow(self, show):
        self.shows.append(show)
        # update shows list

    def findShow(self, name):
        return [x for x in self.shows if name in x.name]


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

        self.rate =int(rate)

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
        self.transactions[len(self.transactions)] = Transaction(value, len(self.transactions), name, date)
        return True
        # update excel file


class ManagementSystem:
    def __init__(self):
        self.auditoriums = Auditorium()  # SRS says auditorium array
        self.ledger = Ledger()
        self.employees = []
        self.balanceSheet = {}       #[audino,starttime]->[name,value]
        self.currentemployee=None

    def save(self):
        pass

        
        #save to ledger.csv            format: ['ID','name','date','price']        name is a string of showname,audino,starttime, and is irrelevant mostly
        fields = ['ID','name','date','price']
        
        transactionFile = "alltransactions.csv"
        with open(transactionFile,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()
        
        '''t1 = Transaction(40,1,"booking",90)
        t2 = Transaction(40,2,"booking",91)
        transactionss = {1:t1,2:t2}'''
        for key,y in self.ledger.transactions.items():
            data = [y.transactionID,y.name,y.date,y.value]
            transactionFile = open("alltransactions.csv", 'a+', newline ='')
            with transactionFile:
                write = csv.writer(transactionFile)
                write.writerow(data)    

        #save to balancesheet.csv      format: [name, audino, starttime, value]
        fields = ['name', 'audino', 'starttime', 'value']
        balSheet = "balanceSheet.csv"
        with open(balSheet,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()

        for key,y in self.balanceSheet.items():
            audinum = key.split(' ;')[0]
            date = key.split(' ;')[1]
            data = [y[1],audinum,date,y[0]]
            balSheet = open("balanceSheet.csv", 'a+', newline ='')
            with balSheet:
                write = csv.writer(balSheet)
                write.writerow(data)        

        #save to shows.csv    format: [starttime, endtime, audiNum, name, nB, nN, priceB, priceN]
        fields = ['starttime', 'endtime', 'audiNum', 'name', 'numBalcony', 'numNormal', 'priceB', 'priceN']
        showsList = "Shows.csv"
        with open(showsList,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()

        for x in self.auditoriums.shows:
            data = [x.startTime, x.endTime, x.audino, x.name, len(x.bseats), len(x.nseats), x.priceBalcony, x.priceNormal]
            showsFile = open("Shows.csv", 'a+', newline ='')
            with showsFile:
                write = csv.writer(showsFile)
                write.writerow(data)
            fields = ['number','type','transactionId','status']
            seatFile = x.name+"_"+str(x.audino)+"_"+ x.startTime.strftime("%c")+".csv"
            seatFile = seatFile.replace(" ","_")
            seatFile = seatFile.replace(":","_")

            with open(seatFile,'w',newline='') as csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=fields)
                writer.writeheader()   
            for y in x.bseats:
                data2  = [y.seatNumber,"balcony",y.transactionID,y.allotmentStatus]
                seatfilee = open(seatFile,'a+',newline='')
                with seatfilee:
                    write = csv.writer(seatfilee)
                    write.writerow(data2) 
            for y in x.nseats:
                data2  = [y.seatNumber,"normal",y.transactionID,y.allotmentStatus]
                seatfilee = open(seatFile,'a+',newline='')
                with seatfilee:
                    write = csv.writer(seatfilee)
                    write.writerow(data2)       
        #save seats for each show to "avengers 3 Mon, Jan 1 2001 00:00".csv

        #save to employees.csx    format:[id, password,commission rate,commission,type,transactionList]
        fields = ['id', 'password','commission rate','commission','type','transactionList']
        employeeFile = "employees.csv"
        with open(employeeFile,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()

        for y in self.employees:
            data = [y.loginID,y.password]
            if isinstance(y,ShowManager):
                data.extend([-1,-1,"showmanager"," "])
            elif isinstance(y,AuditClerk):
                 data.extend([-1,-1,"auditclerk"," "])
            else:
                data.extend([y.rate,y.commission,"salesperson",y.transactions])     
                
            employeeFile = open("employees.csv", 'a+', newline ='')
            with employeeFile:
                write = csv.writer(employeeFile)
                write.writerow(data)   



    '''def read(self, ledgerfile, loginfile, auditoriumfile):  # method not in SRS
        pass  # TBD'''
    
    def book(self, seat, show):
        ID = len(self.ledger.transactions)
        if seat.seatType == 'Normal':
            value = show.priceNormal
        else:
            value = show.priceBalcony
        if seat.isAvailable():
            seat.allot(ID)
            self.ledger.addExpense(show.name+show.audino+show.startTime.strftime("%c"),value, datetime.now())
        else:
            seat.cancel()
            value*=-1
            self.ledger.addExpense(show.name+show.audino+show.startTime.strftime("%c"),value, datetime.now())

        self.currentemployee.transactions.append(ID)
        self.currentemployee.commission += self.currentemployee.rate * value
        key = str(show.audino) + ' ;'+show.startTime.strftime("%c")
        self.balanceSheet[key] = [self.balanceSheet.get(key,[0,''])[0]+value,show.name]
        return [ID, value]


    def book(self, seat, show):
        ID = len(self.ledger.transactions)
        if seat.seatType == 'Normal':
            value = show.priceNormal
        else:
            value = show.priceBalcony
        if seat.isAvailable():
            seat.allot(ID)
            self.ledger.addExpense(show.name+show.audino+show.startTime.strftime("%c"),value, datetime.now())
        else:
            seat.cancel()
            value*=-1
            self.ledger.addExpense(show.name+show.audino+show.startTime.strftime("%c"),value, datetime.now())

        self.currentemployee.transactions.append(ID)
        self.currentemployee.commission += self.currentemployee.rate * value

        return [ID, value]


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
        # save employee to excel
        label = Label(newf, text="Account Created", bg="#ffd6d6")
        label.place(relx=0, rely=0, relheight=1, relwidth=1)

    def loginUI(self, root):  # prototype differs from SRS

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button6 = Button(frame, text="Go Back", command=frame.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        label1 = Label(frame, text="Login ID:", bg="#ffd6d6")
        label1.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.15)

        entry1 = Entry(frame)
        entry1.place(relx=0.35, rely=0.25, relwidth=0.6, relheight=0.15)

        label2 = Label(frame, text="Password", bg="#ffd6d6")
        label2.place(relx=0.05, rely=0.5, relwidth=0.2, relheight=0.15)

        entry2 = Entry(frame)
        entry2.place(relx=0.35, rely=0.5, relwidth=0.6, relheight=0.15)

        def login(ID, passw):
            for emp in self.employees:
                if emp.loginID == ID and emp.password == passw:
                    self.currentemployee = emp
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

        button1 = Button(frame, text='Login', command=lambda: login(str(entry1.get()), str(entry2.get())))
        button1.place(relx=0.45, rely=0.75, relwidth=0.1, relheight=0.15)

    def homeUI(self):
        root = Tk()

        canvas = Canvas(root, height=300, width=750)
        canvas.pack()

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button1 = Button(frame, text='Employee', command=lambda: self.loginUI(root))
        button1.place(relx=0.3, rely=0.4, relwidth=0.1, relheight=0.2)

        button2 = Button(frame, text='Spectator', command=lambda: self.SpectatorMenu(root))
        button2.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.2)

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
            global starttime, endtime, startdate, enddate
            def getsdt():
                cal = Calendar(root, selectmode = 'day',
                                          year = 2020, month = 5,
                                                     day = 22)
  
                cal.place(relx = 0.05, rely = 0.43)

                def grad_date():
                   global startdate
                   c = cal.get_date()
                   print(c)
                   startdate = c
                   cal.destroy()

                   options = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
                   clicked = StringVar()

                   clicked.set( "Select Time" )

                   etime = ' time not selected'
                   
                   def gettime(v, c):
                       v = str(v)
                       print(v)
                       global startdate
                       startdate += ' '+c
                       drop.destroy()                       
                       bb.destroy()
                       labelst = Label(newframe, text= (c + " " + v), bg = "#ffd6d6")
                       labelst.place(relx=0.25, rely=0.30, relwidth=0.2, relheight=0.12)

                   drop = OptionMenu( root , clicked , *options, command = partial(gettime, c) )
                   drop.place(relx = 0.25, rely = 0.30)

                   


                bb = Button(root, text = "Done",
                                      command = grad_date)
                bb.place(relx = 0.25, rely = 0.30)
                          



            buttonst = Button(newframe, text="Start Time:", command = getsdt)
            buttonst.place(relx=0.05, rely=0.30, relwidth=0.15, relheight=0.12)

            def getedt():
                cal = Calendar(root, selectmode = 'day',
                                          year = 2020, month = 5,
                                                     day = 22)
  
                cal.place(relx = 0.55, rely = 0.43)

                def grad_date():
                   c = cal.get_date()
                   print(c)
                   cal.destroy()
                   global enddate
                   enddate = c
                   options = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
                   clicked = StringVar()


                   clicked.set( "Select Time" )

                   etime = ' time not selected'
                   
                   def gettime(v, c):
                       v = str(v)
                       print(v)
                       global enddate
                       enddate += ' '+c
                       drop.destroy()                       
                       bb.destroy()
                       labelst = Label(newframe, text= (c + " " + v), bg = "#ffd6d6")
                       labelst.place(relx=0.75, rely=0.30, relwidth=0.2, relheight=0.12)

                   drop = OptionMenu( root , clicked , *options, command = partial(gettime, c) )
                   drop.place(relx = 0.75, rely = 0.30)

                   


                bb = Button(root, text = "Done",
                                      command = grad_date)
                bb.place(relx = 0.75, rely = 0.30)
                          



            buttonet = Button(newframe, text="End Time:", command = getedt)
            buttonet.place(relx=0.55, rely=0.30, relwidth=0.15, relheight=0.12)

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
                             command=lambda: self.createshow(newframe, entry1.get(), entry2.get(), startdate,
                                                             enddate, entry5.get(), entry6.get(), entry7.get(),
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
                listbox.insert(1,
                               "Name" + " " * 36 + "Start Time" + " " * 30 + "End Time" + " " * 32 + "Percentage occupied")
                for x in self.auditoriums.shows:
                    if x.audino is audi:
                        listbox.insert(listbox.size() + 1,
                                       x.name + " " * (40 - len(x.name)) + x.startTime.strftime("%c") + " " * (
                                               40 - len(x.startTime.strftime("%c"))) + x.endTime.strftime(
                                           "%c") + " " * (
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
                if isinstance(x, SalesPerson):
                    listbox.insert(listbox.size() + 1, str(x.loginID))
            listbox.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.6)

            def getHistory(event):
                ID = str(listbox.get(listbox.curselection()))
                for x in self.employees:
                    if x.loginID == ID:
                        emp = x
                newnewframe = Frame(root, bg="#ffd6d6")
                newnewframe.place(relwidth=1, relheight=1)

                button6 = Button(newnewframe, text="Go Back", command=newnewframe.destroy)
                button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

                translist = Listbox(newnewframe)
                for x in emp.transactions:
                    y = self.ledger.transactions[x]
                    translist.insert(translist.size() + 1,
                                     str(y.transactionID) + " " + y.name + " " + y.date.strftime("%c") + " " + str(y.value)
                                     )

                translist.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.75)

            listbox.bind('<Double-1>', getHistory)

        def balanceSheet():
            newframe = Frame(root, bg="#ffd6d6")
            newframe.place(relwidth=1, relheight=1)

            button6 = Button(newframe, text="Go Back", command=newframe.destroy)
            button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

            listbox = Listbox(newframe)
            # insert things to listbox from self.balancesheet
            listbox.place(relx=0.05, relwidth=0.9, rely=0.2, relheight=0.75)

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

        framed = Frame(sproot,bg = "#ffd6d6")
        framed.place(relwidth=1, relheight=1)

        spframe = Frame(sproot, bg="#ffd6d6")
        spframe.place(relwidth=1, relheight=0.3)
        sproot.title("Welcome Salesperson")

        def spsearch_entry():
            e = (sptosearch.get())
            print(e)

            spframe2 = Frame(sproot, bg="#ffd6d6")
            spframe2.place(relwidth=1, relheight=0.7, rely=0.3)

            # get from excel
            # ff
            # get spshows from excel and show only those that match with e
            spshows = self.auditoriums.findShow(e)  # get from excel
            splistbox = Listbox(spframe2)

            for x in spshows:
                splistbox.insert(splistbox.size() + 1,

                                 x.name + " ;" + str(x.audino) + " ;" + x.startTime.strftime("%c") + " ;" + x.endTime.strftime("%c"))

            splistbox.place(relx=0.05, rely=0.05, relheight=0.85, relwidth=0.9)

            def spselected_item(event):
                value = str((splistbox.get(ANCHOR))).split(' ;')
                print(value)

                def spdestroy():
                    spframe3.destroy()
                    spframe2.destroy()

                spframe3 = Frame(sproot, bg="#ffd6d6")
                spframe3.place(relheight=1, relwidth=1)

                show = None
                for x in self.auditoriums.shows:
                    if x.name == value[0] and x.audino == value[1] and (
                    x.startTime.strftime("%c") == value[2]):
                        show = x
                if show is None:
                    spdestroy()
                    return

                Label(spframe3, text=(
                        "Show: " + show.name + "\nStarts at: " + show.startTime.strftime(
                    "%c") + "\nEnds at: " + show.endTime.strftime("%c") + "\nAuditorium number:" + show.audino),
                      bg="#ffd6d6").pack(padx=5, pady=5)

                def showseats(noofseats, num):
                    spcanvas = Frame(spframe3)
                    spcanvas.place(relx=0.03, rely=0.35, relheight=0.6, relwidth=0.94)

                    statusnormal = []
                    for x in show.nseats:
                        if x.isAvailable():
                            statusnormal.append('unbooked')
                        else:
                            statusnormal.append('booked')

                    statusbalcony = []
                    for x in show.bseats:
                        if x.isAvailable():
                            statusbalcony.append('unbooked')
                        else:
                            statusbalcony.append('booked')

                    if num == 0:
                        status = statusnormal
                        seattype = 'normal'
                    else:
                        status = statusbalcony
                        seattype = 'balcony'

                    x = 0.02
                    y = 0.02

                    for i in range(noofseats):
                        # if available = green, booked = red
                        if x > 0.95:
                            x = 0.02
                            y = y + 0.14

                        if status[i] == 'booked':
                            spbutton5 = Button(spcanvas, text=i + 1, bd=5, bg='#cc0000', command =partial(spbookseat,i, show, num))
                            spbutton5.place(relx=x, rely=y, relheight=0.12, relwidth=0.05)

                        elif status[i] == 'unbooked':
                            spbutton5 = Button(spcanvas, text=i + 1, bd=5, bg='#009933', command =partial(spbookseat, i, show, num))
                            spbutton5.place(relx=x, rely=y, relheight=0.12, relwidth=0.05)

                        x = x + 0.07

                no_of_normals = len(show.nseats)  # from excel
                no_of_balcony = len(show.bseats)  # from excel
                spbutton1 = Button(spframe3, text='Normal seats', bd=5, command=partial(showseats, no_of_normals, 0))
                spbutton1.place(relx=0.70, rely=0.2, relheight=0.1, relwidth=0.12)

                spbutton2 = Button(spframe3, text='Balcony seats', bd=5, command=partial(showseats, no_of_balcony, 1))
                spbutton2.place(relx=0.83, rely=0.2, relheight=0.1, relwidth=0.12)

                spbutton3 = Button(spframe3, text='Back', bd=5, command=spdestroy)
                spbutton3.place(relx=0.03, rely=0.05, relheight=0.1, relwidth=0.1)

            def spbookseat(seatnumber, show, num):
                spframe4 = Frame(sproot, bg="#ffd6d6")
                spframe4.place(relheight=1, relwidth=1)

                spbutton6 = Button(spframe4, text='Back', bd=5, command=spframe4.destroy)
                spbutton6.place(relx=0.03, rely=0.05, relheight=0.1, relwidth=0.1)

                if num == 0:
                    seat = show.nseats[seatnumber]
                elif num == 1:
                    seat = show.bseats[seatnumber]

                Label(spframe4, text=("Confirm changes to seat number " + str(seatnumber + 1) + " for show " + show.name),
                      bg="#ffd6d6").pack(padx=25, pady=100)
                spbutton7 = Button(spframe4, text='Confirm Booking', bd=5,
                                   command=lambda: self.book(seat,show))
                spbutton7.place(relx=0.4, rely=0.4, relheight=0.1, relwidth=0.15)

            splistbox.bind('<Double-1>', spselected_item)

            return

        sptosearch = StringVar()

        spentry1 = Entry(spframe, textvariable=sptosearch, bd=5, width=100)
        spentry1.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.66)

        spbutton1 = Button(spframe, text='Search', bd=5, command=spsearch_entry)
        spbutton1.place(relx=0.75, rely=0.5, relheight=0.3, relwidth=0.2)

        def findestroy():
            spframe.destroy()
            framed.destroy()

        spbutton2 = Button(spframe, text='Log Out', bd=5, command=findestroy)
        spbutton2.place(relx=0.05, rely=0.1, relheight=0.3, relwidth=0.1)

    # book-> update seat allotment excel files for the particular show

    def AuditClerkMenu(self, root):

        frame = Frame(root, bg="#ffd6d6")
        frame.place(relwidth=1, relheight=1)

        button6 = Button(frame, text="Logout", command=frame.destroy)
        button6.place(relx=0.05, relwidth=0.075, rely=0.05, relheight=0.1)

        label1 = Label(frame, text="Enter expense name: ", bg="#ffd6d6")
        label1.place(relx=0.05, relwidth=0.425, rely=0.24, relheight=0.1)

        entry1 = Entry(frame)
        entry1.place(relx=0.525, relwidth=0.425, rely=0.24, relheight=0.1)

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
                label4 = Label(frame, text=entry1.get() + " Saved Successfully", bg="#ffd6d6")
                label4.place(relx=0.55, relwidth=0.4, rely=0.81, relheight=0.1)
            else:
                label4 = Label(frame, text="Could not be saved", bg="#ffd6d6")
                label4.place(relx=0.55, relwidth=0.4, rely=0.81, relheight=0.1)
            # add same for balance sheet

        button1 = Button(frame, text="Save", command=save)
        button1.place(relx=0.05, relwidth=0.1, rely=0.81, relheight=0.1)

    def SpectatorMenu(self, sproot):  # differs from SRS

        framed = Frame(sproot, bg = "#ffd6d6")
        framed.place(relwidth = 1, relheight = 1)
        spframe = Frame(sproot, bg="#ffd6d6")
        spframe.place(relwidth=1, relheight=0.3)
        sproot.title("Welcome Spectator")

        def spsearch_entry():
            e = (sptosearch.get())
            print(e)

            spframe2 = Frame(sproot, bg="#ffd6d6")
            spframe2.place(relwidth=1, relheight=0.7, rely=0.3)

            # get from excel
            # ff
            # get spshows from excel and show only those that match with e
            spshows = self.auditoriums.findShow(e)  # get from excel
            splistbox = Listbox(spframe2)

            for x in spshows:
                splistbox.insert(splistbox.size()+1, x.name+" ;"+x.audino+" ;"+x.startTime.strftime("%c")+" ;"+x.endTime.strftime("%c"))
            splistbox.place(relx=0.05, rely=0.05, relheight=0.85, relwidth=0.9)

            def spselected_item(event):
                value = str((splistbox.get(ANCHOR))).split(' ;')
                print(value)

                def spdestroy():
                    spframe3.destroy()
                    spframe2.destroy()

                spframe3 = Frame(sproot, bg="#ffd6d6")
                spframe3.place(relheight=1, relwidth=1)

                show = None
                for x in self.auditoriums.shows:
                    if x.name == value[0] and x.audino == value[1] and (x.startTime.strftime("%c") == value[2]):
                        show = x
                if show is None:
                    spdestroy()
                    return

                Label(spframe3, text=(
                            "Show: " + show.name + "\nStarts at: " + show.startTime.strftime("%c") + "\nEnds at: " + show.endTime.strftime("%c") + "\nAuditorium number:" + show.audino),
                      bg="#ffd6d6").pack(padx=5, pady=5)

                def showseats(noofseats, num):
                    spcanvas = Frame(spframe3)
                    spcanvas.place(relx=0.03, rely=0.35, relheight=0.6, relwidth=0.94)

                    statusnormal = []
                    for x in show.nseats:
                        if x.isAvailable():
                            statusnormal.append('unbooked')
                        else:
                            statusnormal.append('booked')

                    statusbalcony = []
                    for x in show.bseats:
                        if x.isAvailable():
                            statusbalcony.append('unbooked')
                        else:
                            statusbalcony.append('booked')


                    if num == 0:
                        status = statusnormal
                        seattype = 'normal'
                    else:
                        status = statusbalcony
                        seattype = 'balcony'

                    x = 0.02
                    y = 0.02

                    for i in range(noofseats):
                        # if available = green, booked = red
                        if x > 0.95:
                            x = 0.02
                            y = y + 0.14

                        if status[i] == 'booked':
                            spbutton5 = Button(spcanvas, text=i + 1, bd=5, bg='#cc0000')
                            spbutton5.place(relx=x, rely=y, relheight=0.12, relwidth=0.05)

                        elif status[i] == 'unbooked':
                            spbutton5 = Button(spcanvas, text=i + 1, bd=5, bg='#009933')
                            spbutton5.place(relx=x, rely=y, relheight=0.12, relwidth=0.05)

                        x = x + 0.07

                no_of_normals = len(show.nseats)  # from excel
                no_of_balcony = len(show.bseats)  # from excel
                spbutton1 = Button(spframe3, text='Normal seats', bd=5, command=partial(showseats, no_of_normals, 0))
                spbutton1.place(relx=0.70, rely=0.2, relheight=0.1, relwidth=0.12)

                spbutton2 = Button(spframe3, text='Balcony seats', bd=5, command=partial(showseats, no_of_balcony, 1))
                spbutton2.place(relx=0.83, rely=0.2, relheight=0.1, relwidth=0.12)


                spbutton3 = Button(spframe3, text='Back', bd=5, command=spdestroy)
                spbutton3.place(relx=0.03, rely=0.05, relheight=0.1, relwidth=0.1)
                #

            splistbox.bind('<Double-1>', spselected_item)

            return

        sptosearch = StringVar()

        spentry1 = Entry(spframe, textvariable=sptosearch, bd=5, width=100)
        spentry1.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.66)

        spbutton1 = Button(spframe, text = 'Search', bd=5, command = spsearch_entry)
        spbutton1.place(relx = 0.75, rely = 0.5, relheight = 0.3, relwidth = 0.2)

        def findestroy():
            spframe.destroy()
            framed.destroy()

        spbutton2 = Button(spframe, text='Return' , bd = 5, command=findestroy)
        spbutton2.place(relx = 0.05, rely = 0.1, relheight = 0.3, relwidth = 0.1)


def startup():
    # read from excel files and shit
    sys = ManagementSystem()
    x = ShowManager('id', 'pass')
    y = SalesPerson('id1', 'pass1', 100)
    '''t1 = Show(datetime.strptime("01/01/01 00:00", '%m/%d/%y %H:%M'),datetime.strptime("01/01/01 02:00", '%m/%d/%y %H:%M'),"1","test1",90,10,250,200)
    t2 = Show(datetime.strptime("02/01/01 00:00", '%m/%d/%y %H:%M'),datetime.strptime("02/01/01 00:00", '%m/%d/%y %H:%M'),"1","test2",90,10,250,200)
    sys.auditoriums.addshow(t1)
    sys.auditoriums.addshow(t2)
    sys.employees.append(x)
    sys.employees.append(y)'''
    #read ledger
    if os.path.isfile('alltransactions.csv'):
        with open('alltransactions.csv', mode ='r+')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                if lines[3] != 'price':
                    t = Transaction(int(lines[3]),int(lines[0]),lines[1],lines[2])   
                    sys.ledger.transactions[lines[0]]=t
    else:
        print("alltransactions file not found")  

    #read balance sheet
    if os.path.isfile('balanceSheet.csv'):
        with open('balancesheet.csv', mode ='r+')as file:
            csvFile = csv.reader(file)
            for lines in csvFile: 
                if lines[3]!= 'value':           
                    key = str(lines[1]) + ' ;'+lines[2]
                    sys.balanceSheet[key] =  [int(float(lines[3])),lines[0]]
    else:
        print("balancesheet file not found") 
    #read shows.csv
    if os.path.isfile('Shows.csv'):
        with open('Shows.csv', mode ='r+')as file:
            csvFile = csv.reader(file)
            for lines in csvFile: 
                if lines[2]!= 'audiNum':
                    print(type(lines[0]))   
                    s= Show(datetime.strptime(lines[0],'%Y-%m-%d %H:%M:%S'),datetime.strptime(lines[1],'%Y-%m-%d %H:%M:%S'),int(lines[2]),lines[3],int(lines[4]),int(lines[5]),int(lines[6]),int(lines[7]))
                    sys.auditoriums.shows.append(s)
                    # print("aa")
                    # print(lines[0])
                    # print(type(lines[0]))
                    seatFile = s.name+"_"+str(s.audino)+"_"+ datetime.strptime(lines[0],'%Y-%m-%d %H:%M:%S').strftime("%c")+".csv"
                    seatFile = seatFile.replace(" ","_")
                    seatFile = seatFile.replace(":","_")
                    with open(seatFile, mode ='r+')as file2:
                        csvFile = csv.reader(file2)
                        for line in csvFile: 
                            if line[1] == 'balcony':
                                x = Seat(int(line[0]),'balcony')
                                if line[2]=='':
                                    x.transactionID = None
                                else:
                                    x.transactionID = int(line[2])
                                x.allotmentStatus = line[3]
                                s.bseats.append(x)
                            elif line[1] == 'normal':
                                x = Seat(int(line[0]),'normal')
                                if line[2]=='':
                                    x.transactionID = None
                                else:
                                    x.transactionID = int(line[2])
                                x.allotmentStatus = line[3]
                                s.nseats.append(x)    
    else:
        print("shows file not found") 

    #read employees:
    if os.path.isfile('employees.csv'):
        with open('employees.csv', mode ='r+')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:  
                   if lines[4] == "showmanager":
                       ep = ShowManager(lines[0],lines[1])
                   elif lines[4] == "auditclerk":
                       ep = AuditClerk(lines[0],lines[1])
                   elif lines[4] == "salesperson":
                       ep = SalesPerson(lines[0],lines[1],int(lines[2]))  
                       ep.commission = int(lines[3])
                       ep.transactions = lines[5]             
    else:
        print("employee file not found")             

    sys.homeUI()          #UNCOMMENT FFS
    sys.save()

    


startup()

# write save methods for shows, auditoriums, ledgers, employees. maybe add a filename field everywhere so you know
# where to save.

# Press the green button in the gutter to run the script.
