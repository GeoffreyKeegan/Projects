from flask import Flask
from flask import render_template, request
from flask import flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from user import User

import json
import requests

user_url = 'https://user-service-dattafish.azurewebsites.net/api/user/'
user_func_key = 'e8UuFlzFUwk4p6Sa2gWiF3PI7OsS0HrDa-kAySzarJ-KAzFuBSphfA=='

catch_url = 'https://catch-service-dattafish.azurewebsites.net/api/catch/'
catch_func_key = '62OlbQRVlewvBF27BGmbqTiWbt27do3EhbHTix6GSVuzAzFu2-erjQ=='

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



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
        flash("username or password missing")
        return redirect(url_for('user_create'))
   
    res = requests.post(user_url,params={
        'code':user_func_key}, json={
            'username':un,
            'password':pw
        })
    flash(f'created user {res.text}')
    return redirect(url_for('login', user_id=res.text))


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

    uid = request.form.get('user_id')
    if (user_id != uid):
        flash("incorrect user_id")
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
            flash('logged in')
            return redirect(url_for('index'))
        else:
            flash('login unsuccessful')
            return redirect(url_for('login'))
        
    else:
        flash('username or password missing')
        return redirect(url_for('login'))
    
    
# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out')
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
        flash("missing parameter")
        return redirect(url_for('catch_create'))
   
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
    
    flash(f'created catch')
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
        return render_template('catch-listing.html', user=u)


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
    
    flash("catch updated")
    return redirect(url_for('read_catches', user_id=user_id, catch_id=catch_id))


# DELETE
@app.post('/<user_id>/catches/<catch_id>/delete')
def catch_delete(user_id, catch_id):

    cid = request.form.get('catch_id')
    if (catch_id != cid):
        flash("incorrect catch ID")
        return redirect(url_for('read_catches', user_id=user_id, catch_id=catch_id))
    

    requests.delete(catch_url+catch_id, params={'code': catch_func_key})

    requests.delete(user_url+user_id+"/catches", params={'code': user_func_key}, json={
            'uid': user_id,
            'cid': cid
        })

    return redirect(url_for('read_catches', user_id=user_id, catch_id=""))



#------Data_Tracker------#

# Data Create
@app.route('/<user_id>/catches/data',methods=['GET', 'POST'])
def data_track(user_id):

    if request.method=='GET':
        return render_template('data-query.html')

    q1 = request.form.get('q1')
    q2_name = request.form.get('q2_name')
    q2_value = request.form.get('q2_value')
    q2 = (q2_name, q2_value)

    if not(q2_value):
        flash("missing name")
        return redirect(url_for('data_track', user_id=user_id))
    
    res = requests.get(user_url+user_id,
                       params = {"code" : user_func_key})
    #print(res.status_code,res.text)

    u = json.loads(res.text)

    cids = u.get("catches")
   
    res = requests.get(catch_url+"/data",params={
        'code':catch_func_key}, json={
            'cids':cids,
            'q1':q1,
            'q2':q2
        })
    
    data = json.loads(res.text)

    return render_template('data-listing.html', data=data, q2=q2, q1=q1)

