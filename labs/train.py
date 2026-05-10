
import requests 
import csv  
from xml.dom.minidom import parseString 
url = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML" 
page = requests.get(url) 
doc = parseString(page.content) 
# check it works 
#print (doc.toprettyxml()) #output to console comment this out once you know it works 
# if I want to store the xml in a file. You can comment this out later 
with open("trainxml.xml","w") as xmlfp: 
    doc.writexml(xmlfp) 

retrieveTags=['TrainStatus', 
'TrainLatitude', 
'TrainLongitude', 
'TrainCode', 
'TrainDate', 
'PublicMessage', 
'Direction' 
] 

objTrainPositionsNodes = doc.getElementsByTagName("objTrainPositions") 

# https://stackoverflow.com/questions/18952716/valueerror-i-o-operation-on-closed-file
#adding the newline= '' parameter 
with  open('week03_train.csv', mode='w', newline='') as train_file: 
    train_writer = csv.writer(train_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
    for objTrainPositionsNode in objTrainPositionsNodes: 
        traincodenode = objTrainPositionsNode.getElementsByTagName("TrainCode").item(0) 
        traincode = traincodenode.firstChild.nodeValue.strip()
    
    dataList = [] 
    for retrieveTag in retrieveTags: 
        datanode = objTrainPositionsNode.getElementsByTagName(retrieveTag).item(0) 
        dataList.append(datanode.firstChild.nodeValue.strip()) 
        train_writer.writerow(dataList) 
        print (dataList)