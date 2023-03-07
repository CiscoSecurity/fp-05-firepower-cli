from typing import Union

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import shutil
import json
import subprocess
import datetime

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str

class Config(BaseModel):
    server: str
    connection: int

DB: List[Person] = [
   Person(id=1, name="TestS"),
   Person(id=2, name="TestH")
]


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
    with open("../partner-fmc.csta.cisco.com-8302_status.dat") as f :
        data = json.load(f)

    return data

@app.get("/api/loadconfig/")
def read_config():

    with open("../estreamer.conf") as f :
        data = json.load(f)

    return data

@app.post("/api/uploadfile/")
async def create_upload_file(file: UploadFile): 

    filename = '../client.pkcs12'

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}
