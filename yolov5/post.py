import glob
import base64
from datetime import date
import requests
import os
def find(root_dir, ip):
    headers = {'Content-type': 'application/jsonData',
            'Accept': 'text/plain',
            'Content-Encoding': 'utf-8'}

    for filename1 in glob.iglob(root_dir + '**/*.jpg', recursive=True):
        print(filename1)
        filename_l = filename1.split("/")
        filename_l = filename_l[2] + "_" + filename_l[3]
        
        if filename_l[-5:] == "r.jpg":
            for filename2 in glob.iglob(root_dir + '**/*.jpg', recursive=True):
                filename_r = filename2.split("/")
                filename_r = filename_r[2] + "_" + filename_r[3]
                if filename_r[-5:] == "l.jpg" and filename_r[:-5] == filename_l[:-5]:
                    f1, f2 = encode(filename1, filename2)
                    
                    for gps in glob.iglob(root_dir + '**/*.json', recursive=True):
                        if gps[-8:] == "gps.json" and gps[:-8] == filename_l[:-5]:
                            file = open(gps)
                            data = json.load(file)
                            gps = data["gps"]
                            post(ip, f1, f2, gps)
                            os.remove(filename1)
                            os.remove(filename2)
                            os.remove(gps)




def encode(filename1, filename2):         
    with open(filename1, "rb") as image_file:
        encoded_il = str(base64.b64encode(image_file.read())).encode()

    with open(filename2, "rb") as image_file:
        encoded_ir = str(base64.b64encode(image_file.read())).encode()
    return encoded_il, encoded_ir

def post(ip, encoded_il, encoded_ir, gps):  
    json = {
            "lat": str(gps[0]),
            "lng": str(gps[1]),
            "image_l": encoded_il,
            "image_r": encoded_ir
            }


    while requests.post(ip, json=json).status_code() != 200:
        print("Error with post")     
    print("Sucsessfully posted")
