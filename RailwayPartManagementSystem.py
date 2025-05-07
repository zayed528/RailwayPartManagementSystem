# RAILWAY WORKSHOP MANAGEMENT SYSTEM

import os
import mysql.connector
import datetime

# Get current timestamp
now = datetime.datetime.now()

# Connect to the MySQL database
myDb = mysql.connector.connect(host="localhost", user="root", password="admin", database="Railway")
mycursor = myDb.cursor()

# Clear the screen
def Clrscr():
    print("\n" * 5)

# Train management menu
def Train_Mgmt():
    while True:
        print("\t\t\t 1. Add New Train Parts")
        print("\t\t\t 2. List Train Parts")
        print("\t\t\t 3. Update Train Parts")
        print("\t\t\t 4. Delete Train Parts")
        print("\t\t\t 5. Back (Main Menu)")
        p = int(input("\t\t Enter Your Choice :"))
        if p == 1: Add_TrainParts()
        if p == 2: Search_TrainParts()
        if p == 3: Update_TrainParts()
        if p == 4: Delete_TrainParts()
        if p == 5: break

# Purchase management menu
def Purchase_Mgmt():
    while True:
        print("\t\t\t 1. Add New Train Parts Order")
        print("\t\t\t 2. List Train Parts Orders")
        print("\t\t\t 3. Back (Main Menu)")
        o = int(input("\t\t Enter Your Choice :"))
        if o == 1: Add_Order()
        if o == 2: List_Order()
        if o == 3: break

# Sales management menu
def Sales_Mgmt():
    while True:
        print("\t\t\t 1. Sale of Scrap Items")
        print("\t\t\t 2. List of Sales")
        print("\t\t\t 3. Back (Main Menu)")
        s = int(input("\t\t Enter Your Choice :"))
        if s == 1: Sale_Train()
        if s == 2: List_Sale()
        if s == 3: break

# Employee management menu
def Employees_Mgmt():
    while True:
        print("\t\t\t 1. Add Employees")
        print("\t\t\t 2. List Employees")
        print("\t\t\t 3. Back (Main Menu)")
        u = int(input("\t\t Enter Your Choice :"))
        if u == 1: Add_Employees()
        if u == 2: List_Employees()
        if u == 3: break

# Create all required tables
def Create_Database():
    mycursor.execute("CREATE TABLE IF NOT EXISTS Train(TrainNumber INT PRIMARY KEY, PartName CHAR(30), Price INT, Part_Qty INT, PartCategory CHAR(30));")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Orders(Orderid INT PRIMARY KEY, Orderdate DATE, PartName CHAR(30), Price INT, Part_Qty INT, supplier CHAR(50), PartCategory CHAR(30));")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Sales(Salesid INT PRIMARY KEY, Salesdate DATE, PartName CHAR(30), Price INT, Part_Qty INT, Total DOUBLE);")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Employees(Eid CHAR(6) PRIMARY KEY, Ename CHAR(30), Epwd CHAR(30));")
    print("All tables created successfully.")

# Show all tables
def List_Database():
    mycursor.execute("SHOW TABLES;")
    for table in mycursor:
        print(table)

# Add new order
def Add_Order():
    now = datetime.datetime.now()
    oid = now.year + now.month + now.day + now.hour + now.minute + now.second
    sql = "INSERT INTO Orders (Orderid, Orderdate, PartName, Price, Part_Qty, supplier, PartCategory) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    part = input("Enter Train Part Name: ")
    price = float(input("Enter Price: "))
    qty = int(input("Enter Quantity: "))
    supplier = input("Enter Supplier: ")
    category = input("Enter Category: ")
    values = (oid, now, part, price, qty, supplier, category)
    mycursor.execute(sql, values)
    myDb.commit()

# Show all orders
def List_Order():
    mycursor.execute("SELECT * FROM Orders")
    for row in mycursor:
        print(row)

# Add train part
def Add_TrainParts():
    sql = "INSERT INTO Train(TrainNumber, PartName, Price, Part_Qty, PartCategory) VALUES (%s,%s,%s,%s,%s)"
    number = int(input("Enter Train Number: "))
    mycursor.execute("SELECT COUNT(*) FROM Train WHERE TrainNumber=%s", (number,))
    if mycursor.fetchone()[0] == 0:
        name = input("Enter Part Name: ")
        price = float(input("Enter Price: "))
        qty = int(input("Enter Quantity: "))
        category = input("Enter Category: ")
        mycursor.execute(sql, (number, name, price, qty, category))
        myDb.commit()
    else:
        print("Part already exists.")

# Update quantity of train part
def Update_TrainParts():
    number = int(input("Enter Train Number: "))
    qty = int(input("Enter Quantity to Add: "))
    mycursor.execute("UPDATE Train SET Part_Qty = Part_Qty + %s WHERE TrainNumber = %s", (qty, number))
    myDb.commit()

# Delete a train part
def Delete_TrainParts():
    number = int(input("Enter Train Number to Delete: "))
    mycursor.execute("DELETE FROM Train WHERE TrainNumber = %s", (number,))
    myDb.commit()

# Search menu for train parts
def Search_TrainParts():
    while True:
        print("\t1. List All Parts\n\t2. Search by Number\n\t3. Search by Category\n\t4. Back")
        choice = int(input("Enter choice: "))
        if choice == 1: List_Train()
        if choice == 2:
            number = int(input("Enter Train Number: "))
            List_PrNumber(number)
        if choice == 3:
            cat = input("Enter Category: ")
            List_prcat(cat)
        if choice == 4: break

# List all train parts
def List_Train():
    mycursor.execute("SELECT * FROM Train")
    for row in mycursor:
        print(row)

# List train part by number
def List_PrNumber(number):
    mycursor.execute("SELECT * FROM Train WHERE TrainNumber = %s", (number,))
    for row in mycursor:
        print(row)

# List train part by category
def List_prcat(cat):
    mycursor.execute("SELECT * FROM Train WHERE PartCategory = %s", (cat,))
    for row in mycursor:
        print(row)

# Handle sale of train parts
def Sale_Train():
    train_no = input("Enter Train Number: ")
    mycursor.execute("SELECT * FROM Train WHERE TrainNumber=%s", (train_no,))
    row = mycursor.fetchone()
    if row:
        print(row)
        qty = int(input("Enter Quantity to Sell: "))
        if qty <= row[3]:
            total = qty * row[2]
            print("Total Price: ", total)
            sale_id = int(datetime.datetime.now().timestamp())
            mycursor.execute("INSERT INTO Sales VALUES (%s,%s,%s,%s,%s,%s)", (sale_id, datetime.datetime.now(), row[1], row[2], qty, total))
            mycursor.execute("UPDATE Train SET Part_Qty = Part_Qty - %s WHERE TrainNumber = %s", (qty, train_no))
            myDb.commit()
        else:
            print("Not enough stock.")
    else:
        print("Train not found.")

# Show all sales
def List_Sale():
    mycursor.execute("SELECT * FROM Sales")
    for row in mycursor:
        print(row)

# Add a new employee
def Add_Employees():
    eid = input("Enter ID: ")
    name = input("Enter Name: ")
    pwd = input("Enter Password: ")
    mycursor.execute("INSERT INTO Employees VALUES (%s,%s,%s)", (eid, name, pwd))
    myDb.commit()

# Show all employees
def List_Employees():
    mycursor.execute("SELECT Eid, Ename FROM Employees")
    for row in mycursor:
        print(row)

# Database setup menu
def Db_Mgmt():
    while True:
        print("\t1. Create Database\n\t2. List Tables\n\t3. Back")
        p = int(input("Enter Choice: "))
        if p == 1: Create_Database()
        if p == 2: List_Database()
        if p == 3: break

# Main program loop
while True:
    Clrscr()
    print("\t\t\t RAILWAY WORKSHOP MANAGEMENT")
    print("\t\t\t ***************************\n")
    print("\t\t 1. TRAIN MANAGEMENT")
    print("\t\t 2. PURCHASE MANAGEMENT")
    print("\t\t 3. SALES MANAGEMENT")
    print("\t\t 4. EMPLOYEES MANAGEMENT")
    print("\t\t 5. DATABASE SETUP")
    print("\t\t 6. EXIT\n")
    n = int(input("\t\t Enter your choice: "))
    if n == 1: Train_Mgmt()
    if n == 2: Purchase_Mgmt()
    if n == 3: Sales_Mgmt()
    if n == 4: Employees_Mgmt()
    if n == 5: Db_Mgmt()
    if n == 6: break
