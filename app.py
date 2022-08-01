from flask import Flask, request, jsonify , render_template , redirect , Response , send_file
from sheets import *
import datetime
DateTime==4.5
app = Flask(__name__)

info = {}
fdata = []
dumtext = {'Card':{
        'title': '`Title: this is a card title`',
        'text': 'This is the body text of a card.  You can even use line\n  breaks and emoji! 💁',
        'buttonText': 'Click me',
        'buttonUrl': 'https://assistant.google.com/'
    }}

@app.route('/')
def index():
    return '<h1>Hellow</h1>'



@app.route('/api', methods=['GET', 'POST'])
def api():
    print('requested --------------------------------------------------')
    data = request.get_json()
    print(data)
   
    intent = data['queryResult']['intent']['displayName']
    print(intent)
    


    if intent == 'Default Welcome Intent - name - custom':
        name = data['queryResult']['parameters']['person']['name']
        print(f'This is the name: {name}')
        info['name'] = name
        fdata.append(name)
        fdata.append(datetime.datetime.now())
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent - url':
        print
        url = data['queryResult']['parameters']['url']
        print(f'This is the url: {url}')
        info['url'] = url
        fdata.append(url)
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent -email':
        email = data['queryResult']['parameters']['email']
        print(f'This is the email: {email}')
        info['email'] = email
        fdata.append(email)
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent-service':
        service = data['queryResult']['queryText']
        print(f'This is the service: {service}')
        info['service'] = service
        fdata.append(service)
        return jsonify(dumtext)
    elif intent == 'Default Welcome Intent-phno':
        print('...............................................')
        phno = data['queryResult']['parameters']['phone-number']
        print(f'This is the phno: {phno}')
        info['phno'] = phno
        fdata.append(phno)
        print('+++++++++++++++++++++++++++++++++++++++')
        print(info)
        insert_data(fdata)
        print('+++++++++++++++++++++++++++++++++++++++')
        return jsonify(dumtext)


if __name__ == "__main__":
    app.run(debug=True)
    