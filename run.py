import requests
from bs4 import BeautifulSoup
import json
import os

headers = {
'Content-Type': 'text/xml; charset=UTF-8',
'SOAPAction': 'login',
}
data = open('documentation/login.xml')
response = requests.post('https://login.salesforce.com/services/Soap/u/45.0', headers=headers, data=data)
soup = BeautifulSoup(response.text, 'lxml')

maintag=soup.select_one('result')
for childtag in maintag.select('sessionId'):
    sessionId = childtag.text.strip()
    
for childtag in maintag.select('metadataServerUrl'):
    baseUrl = childtag.text.strip()
    baseUrl = baseUrl.split('/services')[0]

objNameList = ['Account', 'Opportunity']
extIdField = 'wmxid__c'

try:
    os.mkdir('soql')
    os.mkdir('sdl')
except:
    pass

for objectName in objNameList: 
    headers = {
    'Content-Type': 'text/xml; charset=UTF-8',
    'Authorization': 'Bearer ' + sessionId
    }
    response2 = requests.get(baseUrl + '/services/data/v20.0/sobjects/' + objectName + '/describe/', headers=headers)
    json_string = response2.text

    data = json.loads(json_string)
    fileName = objectName
    os.chdir('sdl')
    sdl = open(fileName+'.sdl', "w")
    os.chdir('..')
    os.chdir('soql')
    soql = open(fileName+'.soql', "w")
    os.chdir('..')
    soql.write('SELECT Id, ')
    soqlString = ''
    
    for entry in data["fields"]:
        if entry["updateable"]:
            if entry["custom"] and str(entry["relationshipName"]) != 'None':
                sdl.write(str(entry["relationshipName"]) + '=' + str(entry["relationshipName"]) +'\:' + extIdField + '\n')
                soqlString += (entry["relationshipName"]+'.' + extIdField + ',\n')
            elif entry["custom"]:
                soqlString += (entry["name"]+ ',\n')
                sdl.write(entry["name"] + '=' + entry["name"] + '\n')
    
    result = soqlString[0:-2]
    result += ' \nFROM ' + objectName       

    soql.write(result)
    sdl.close()
    soql.close()
    
