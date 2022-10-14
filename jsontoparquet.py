from pyarrow import json
import pyarrow.parquet as pq
import os

data_dir = os.getcwd() + "/data/ocsf/"

for filename in os.listdir(data_dir) :
    f = os.path.join(data_dir, filename)
    dest_dir = os.getcwd() + "/data/ocsf/" + str(filename).replace(".json", ".parquet")

    if os.path.isfile(f) :
        table = json.read_json(f) 
        pq.write_table(table, dest_dir)  
