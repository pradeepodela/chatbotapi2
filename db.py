import pyrebase
from datetime import date , datetime
import pandas as pd
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

print('configering.....')

firebase = pyrebase.initialize_app(cfg)
print('app configered')
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
        print(df)
        dflist.append(df)
    fdf = pd.concat(dflist, ignore_index = True)
    # print('-----------------------******---------------------------')
    # print(fdf)
    fdf.to_csv('data.csv')
    # print('-----------------------------------------------------')
#### CREATING YOUR OWN USER ID ######
def database2(data):
    

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


#print(str(datetime.now().strftime("%H:%M:%S")))
struct = {
        'date': str(datetime.now().strftime("%Y-%m-%d")),
        'time': str(datetime.now().strftime("%H:%M:%S")),
        'name':'hellow',
        'url':'www.hellow.com',
        'email':'hellow@googel.com',
        'phno':'90090909090',
        'service':'h8il'


    }

#print(struct)
#database2(struct)

        
        

#dataupdate = dataupdate[str(date.today())][str(datetime.now())] = {}
#print(dataupdate)
