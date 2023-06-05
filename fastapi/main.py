from typing import Union

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import shutil
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

    subprocess.Popen('python3 ./estreamer/service.py ./estreamer.conf', shell=True, cwd="../")

@app.post("/api/executestop/")
def executestop():

    subprocess.Popen('bash encore.sh stop', shell=True, cwd="../")

@app.get("/api/lastwritten/")
def get_lastwritten():

    data = "N/A"
    try: 
      with open('../partner-fmc.csta.cisco.com-8302_bookmark.dat', 'r') as reader:
          data = reader.readlines()
          data = data[0]
          data = data[6:16]
          data = datetime.datetime.fromtimestamp( int(data) )        
    except IOError: 
      print("N/A")

    return data

@app.get("/api/status/")
def get_status():

    data = "Inactive"
    #this needs to change to the proper .dat filename, read value from config if possible
    with open("../partner-fmc.csta.cisco.com-8302_status.dat") as f :
        data = json.load(f)

    return data

@app.get("/api/awsresponse/")
def read_awsresponse():

    #must change to configured value
    fmcServer = "partner-fmc.csta.cisco.com"
    rateFile = "{0}-8302_response.dat".format(fmcServer)
    rateFile = "s3responses.dat"

    with open("../{0}".format(rateFile)) as f :
        data = json.load(f)

    return data

@app.get("/api/datarate/")
def read_datarate():

    fmcServer = "partner-fmc.csta.cisco.com"
    rateFile = "{0}-8302_rate.dat".format(fmcServer)

    with open("../{0}".format(rateFile)) as f :
        data = json.load(f)

    return data

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
