import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import datetime
import sqlite3 as sq
import MySQLdb as mysql
import csv

master = tk.Tk()

canvas = tk.Canvas(master, width = 1280, height = 250)
canvas.create_text(640,75, text = "Darkstar Visitor Sign In", font="system 40")
canvas.pack()

canvas.create_text(640,225, text = "Please Scan Your ID or Enter Your Name", font="system 20")


def get_name(barcode):
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('SELECT name FROM patrons WHERE id = '+str(barcode))
    row = c.fetchone()
    if row != None:
        return(row[0])
    else:
        return(None)

def clear_visitor_log():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('DELETE FROM visitor_log')
    conn.commit()
    conn.close()
    

def barcode_input():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    #c.execute('DROP TABLE visitor_log')
    c.execute('CREATE TABLE IF NOT EXISTS visitor_log (id INTEGER, name TEXT, affiliation TEXT, timestamp TEXT)')    
    while True:
        barcode = simpledialog.askstring("Barcode Input", "Scan Barcode: ")
        timestamp = str(datetime.datetime.now())
        if str(barcode) == "None":
            break
            file.close()
            conn.commit()
            conn.close()
        elif barcode.isdigit() and len(str(barcode)) == 14:
            name = get_name(barcode)
            if name != None:
                c.execute('INSERT INTO visitor_log VALUES (' + '"'+str(barcode)+'"'+ ', '+'"'+str(name)+'"' + ', '+ '"'+'student'+'"' + ', '+'"'+str(timestamp)+'"'+')')
                conn.commit()
                conn.close()
            else:
                if register.get() == 0:
                    c.execute('INSERT INTO visitor_log VALUES (' + '"' + str(barcode) + '"'+ ', '+ 'NULL' + ', '+'"'+'student'+'"'+ ', ' +'"'+str(timestamp)+'"'+')')
                    conn.commit()
                    conn.close()
                else:
                    name = simpledialog.askstring("Name Input", "Enter Name: ")
                    affiliation = simpledialog.askstring("Affiliation", "Enter Affiliation (Student, staff, guest, alumni): ")
                    c.execute('INSERT INTO visitor_log VALUES (' + '"'+str(barcode)+'"'+ ', '+'"'+str(name)+'"' + ', '+ '"'+str(affiliation)+'"' + ', '+'"'+str(timestamp)+'"'+')')
                    conn.commit()
                    conn.close()
                    
            file = open("C:/Users/johnj/Desktop/barcode.txt", 'a+')
            file.write(str(barcode)+", "+timestamp+", "+"\n")
        else:
            messagebox.showerror("Error", "Error: Invalid input type. Please scan a student ID.")
            break
            conn.commit()
            conn.close()
            file.close()


def name_input():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visitor_log (id INTEGER, name TEXT, affiliation TEXT, timestamp TEXT)') 
    while True:
        name = simpledialog.askstring("Name Input", "Enter Name: ")
        affiliation = simpledialog.askstring("Affiliation", "Enter Affiliation (Student, staff, guest, alumni): ")
        timestamp = str(datetime.datetime.now())
        if str(name) == "None":
            break
            file.close()
            conn.commit()
            conn.close()
        elif len(str(name)) < 2:
            break
            conn.commit()
            conn.close()
            file.close()
        else:
            file = open("C:/Users/johnj/Desktop/barcode.txt", 'a+')
            file.write(str(name)+", "+timestamp+", ")
            c.execute('INSERT INTO visitor_log VALUES (' + 'NULL' + ', ' +'"'+str(name)+'"' + ', '+ '"'+str(affiliation)+'"' + ', ' +'"'+str(timestamp)+'"'+ ')')
            conn.commit()
            conn.close()
            file.close()


def update_patrons():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS patrons (id INTEGER, name TEXT)')
    c.execute('DELETE FROM patrons')
    #db = mysql.connect(host = "localhost",user="root", passwd="********", db="sys")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patrons")
    numrows = cursor.rowcount
    for x in range(0, numrows):
        row = cursor.fetchone()
        c.execute("INSERT INTO patrons VALUES ("+"'"+row[0]+"'"+", "+"'"+str(row[2])+" "+str(row[1])+"'"+")")
    conn.commit()
    conn.close()
    db.commit()
    db.close()    
        
def show_patrons():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patrons')
    row = c.fetchall()
    numrows = len(row)
    for x in range(0,numrows):
        print(row[x])
    
def show_visitor_log():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('SELECT * FROM visitor_log')
    row = c.fetchall()
    numrows = len(row)
    for x in range(0,numrows):
        print(row[x])

def export_log_to_csv():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('SELECT * FROM visitor_log')
    row = c.fetchall()
    csvWriter = csv.writer(open("visitor_log.csv","w"))
    csvWriter.writerows(row)
    
def export_patrons_to_csv():
    conn = sq.connect('darkstar.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patrons')
    row = c.fetchall()
    csvWriter = csv.writer(open("patrons.csv","w"))
    csvWriter.writerows(row)


#Test barcode: 21822056999362


#update_patrons()

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff = 0)
filemenu.add_command(label="Print Patron Records", command = show_patrons)
filemenu.add_command(label="Print Visitor Log", command = show_visitor_log)
#filemenu.add_command(label="Clear Visitor Log", command = clear_visitor_log)
filemenu.add_command(label="Export Visitor Log as csv", command = export_log_to_csv)
filemenu.add_command(label="Update Patron Records", command = update_patrons)
filemenu.add_command(label="Export Patron Records as csv", command = export_patrons_to_csv)

menubar.add_cascade(label="Options", menu = filemenu)
master.config(menu=menubar)
    
b = tk.Button(master, text = "Input Barcodes", command = barcode_input, bd = 10)
b.pack()

d = tk.Button(master, text = "Input Names", command = name_input, bd = 10)
d.pack()

register = tk.IntVar()
c = tk.Checkbutton(master, text="Register Unknown Patrons", variable=register)
c.pack()

export_log_to_csv()

tk.mainloop()
