from flask import Flask,request
import datetime as datedatedate
from datetime import datetime
import pyrebase
from flask_cors import CORS

import numpy as np
import pandas as pd



app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
config = {"apiKey": "AIzaSyCQlJNxtcp_ambo4mGWH9LxhK6Wsr3VlSM",
          "authDomain": "projectbase-1fca0.firebaseapp.com",
          "databaseURL": "https://projectbase-1fca0-default-rtdb.europe-west1.firebasedatabase.app",
          "projectId": "projectbase-1fca0",
          "storageBucket": "projectbase-1fca0.appspot.com",
          "messagingSenderId": "821113244030",
          "appId": "1:821113244030:web:1f86f63dfbba3d08c4cb2f",
          "measurementId": "G-J76JKQ1XX5"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/listhistorical', methods=['POST', 'GET'])
def listhistorical():
    if request.method == 'GET':
        symbol = request.args.get('symbol')
        alldates = []
        thedictionary = dict()
        symbol = symbol.split(',')
        for symb in symbol:

            dic = db.child('realhistorical').child(str(symb).strip().upper()).get().val()
            df = pd.DataFrame()
            for key in dic.keys():
                df[key] = dic[key]

            # In[3]:

            df = df.drop(columns=['change', 'high', 'low', 'open', 'vol'])

            # In[4]:

            def fixdate(date):
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                first = date.split(' ')
                for i in range(len(months)):
                    if first[0] == months[i]:
                        first[0] = str(i + 1)
                first[1] = first[1].replace(',', '')
                date = [int(first[2]), int(first[0].replace(' ', '')), int(first[1])]
                return datetime(date[0], date[1], date[2])

            # In[5]:

            df['newdate'] = df['date'].apply(fixdate)
            df['price'] = df['price'].apply(float)
            df.set_index('newdate', inplace=True)
            del (df['date'])
            df.sort_index(inplace=True)
            r = pd.date_range(start=datetime(2013, 1, 1), end=datedatedate.date.today())
            df = df.reindex(r).fillna(np.nan).rename_axis('date').reset_index()
            if len(alldates) == 0:
                alldates = df['date']
            newlst = []
            for s in df['price']:
                if s is not np.nan:
                    newlst.append(str(s))
                else:
                    newlst.append(np.nan)
            df['price'] = newlst
            thedictionary[symb.upper()] = []
            for e in df['price']:
                thedictionary[symb.upper()].append(e)
        thedictionary['date'] = []
        for e in alldates:
            thedictionary['date'].append(str(e).split(' ')[0])

        # df['price']=df['price'].apply(str)
        # dic=dict()
        # dic['date']=[]
        # dic['price']=[]
        # for key in df.keys():
        # for i in df.index:
        # if key=="date":
        # dic[key].append(str(df[key][i]).split(' ')[0])
        # else:
        # dic[key].append(df[key][i])

        return thedictionary


if __name__ == '__main__':
    app.run()
