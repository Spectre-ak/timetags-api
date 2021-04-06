import json
import time
import uuid
import requests
import pandas as pd

labels=pd.read_csv("sampled-cliff_people-20210402142827.csv")['label']
label_formatted=[]
for i in labels:
    try:
        print(i)
        label_formatted.append(urllib.parse.quote_plus(i))
    except Exception as e:
        continue

        
        
# Making nyt request

baseUrl="https://api.nytimes.com/svc/semantic/v2/concept/suggest?query="
params="&filter=Per&max=1000&api-key=xxxxxxxx"
LabelWithTags={}
count=0
maxAtATime=0
for i in label_formatted[99:]:
    maxAtATime=maxAtATime+1
    
    url=baseUrl+i+params
    response=requests.get(url)
    jsonData=json.loads(response.text)
    #print(jsonData)
    LabelWithTags[jsonData[0]]=jsonData[1]
    #print(LabelWithTags)
    count=count+1
    print(count)
    if count==10:
        count=0
        time.sleep(12)
    time.sleep(3)
with open('LabelWithTags2.json', 'w') as json_file:
    json.dump(LabelWithTags, json_file)

f = open('LabelWithTags2.json',)
data = json.load(f)
result={}
for key in data:
    print(key)
    ID=str(uuid.uuid1())
    ID=ID.replace("-","")
    l1={"data":data[key],"similarTags":[],"id":ID}
    #print(l1)
    if len(l1["data"])==0:
        continue
    
    for i in data:
        if i == key:
            continue
        currList=data[i]
        if len(currList)==0:
            continue
        
        if len(l1["data"])>len(currList):
            no=0
            for j in currList:
                if j in l1["data"]:
                    no=no+1
            if no>0 and no>=len(currList)/2:
                #print("Added "+i)
                #print()
                for j in currList:
                    if j not in l1["data"]:
                        l1["data"].append(j)
                #print("new list {}".format(l1))
                data[i]=[]
                l1["similarTags"].append(i)
        else:
            no=0
            for j in l1["data"]:
                if j in currList:
                    no=no+1
            #print(currList)
            
            #print("no else {}".format(no))
            if no>0 and no>=len(l1["data"])/2:
                #print("Added "+i)
                #print()
                for j in currList:
                    if j not in l1["data"]:
                        l1["data"].append(j)
                #print("new list {}".format(l1))
                data[i]=[]
                l1["similarTags"].append(i)
    
    result[key]=l1
    #break

with open('tagsMapped.json', 'w') as json_file:
    json.dump(result, json_file)
 

labelsWithId={}
for i in labels:
    for key in result:
        if key==i:
            labelsWithId[i]=result[key]["id"]
            break
        if i in result[key]["similarTags"]:
            labelsWithId[i]=result[key]["id"]
            break
    try:
        val=labelsWithId[i]
    except Exception as e:
        print("no id found for {}".format(i))
        
        
resultID={}
for res in result:
    resultID[result[res]["id"]]={"data":result[res]["data"],"similarTags":result[res]["similarTags"],"base":res}
    

  

  
