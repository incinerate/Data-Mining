import csv
from sklearn.neural_network import MLPClassifier 
from sklearn.ensemble import RandomForestClassifier
import datetime
import time
from astropy.units import second
import sklearn
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
 
 
X_test = csv.reader(open('activity_log.csv'))
UserCourse = csv.reader(open('enrollment_list.csv'))
Y_test = csv.reader(open('activity_log.csv'))
 
 
figures = ['access','navigate','problem','wiki','video','discussion','page_close','time']
def readCVStoDic(X):
    event = row[-1];
    if(X.has_key(row[-1])):
        X[event] = X.get(event) + 1;
    else:
        X[event] = 1;
    pass
 
 
data = [];
i = 1;
X={};
 
clickTimes = {}
Users_S={}
Courses_S = {}
UCdata=[]
 
def initializeX():
    for ele in figures:
        X[ele] = 0
    return X
 
def getTimeDiff(timeStra,timeStrb):
    if timeStra<=timeStrb:
        return 0
    ta = time.strptime(timeStra, "%Y-%m-%dT%H:%M:%S")
    tb = time.strptime(timeStrb, "%Y-%m-%dT%H:%M:%S")
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)
    secondsDiff=(dataTimea-dataTimeb).total_seconds()
  
    minutesDiff=round(secondsDiff/60,1)
    return minutesDiff;
 
id1 = 1
for row in UserCourse:
    if row[1]=='user_id':
        continue
    UCdata.append(row)
    Cid = row[2]
    if Courses_S.has_key(Cid):
        Courses_S[Cid] = Courses_S.get(Cid)
        Users_S[Cid] = Users_S.get(Cid)+1
    else:
        Courses_S[Cid] = id1
        Users_S[Cid] = 1
        id1 = id1 +1
 
for k in Y_test:
    if(k[0]=='enrollment_id'):
        continue
    courseId = Courses_S.get(UCdata[int(k[0])-1][2])
#     print courseId
    if clickTimes.has_key(courseId):
        clickTimes[courseId] = clickTimes.get(courseId)+1
    else:
        clickTimes[courseId] = 1
 
print clickTimes
start = True
endtime = '2014-05-31T12:43:20'
lastTime = 0
 
for row in X_test:
    if(row[-1]=='event'):
        X = initializeX()
        continue
    if(int(row[0]) == i):
        readCVStoDic(X)
        if start:
            X['Erollment_time'] = 1
            start = False
        else:
            if getTimeDiff(row[1], lastTime) < 240:
                X['time'] = getTimeDiff(row[1], lastTime) + X.get('time')
            else :
                X['Erollment_time'] = X.get('Erollment_time') + 1
        lastTime = row[1]
         
        X['course_id'] = Courses_S.get(UCdata[i-1][2])
        X['users'] = Users_S.get(UCdata[i-1][2])
        averageClick = float(clickTimes.get(Courses_S.get(UCdata[i-1][2]))) /float(X.get('users'))
        click = float(X.get('access'))+float(X.get('navigate'))+float(X.get('problem'))+float(X.get('wiki'))+float(X.get('video'))+float(X.get('discussion'))+float(X.get('page_close'))
        X['ave_clickTime'] = click-averageClick
    else:
        i=i+1
        temp = {}
        temp.update(X)
        data.append(temp)
        X.clear()
        X = initializeX()
        readCVStoDic(X)
        startTime = row[1]
        X['Erollment_time'] = 1
        X['course_id'] = Courses_S.get(UCdata[i-1][2])
        X['users'] = Users_S.get(UCdata[i-1][2])
        averageClick = float(clickTimes.get(Courses_S.get(UCdata[i-1][2]))) /float(X.get('users'))
        click = float(X.get('access'))+float(X.get('navigate'))+float(X.get('problem'))+float(X.get('wiki'))+float(X.get('video'))+float(X.get('discussion'))+float(X.get('page_close'))
        X['ave_clickTime'] = click-averageClick
temp = {};
temp.update(X);
data.append(temp);
 
# print data
firstline = True;
   
A = []
B = []
A2 = []
id = 1
 
 
 
with open('train_label.csv') as f:
    for l in f:
        l = l.replace('\n', '')
        if firstline:
            firstline = False;
            l = l.replace('"', "")
            features = l.split(",")
        else:
            a = data[id -1]
            b = a.values()
            A.append(b)
            B.append(l.split(",")[-1])
            id = id + 1 
print A;
   
while(id!=len(data)+1):
    a = data[id -1]
    b = a.values()
    A2.append(b)
    id = id + 1
       
# clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
# clf = RandomForestClassifier(n_estimators=50)
clf = GradientBoostingClassifier(n_estimators=1000)
clf.fit(A, B)
result = clf.predict_proba(A2)
      
with open('results.csv','wb') as f:
    writer = csv.writer(f)
    writer.writerow(["enrollment_id","dropout_prob"])
    rid=72326
    for row in result:
        writer.writerow([rid,row[1]])
        rid = rid+1
print result
