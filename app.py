from flask import Flask, app,render_template,request,redirect
from logging import debug
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import mysql.connector


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Mytable(db.Model):
    sno=db.Column(db.Integer,primary_key = True)
    month=db.Column(db.String(50),nullable = False)
    totalunit = db.Column(db.Integer,nullable = False)
    ownerunit = db.Column(db.Integer,nullable = False)
    ourunit = db.Column(db.Integer,nullable = False)
    totalamount = db.Column(db.Integer,nullable = False)
    ouramount =db.Column(db.Integer,nullable = False)
    owneramount = db.Column(db.Integer,nullable = False)	
@app.route('/',methods=["GET","POST"])
def home():
     if request.method=="POST":
        print("post")
        month = request.form.get("mont")
        total_unit = request.form.get("totalunit")
        owner_unit = request.form.get("ownerunit")
        our_unit= request.form.get("ourunit")
        total_bill = request.form.get("totalbill")
        our_amount= request.form.get("branchamount")
        owner_amount = request.form.get("owneramount")
        Entry = Mytable(month=month,totalunit=total_unit,ownerunit=owner_unit,ourunit=our_unit,totalamount=total_bill,ouramount=our_amount,owneramount=owner_amount)
        db.session.add(Entry)
        db.session.commit()
     alldata = Mytable.query.all()
     return render_template("home.html",alldata=alldata)
     #return render_template("home.html")
'''@app.route('/show', methods=['GET', 'POST'])
def showData():
       alldata = Mytable.query.all()
       return render_template("data.html",alldata=alldata)'''


@app.route('/delete/<int:sno>')
def delete(sno):
       DeleteData= Mytable.query.filter_by(sno=sno).first()
       db.session.delete(DeleteData)
       db.session.commit()
       return redirect("/")
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
   if request.method=="POST":
        month = request.form.get("mont")
        total_unit = request.form.get("totalunit")
        owner_unit = request.form.get("ownerunit")
        our_unit= request.form.get("ourunit")
        total_bill = request.form.get("totalbill")
        our_amount= request.form.get("branchamount")
        owner_amount = request.form.get("owneramount")
        #mytable ke all content ko query kiya sno filter kr ke aur ek variable me store kiya
        DataUpdate = Mytable.query.filter_by(sno=sno).first()
        #variable jisme store kiya tha usme uske table by table section me wo data store kr rhe jo hm form se utha rhe h
        DataUpdate.month=month
        DataUpdate.totalunit=total_unit
        DataUpdate.ownerunit=owner_unit
        DataUpdate.ourunit=our_unit
        DataUpdate.totalamount=total_bill
        DataUpdate.ouramount=our_amount
        DataUpdate.owneramount=owner_amount
        #ab database me add fir commit
        db.session.add(DataUpdate)
        db.session.commit()
        return redirect("/")
        #return render_template("data.html")
   DataUpdate = Mytable.query.filter_by(sno=sno).first()
   return render_template("update.html",DataUpdate=DataUpdate)
@app.route('/result', methods=['GET', 'POST'])
def search():
   if request.method=="POST":
      search_val =  request.form.get("search")
      search = "%{0}%".format(search_val)
      results = Mytable.query.filter(Mytable.month.like(search)).all()
      return render_template("data.html",allresults=results)
   else:
      return render_template("data.html")


if __name__=="__main__":
    app.run()
