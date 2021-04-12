from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import pre_process as pp
import psycopg2
import random
import string
import os
app=Flask(__name__)
app.secret_key=os.urandom(24)

global zip_code


ENV='dev'

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:55555@localhost/answers'
else:    
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']=''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    if request.method=='POST':
        return render_template('index.html')    


@app.route('/question1',methods=['POST','GET'])
def question1():
    if 'username' in session:
        if request.method=='POST':
            return render_template('question1.html')
        else:
            return redirect('/')    
    else:
        return redirect('/')
@app.route('/question2',methods=['POST','GET'])
def question2():
    if 'username' in session:
        if request.method=='POST':
            if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
            return render_template('question2.html')
        else:
            return redirect('/')
    else:
        return redirect('/')
@app.route('/question3',methods=['POST'])
def question3():
    if request.method=='POST':
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        return render_template('question3.html')

@app.route('/question4',methods=['POST'])
def question4():
    if request.method=='POST':
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        return render_template('question4.html')

@app.route('/question5',methods=['POST'])
def question5():
    if request.method=='POST':
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        return render_template('question5.html')    

@app.route('/question6',methods=['POST'])
def question6():
    if request.method=='POST':
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        return render_template('question6.html')        
@app.route('/question7',methods=['POST'])
def question7():
    if request.method=='POST':
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        return render_template('question7.html')        
@app.route('/suggestion',methods=['POST'])
def suggestion():
    if request.method=='POST':
        # zip="L5V 2C9"
        if(request.form.get("emerge")=="YES"):
                return render_template('emergency.html')
        global zip_code
        result=pp.find_nearby_vaccine(zip_code)
        results=result.values.tolist()
        return render_template('suggestion.html',hospital=results)
        # return render_template('suggestion.html', tables=[result.to_html(classes='data')], titles= 'Approximate distance from your location')   
@app.route('/login',methods=['POST','GET'])
def login():
        userid=request.form.get("userID")
        password=request.form.get("password")

        global zip_code
        zip_code=request.form.get("zipCode")
        try:
            mycursor=db.session.execute("SELECT * FROM userdb WHERE userid = :id AND password = :pass", {'id': userid,'pass':password})
            fetched = mycursor.fetchone()
            if (fetched[0]==userid and fetched[1]==password):
                session['username']=userid
                db.session.execute("UPDATE userdb set zip= :pincode WHERE userid=:id",{'pincode':zip_code,'id':userid})
                db.session.commit()
    
                return render_template('question1.html')
            else:
                return render_template('index.html',message="Invalid Credentials") 
        except:
            return render_template('index.html') 
   
@app.route('/thank',methods=['POST'])
def thank():
    fid=request.form.get("subject")
    if(request.form.get("Logout")=="Logout"):
                return redirect('/logout')

    
    alpha = string.ascii_uppercase
    otp=''.join(random.choice(alpha) for i in range(6))
    email=session['username']
    db.session.execute("UPDATE userdb set otp= :otp WHERE userid=:id",{'otp':otp,'id': session['username']})
    db.session.commit()
    pp.send_mail(fid,otp,email)
    email=email.replace(email[2:-4],"*"*(len(email)-6))
    return render_template('thank.html',otp=otp,email=email) 

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username',None)
    return redirect('/')

@app.route('/register',methods=['POST','GET'])
def register():
    userid=request.form.get("userID")
    password=request.form.get("password")
    cpassword=request.form.get("cpassword")
    if(password!=cpassword):
        return render_template('index2.html')

    try:
        mycursor=db.session.execute("SELECT * FROM userdb WHERE userid = :id",{'id': userid})
        # fetched = mycursor.fetchone()
        if (mycursor is None):
            return render_template('/')
        else:
            
            session['username']=userid
            db.session.execute("INSERT INTO userdb(userid,password) VALUES(:userid,:password)",{'userid':userid,'password':password})
            db.session.commit()
            return render_template('/index') 
    except:
        return render_template('index.html') 

@app.route('/index2',methods=['POST','GET'])
def index2():
    return render_template('index2.html')   

@app.route('/emergency',methods=['POST','GET'])
def emergency():
    return render_template('emergency.html')
if __name__=='__main__':
    app.run(debug=True)