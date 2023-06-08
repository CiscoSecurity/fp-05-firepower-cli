from typing import Union

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import shutil
import utils
import json
import subprocess
import datetime

app = FastAPI()

class eStreamerConfig(BaseModel):
    aws_region: str
    aws_source: str
    aws_account: str
    aws_s3: str
    aws_buffer_rate: str

    class Config:
        orm_mode = True

@app.get("/api/")
def read_root():
    return DB

@app.post("/api/execute/")
def execute():
    output = subprocess.run('bash ./encore.sh start', capture_output=True, text=True, cwd="../", shell=True)
    return output
#    subprocess.Popen('python3 ./estreamer/service.py ./estreamer.conf', shell=True, cwd="../")

@app.post("/api/test/")
def test():

    output = subprocess.run('python3 ./estreamer/diagnostics.py ./estreamer.conf', capture_output=True, text=True, cwd="../", shell=True)
    return output

@app.post("/api/executestop/")
def executestop():

    output = subprocess.run('bash ./encore.sh stop', capture_output=True, text=True, cwd="../", shell=True)
    return output
#    subprocess.Popen('bash ../encore.sh stop', shell=True, cwd="../")

@app.get("/api/lastwritten/")
def get_lastwritten():

    with open("../estreamer.conf") as f :
      data = json.loads(f.read())

    hostname = data["subscription"]["servers"][0]["host"]
    bookmark = '../{0}-8302_bookmark.dat'.format(hostname)

    try: 
      with open(bookmark, 'r') as reader:
          data = reader.readlines()
          data = data[0]
          data = data[6:16]
          data = datetime.datetime.fromtimestamp( int(data) )        
    except IOError: 
      print("N/A")

    return data

@app.get("/api/status/")
def get_status():

    with open("../estreamer.conf") as f :
      data = json.loads(f.read())

    hostname = data["subscription"]["servers"][0]["host"]
    status = '../{0}-8302_status.dat'.format(hostname)

    with open(status) as f :
        data = json.load(f)

    return data

@app.get("/api/awsresponse/")
def read_awsresponse():

    #todo: change to configured value
    rateFile = "../s3responses.dat"

    data = [json.loads(line)
        for line in open(rateFile, 'r', encoding='utf-8')]

    events = [];

    for index, k in enumerate(data):

       for v in k.values() :

           events.append(v)

    return events

@app.get("/api/datarate/")
def read_datarate():

    rateFile = "../rates.dat"

    data = [json.loads(line)
        for line in open(rateFile, 'r', encoding='utf-8')]

    rates = [];

    for index, k in enumerate(data):
       event_rate = {}
       for key in k.keys() :
           event_rate['monitor'] = key

       for v in k.values() :
           event_rate.update(v)

       event_rate['diff'] = 0

       if index != 0 :
           delta = event_rate['count'] - rates[index-1]['count']
           if delta > 0 : event_rate['diff'] = delta 

       rates.append(event_rate)


    return rates

@app.get("/api/loadconfig/")
def read_config():

    with open("../estreamer.conf") as f :
        data = json.load(f)

    return data

#The current method modifies only the first configuration item in the list
@app.post("/api/modifyconfig/")
async def modify_config(config: eStreamerConfig): 

    filename = '../client.pkcs12'

    with open("../estreamer.conf") as f :
      data = json.loads(f.read())

    if(config.aws_region ):
       adapters = data["handler"]["outputters"]
       for obj in adapters :
           print(obj["stream"]["options"]["region"])

    data["handler"]["outputters"][0]["stream"]["options"]["region"] = config.aws_region
    data["handler"]["outputters"][0]["stream"]["options"]["accountId"] = config.aws_account
    data["handler"]["outputters"][0]["stream"]["options"]["s3"] = config.aws_s3
    data["handler"]["outputters"][0]["stream"]["options"]["awsBufferRate"] = config.aws_buffer_rate
    data["handler"]["outputters"][0]["stream"]["options"]["awssource"] = config.aws_source 

    with open("../estreamer.conf", 'w') as f:
       f.write(json.dumps(data,indent=4, separators=(',', ': ')))

    return {"Updated Configuration"}

@app.post("/api/uploadfile/")
async def create_upload_file(file: UploadFile): 

    filename = '../client.pkcs12'

    if file is not None:
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}
