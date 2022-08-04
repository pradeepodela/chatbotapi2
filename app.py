from flask import Flask, request, jsonify , render_template , redirect , Response , send_file
import pandas as pd
from db import *
from datetime import date , datetime
app = Flask(__name__)
df = pd.read_csv('data.csv')
info = {}
dataupdate = {}
fdata = []
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
        database2(struct)
        
        #updater(info)
        #print('+++++++++++++++++++++++++++++++++++++++')
        return jsonify(dumtext)
@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLAKSY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning('Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration,
                query.context))
    return response

if __name__ == "__main__":
    app.run(debug=True) 
    
