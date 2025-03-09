from flask import Flask
from flask import render_template, request
from flask import flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from user import User

import json
import requests

# user_url = None
# user_func_key = None

# catch_url = None
# catch_func_key = None

app = Flask(__name__)
app.secret_key = None



# Home Page
@app.route("/")
def index():
    return render_template('index.html')



#------USER_CRUD------#

# CREATE
@app.route('/users/create',methods=['GET', 'POST'])
def user_create():

    if request.method=='GET':
        return render_template('user-create.html')

    un = request.form.get('username')
    pw = request.form.get('password')

    if not(un and pw):
        flash('ERROR: Username or Password is Missing')
        return redirect(url_for('user_create'))
   
    res = requests.post(user_url,params={
        'code':user_func_key}, json={
            'username':un,
            'password':pw
        })
    
    if res.status_code == 401:
        flash(f'{res.text}')
        return redirect(url_for('user_create'))

    user = User.authenticate(un,pw)

    login_user(user)
    return redirect(url_for('index'))


# READ
@app.route('/users/<user_id>')
def user_view(user_id=""):

    res = requests.get(user_url+user_id,
                       params = {"code" : user_func_key})
    #print(res.status_code,res.text)


    u = json.loads(res.text)
    return render_template('user-detail.html',user=u)


# UPDATE
@app.post('/users/<user_id>')
def user_update(user_id=""):

    res = requests.get(user_url+user_id, params = {"code" : user_func_key})
    us = json.loads(res.text)

    password = us.get('password')
    oldpass = request.form.get('old_password')
    newpass0 = request.form.get('new_password0')
    newpass1 = request.form.get('new_password1')

    if not (oldpass and newpass0 and newpass1):
        flash("all fields must be entered")
        return redirect(url_for('user_view', user_id=user_id))

    if oldpass == newpass0:
        flash("new password cannot be the same as the old password")
        return redirect(url_for('user_view', user_id=user_id))

    if newpass0 != newpass1:
        flash("new passwords do not match")
        return redirect(url_for('user_view', user_id=user_id))
    
    
    # Need to check if old password is correct
    if oldpass != password:
        flash("enter correct old password")
        return redirect(url_for('user_view', user_id=user_id))
    
    
    requests.put(user_url+user_id, params={'code': user_func_key}, json={'password': newpass0})
    flash("user password updated")
    return redirect(url_for('user_view', user_id=user_id))
    

# DELETE
@app.post('/users/<user_id>/delete')
def user_delete(user_id):

    res = requests.get(user_url+user_id,
                params = {"code" : user_func_key})
    password = json.loads(res.text).get("password")

    pw = request.form.get('password')
    if (pw != password):
        flash("Incorrect Password")
        return redirect(url_for('user_view', user_id=user_id))
    

    requests.delete(user_url+user_id, params={'code': user_func_key})
    return redirect(url_for('index'))



#------AUTHENTICATION------#

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')

    # TODO: get form data and validate
    un = request.form.get('username')
    pw = request.form.get('password')

    if (un and pw):

        ## authenticate
        user = User.authenticate(un,pw)

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful: Username or Password incorrect')
            return redirect(url_for('login'))
        
    else:
        flash('ERROR: Username or Password is Missing')
        return redirect(url_for('login'))
    
    
# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print('loading user')
    return User.get(user_id)




#------CATCH_CRUD------#

# CREATE
@app.route('/<user_id>/catches/create',methods=['GET', 'POST'])
def catch_create(user_id):

    if request.method=='GET':
        return render_template('catch-create.html')

    sp = request.form.get('species')
    wt = request.form.get('weight')
    lo = request.form.get('location')
    lu = request.form.get('lure')
    tm = request.form.get('time')


    if not(sp and wt and lo and lu and tm):
        flash("Error: Missing at least one of the Data Inputs")
        return redirect(url_for('catch_create', user_id=user_id))
   
    res = requests.post(catch_url,params={
        'code':catch_func_key}, json={
            'species':sp,
            'weight':wt,
            'location': lo,
            'lure': lu,
            'time': tm
        })
    cid = res.text
    
    requests.post(user_url+user_id+"/catches",params={
        'code':user_func_key}, 
        json={
            'cid' : cid
            })
    
    return redirect(url_for('read_catches', user_id=user_id, catch_id=cid))


# READ
@app.route('/<user_id>/catches/')
@app.route('/<user_id>/catches/<catch_id>')
def read_catches(user_id, catch_id=""):

    res = requests.get(user_url+user_id,
                       params = {"code" : user_func_key})
    #print(res.status_code,res.text)

    u = json.loads(res.text)


    if catch_id == "":
        catches = []
        for c in u.get("catches"):
            res = requests.get(catch_url+c,
                params = {"code" : catch_func_key})
            catches.append(json.loads(res.text))
        return render_template('catch-listing.html', user=u, catches=catches)


    res = requests.get(catch_url+catch_id,
                       params = {"code" : catch_func_key})
    #print(res.status_code,res.text)


    c = json.loads(res.text)
    return render_template('catch-detail.html',catch=c, user=u)


# UPDATE
@app.route('/<user_id>/catches/<catch_id>/edit', methods=['GET','POST'])
def catch_update(catch_id, user_id):

    res = requests.get(catch_url+catch_id,
                    params = {"code" : catch_func_key})
    
    c = json.loads(res.text)

    if request.method=='GET':
        return render_template("edit-catch.html", catch=c)

    sp = request.form.get('species')
    wt = request.form.get('weight')
    lo = request.form.get('location')
    lu = request.form.get('lure')
    tm = request.form.get('time')


    if not(sp and wt and lo and lu and tm):
        flash("missing parameter")
        return redirect(url_for('catch_update', catch_id=catch_id, user_id=user_id))
    

    requests.put(catch_url+catch_id,params={'code':catch_func_key}, json={"species":sp})

    requests.put(catch_url+catch_id,params={'code':catch_func_key}, json={"weight":wt})

    requests.put(catch_url+catch_id,params={'code':catch_func_key}, json={"location":lo})

    requests.put(catch_url+catch_id,params={'code':catch_func_key}, json={"lure":lu})    

    requests.put(catch_url+catch_id,params={'code':catch_func_key}, json={"time":tm})   
    
    flash("Catch Updated")
    return redirect(url_for('read_catches', user_id=user_id, catch_id=catch_id))


# DELETE
@app.post('/<user_id>/catches/<catch_id>/delete')
def catch_delete(user_id, catch_id):

    res = requests.get(user_url+user_id,
                params = {"code" : user_func_key})
    password = json.loads(res.text).get("password")

    pw = request.form.get('password')
    if (pw != password):
        flash("Incorrect Password")
        return redirect(url_for('read_catches', user_id=user_id, catch_id=catch_id))
    

    requests.delete(catch_url+catch_id, params={'code': catch_func_key})

    requests.delete(user_url+user_id+"/catches", params={'code': user_func_key}, json={
            'uid': user_id,
            'cid': catch_id
        })

    return redirect(url_for('read_catches', user_id=user_id, catch_id=""))



#------Data_Tracker------#

# Data Track
@app.route('/<user_id>/catches/data',methods=['GET', 'POST'])
def data_track(user_id):

    if request.method=='GET':
        return render_template('data-query.html')
    

    q1 = request.form.get('q1')
    q2_name = request.form.get('q2_name')
    q2_value = request.form.get('q2_value')
    q2 = (q2_name, q2_value)


    if not(q2_value):
        flash("Missing Name")
        return redirect(url_for('data_track', user_id=user_id))
    
    res = requests.get(user_url+user_id,
                       params = {"code" : user_func_key})
    #print(res.status_code,res.text)

    u = json.loads(res.text)

    cids = u.get("catches")
    if (len(cids) == 0):
        flash("You have no Catches to Track")
        return redirect(url_for('data_track', user_id=user_id))
    
   
    res = requests.post(catch_url+"data",
                        params = {"code" : catch_func_key},
                        json={"cids": cids, "q1" : q1, "q2": q2})
    
        
    data = json.loads(res.text)

    data_track = []

    if q1 == 'weight':
        for d in data:
            info = []
            res = requests.get(catch_url+d[1],
                params = {"code" : catch_func_key})
            info.append(d[0])
            info.append(json.loads(res.text))
            data_track.append(info)       
    else:
        for d in data:
            info = []
            catches = []
            for c in d[0]:
                res = requests.get(catch_url+c,
                    params = {"code" : catch_func_key})
                catches.append(json.loads(res.text))
            info.append(catches)
            info.append(d[1])
            data_track.append(info)




    return render_template('data-listing.html', data=data_track, q2=q2, q1=q1)

