from flask import Flask, request, jsonify , render_template , redirect , Response , send_file
import pandas as pd
import pyrebase
# from db import *
from datetime import date , datetime
app = Flask(__name__)
df = pd.read_csv('data.csv')
info = {}
dataupdate = {}
fdata = []
dflist = []
dataupdate = {}
cfg = {
    'apiKey': "AIzaSyBwRBcKz9DC68UVsMBygkANr_QixS0ZaKA",
    'authDomain': "mypy-19226.firebaseapp.com",
    'databaseURL':'https://mypy-19226-default-rtdb.firebaseio.com/',
    'projectId': "mypy-19226",
    'storageBucket': "mypy-19226.appspot.com",
    'messagingSenderId': "990787705081",
    'appId': "1:990787705081:web:ab15b33b11bbea973dea28",
    'measurementId': "G-298F64SX86"

}

dumtext = {'Card':{
        'title': '`Title: this is a card title`',
        'text': 'This is the body text of a card.  You can even use line\n  breaks and emoji! 💁',
        'buttonText': 'Click me',
        'buttonUrl': 'https://assistant.google.com/'
    }}
struct = {
        'date': str(datetime.now().strftime("%Y-%m-%d")),
        'time': str(datetime.now().strftime("%H:%M:%S")),
        'name':'',
        'url':'',
        'email':'',
        'phno':'',
        'service':''


    }
firebase = pyrebase.initialize_app(cfg)
db = firebase.database()
auth = firebase.auth()
Storage = firebase.storage()
def get_db():

    data = db.child('data').child('leadsinfo').get() 

    for person in data.each():
        # print('/**//*////**//*/*/*//**/*/*//*/*/*///*/*/*/*/*/*//*/*/*//*/*/*/')
        # print(person.val())
        # print(person.key())
        df = pd.DataFrame(person.val())
        df = df.T
        # print(df)
        dflist.append(df)
    fdf = pd.concat(dflist, ignore_index = True)
    # print('-----------------------******---------------------------')
    # print(fdf)
    fdf.to_csv('data.csv')
    # print('-----------------------------------------------------')
#### CREATING YOUR OWN USER ID ######
def database2(data):
    if data['date'] != str(datetime.now().strftime("%Y-%m-%d")):
        data['date'] = str(datetime.now().strftime("%Y-%m-%d"))
    if data['time'] != str(datetime.now().strftime("%H:%M:%S")):
        data['time'] = str(datetime.now().strftime("%H:%M:%S"))
    db.child('data').child('leadsinfo').child(str(datetime.now().strftime("%Y-%m-%d"))).child(str(datetime.now().strftime("%H:%M:%S"))).set(data)
    print('successfully pushed data')
    get_db()
    fdf = pd.concat(dflist, ignore_index = True)
    # print('-----------------------------------------------------')
    # print(fdf)
    # print('-----------------------------------------------------')
def get_specfic(date):
    data = db.child('data').child('leadsinfo').child(str(date)).get() 
    # print('++++++++++++++++++++++++++++++++++++++++++++++++Specfic++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # print(date)
    # print(data.val())
    df = pd.DataFrame(data.val())
    df = df.T
    df.reset_index(drop=True, inplace=True)
    # print(df)
    
    return df
# print(date.today())
# print(datetime.now())
# print(dataupdate[str(date.today())][str(datetime.now())])

#@app.route('/')
@app.route("/index")
def index():

    with open("tempdata.csv") as file:
        return render_template('index.html', csv=file)




@app.route('/', methods=['POST', 'GET'])
def check():
    return render_template('login.html')




@app.route('/date', methods=['POST', 'GET'])
def date():
    return render_template('edit_user.html')




@app.route('/viewwhole', methods=['POST', 'GET'])
def viewwhole():
    get_db()
    with open("data.csv") as file:
        return render_template('viewwhole.html', csv=file)





@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        if username == 'admin' and password == 'admin':
            return render_template('result.html')
        else:
            return render_template('result.html')
    else:
        return render_template('login.html')



@app.route('/select', methods=['POST', 'GET'])
def select():
    if request.method == 'POST':
        print('****************************************************')
        print(request.form['uname'])
        rest = get_specfic(request.form['uname'])
        rest = pd.DataFrame(rest)
        rest.to_csv('tempdata.csv')
        print('****************************************************')

        return redirect('/index')
    else:
        return render_template('select.html')  

get_db()
@app.route('/downloadcsv', methods=['GET'])
def downloadcsv():
    if request.method=='GET':
        get_db()
        return send_file('data.csv', attachment_filename='data.csv', as_attachment=True)
@app.route('/specfic', methods=['GET'])
def specfic():
    if request.method=='GET':
        return send_file('tempdata.csv', attachment_filename='tempdata.csv', as_attachment=True)




@app.route('/api', methods=['GET', 'POST'])
def api():
    print('requested --------------------------------------------------')
    data = request.get_json()
    #print(data)
   
    intent = data['queryResult']['intent']['displayName']
    #print(intent)
    


    if intent == 'Default Welcome Intent - name - custom':
        name = data['queryResult']['parameters']['person']['name']
        print(f'This is the name: {name}')
        struct['name'] = name
        
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent - url':
        
        url = data['queryResult']['parameters']['url']
        print(f'This is the url: {url}')
        struct['url'] = url
        
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent -email':
        email = data['queryResult']['parameters']['email']
        print(f'This is the email: {email}')
        struct['email'] = email
        
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent-service':
        service = data['queryResult']['queryText']
        print(f'This is the service: {service}')
        struct['service'] = service
        
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent-phno':
        print('...............................................')
        phno = data['queryResult']['parameters']['phone-number']
        print(f'This is the phno: {phno}')
        struct['phno'] = phno
        
        #print('+++++++++++++++++++++++++++++++++++++++')
        #print(info)
        if len(struct['service']) <3:
            struct['service'] = service
        if len(struct['name']) <3:
            struct['name'] = name
        if len(struct['url']) <3:
            struct['url'] = url
        if len(struct['email']) <3:
            struct['email'] = email
        if len(struct['phno']) <3:
            struct['phno'] = phno
        if struct['date'] != str(datetime.now().strftime("%Y-%m-%d")):
            struct['date'] = str(datetime.now().strftime("%Y-%m-%d"))
        if struct['time'] != str(datetime.now().strftime("%H:%M:%S")):
            struct['time'] = str(datetime.now().strftime("%H:%M:%S"))
        try:
            database2(struct)
        except:
            if struct['date'] != str(datetime.now().strftime("%Y-%m-%d")):
                struct['date'] = str(datetime.now().strftime("%Y-%m-%d"))
            if struct['time'] != str(datetime.now().strftime("%H:%M:%S")):
                struct['time'] = str(datetime.now().strftime("%H:%M:%S"))
            struct['service'] = service
            struct['name'] = name
            struct['url'] = url
            struct['email'] = email
            struct['phno'] = phno

            database2(struct)
        
        #updater(info)
        #print('+++++++++++++++++++++++++++++++++++++++')
        return jsonify(dumtext)


if __name__ == "__main__":
    app.run(debug=True) 
    