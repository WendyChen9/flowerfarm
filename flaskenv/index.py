# imports flask library and creates a new website stored in app
# import function render_template
from flask import Flask, render_template, request, redirect, session, g, url_for, abort, flash
import cgi
import os
from wtforms import Form
from wtforms.ext.appengine.db import model_form
import random
import cx_Oracle
app = Flask(__name__)


#con = cx_Oracle.connect('wchen9/password@Wendys-Laptop/XE')
con = cx_Oracle.connect('wchen9/password@127.0.0.1/XE')
cur = con.cursor()

#test
#entry2 = [(random.getrandbits(20), 'weend', '2022222', 'home2', 0, 1, 0, 0, 0, 'jan2','jan3')]
#cur.bindarraysize = 1
#cur.setinputsizes(int, 50, 50, 50, int, int, int, int, int, 50, 50)
#cur.executemany("insert into CORDER(OID, NAME, PHONE, ADDRESS) VALUES (:0, :1, :2, :3)", entry2)
#cur.executemany("INSERT INTO CORDER(OID, NAME, PHONE, ADDRESS,WMICRO,MMICRO,CMICRO,HMICRO, BG, ODATE, DDATE) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)", entry2)
#cur.execute("select * from CORDER")
#con.commit
#res=cur.fetchall()
#print(res)
print(con.version)

form = cgi.FieldStorage()

# route address / to hello world function
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/order', methods=['GET','POST'])
def order_page():
    global oid, name, number, address, wmicro, mmicro, hmicro, cmicro, bg, odate, ddate
    if request.method == 'POST':
        #order ID
        oid = random.getrandbits(20)
        #get inputted values
        name = str(request.values.get('name'))
        number = str(request.values.get('number'))
        address = str(request.values.get('address'))
        wmicro = int(request.values.get('wmicro'))
        mmicro = int(request.values.get('mmicro'))
        hmicro = int(request.values.get('hmicro'))
        cmicro = int(request.values.get('cmicro'))
        bg = int(request.values.get('bg'))
        odate = str(request.values.get('odate'))
        ddate = str(request.values.get('ddate'))
        order = [(oid, name, number, address, wmicro, mmicro, cmicro, hmicro, bg, odate, ddate)]
        cur.bindarraysize = 1
        cur.setinputsizes(int, 50, 50, 50, int, int, int, int, int, 50, 50)
        cur.executemany(
        "INSERT INTO CORDER(OID, NAME, PHONE, ADDRESS,WMICRO,MMICRO,CMICRO,HMICRO, BG, ODATE, DDATE) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)",
        order)
        con.commit()
        print(order)
    return render_template('new-order.html')

@app.route('/list')
def order_list():
    cur=con.cursor()
    #find all orders
    cur.execute("select * from CORDER")
    order=cur.fetchall()
    print(order)
    return render_template('list-orders.html',order=order)

@app.route('/edit/<id>', methods=['GET','POST'])
def edit_order(id):
    global name, number, address, wmicro, mmicro, hmicro, cmicro, bg, odate, ddate
    #order id
    id=id
    cur=con.cursor()
    #select query to find specific order id
    stmt = "select * from CORDER where OID="+str(id)
    cur.execute(stmt)
    order=cur.fetchall()
    print(order)
    if request.method == 'POST':
        # get inputted values
        name = str(request.values.get('name'))
        number = str(request.values.get('number'))
        address = str(request.values.get('address'))
        wmicro = int(request.values.get('wmicro'))
        mmicro = int(request.values.get('mmicro'))
        hmicro = int(request.values.get('hmicro'))
        cmicro = int(request.values.get('cmicro'))
        bg = int(request.values.get('bg'))
        odate = str(request.values.get('odate'))
        ddate = str(request.values.get('ddate'))

        #update statement
        stmt = "update CORDER set NAME=\'"+name+"\', PHONE=\'"+number+"\', ADDRESS=\'"+address
        stmt = stmt+"\', WMICRO="+str(wmicro)+", MMICRO="+str(mmicro)+", CMICRO="+str(cmicro)
        stmt = stmt+", HMICRO="+str(hmicro)+", BG="+str(bg)+", ODATE=\'"+odate+"\', DDATE=\'"+ddate+"\'"
        stmt = stmt+" where OID="+str(id)
        #stmt = "update CORDER set NAME=\'"+name+"\' where OID="+str(id)

        cur = con.cursor()
        #update = [(oid, name, number, address, wmicro, mmicro, cmicro, hmicro, bg, odate, ddate)]
        #cur.bindarraysize = 1
        #cur.setinputsizes(int, 50, 50, 50, int, int, int, int, int, 50, 50)

        print(stmt)
        cur.execute(stmt)
        con.commit()

    return render_template('edit-order.html',order=order)

@app.route('/delete/<id>', methods=['GET','POST'])
def delete_order(id):
    id=id
    cur=con.cursor()
    if request.method == 'POST':
        #delete statement
        stmt= "delete from CORDER where OID="+str(id)
        cur = con.cursor()
        print(stmt)
        cur.execute(stmt)
        con.commit()
    print(id)
    return render_template('delete-order.html',id=id)

# run the application
if __name__ == '__main__':
    app.run()
