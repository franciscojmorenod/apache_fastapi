import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import subprocess
import mariadb
import json
import threading
import time


xlist_id             = []
xlist_ip             = []
xlist_engname        = []
xlist_active         = []
xlist_description    = []
xlist_macadr         = []

print("***************** mysql ********************")

mydb = mariadb.connect(
    host="localhost",
    user="fjmd",
    password="sicurumero",
    database="fmtestdb"
)

mycursor = mydb.cursor()

print("***************** mysql ******************** END")
app = FastAPI()

origins = [
      "http://localhost:5173"
]

app.add_middleware(
      CORSMiddleware,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)


#**********************************************************
#
#**********************************************************
def show_all_db_records():
    mycursor.execute("SELECT * FROM software_network_table")
    myresult = mycursor.fetchall()
    return myresult

#**********************************************************
#
#**********************************************************
def count_record(ip):
    sql =f"SELECT ip, COUNT(*) FROM software_network_table WHERE ip='{ip}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for row in myresult:
        count = row[1]
        # print(f"count={count}")
    return count

#**********************************************************
#
#**********************************************************
def insert_record(val):
    sql = "INSERT INTO software_network_table (ip, name, active, description, macadr) VALUES (%s, %s, %s ,%s ,%s)"
    mycursor.execute(sql, val)
    mydb.commit()
    #print(mycursor.rowcount, "Record Inserted.")

#**********************************************************
#
#**********************************************************
def runnmp_command(num):
    print(f"Entering nmap Thread {num}")
    get_ips_nmap_thread()
    while (num > 0):
        print(f"Thread is Sleeping.....")
        time.sleep(120)
        num = num -1
        print(f"Thread is Running the nmap Command to populate the nmp-data-buffer {num}")
        get_ips_nmap_thread()
    print(f"Exiting nmap Thread {num}")        
      
      

#**********************************************************
#
#**********************************************************
def get_ips_nmap_thread():
    global xlist_id            
    global xlist_ip            
    global xlist_engname       
    global xlist_active        
    global xlist_description   
    global xlist_macadr        
    
    print ("****************************************************")
    print("Thread that runs the nmap command and populates the nmap data-buffer")
    print("****************************************************")
    comm = [
        "sudo",
        "nmap",
        "-sP",
        "192.168.1.0/24",
        "-oG",
        "result_output"
    ]

    try:
        print("run the nmap command via a subprocess")
        result = subprocess.run(comm, capture_output=True, text=True, check=True)
        xlist_id.clear()
        xlist_ip.clear()
        xlist_engname.clear()
        xlist_active.clear()
        xlist_description.clear()
        xlist_macadr.clear()  
        #print(result.stdout)
        lines = result.stdout.splitlines()
        # print("--------------------------1001")
        #time.sleep(10)
        idx = 0
        myline = ""
        ready= False
        for line in lines:  
            if "Nmap scan report for" in line:
                idx = idx + 1

                if(ready == True):
                    val = (ip, engname, active, description, macadr)
                    xlist_id.append(idx)
                    xlist_ip.append(ip)
                    xlist_engname.append(engname)
                    xlist_active.append(active)
                    xlist_description.append(description)
                    xlist_macadr.append(macadr)
                    
                    
                    if count_record(ip) > 0:
                        print(f"\tAlready Exist -- {myline}")
                    else:
                        insert_record(val)
                        print(f"\tInserting New -- {myline}")

                    ready= False
                    macadr = ""
                    description  = ""
                    engname = ""

                str1 = line.replace("Nmap scan report for", "")
                ip = str1[1:]
                str1 = ip
                myline = "\t" + ip

            elif "Host is up" in line:
                active = "True"
                str2 = active
                myline = myline + "\t" + active

            elif "MAC Address: " in line:
                str3x = line.replace("MAC Address: ", "")
                macadr = str3x[:17]
                str3 = macadr
                description  = str3x[18:]
                engname = "morenof"
                myline = myline +  "\t" + str3x 
                ready = True

            else:
                print()
                print(line + "   ====== ???\n")

        print("\t***********************************************")  
        macadr      = "??:??:??:??:??:??"
        engname     = "defname"
        description = "defdescription"
        print(f"\tWARNING: Encountered a Not-fully-formed line for host= [{myline}]")
        # print(f"\t\tIP          = {ip}")
        # print(f"\t\tActive      = {active}")
        # print(f"\t\tMAC adr     = {macadr}")
        # print(f"\t\tEngName     = {engname}")
        # print(f"\t\tDescription = {description}")    
        # print("=========================")            
        # print("\t*******************************")                
        print(f"\tCONSIDER INSERTING RECORD [{myline} {macadr} {engname} {description}] ****")
        val = (ip, engname, active, description, macadr)
        xlist_id.append(idx)
        xlist_ip.append(ip)
        xlist_engname.append(engname)
        xlist_active.append(active)
        xlist_description.append(description)
        xlist_macadr.append(macadr)
        if count_record(ip) == 0:
            insert_record(val)
            print(f"\tINSERTED = [{myline} {macadr} {engname} {description}]")
        else:   
            print("\tNOT INSERTED: already exists in database")
        print("\t***********************************************")        
      
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stderr: {e.stderr}")

#**********************************************************
#
#**********************************************************   
@app.get("/getipsnmap")
def get_ips_nmap():
    global xlist_id            
    global xlist_ip            
    global xlist_engname       
    global xlist_active        
    global xlist_description   
    global xlist_macadr         
    print ("*********************************************************************")
    print("Client requested the nmap-data populated by the nmap thread")
    print("**********************************************************************")
 
      
    data = []
    total = len(xlist_ip)
    for i in range(total):
        # print(f"id = {i}")
        # print(f"ip = {xlist_ip[i]}")
        # print(f"macadr = {xlist_macadr[i]}")
        # print(f"active = {xlist_active[i]}")
        # print(f"engname = {xlist_engname[i]}")
        # print(f"description = {xlist_description[i]}")
        item = {
            "id":i+1,
            "ip":xlist_ip[i],
            "macadr": xlist_macadr[i],
            "active": xlist_active[i],                                    
            "engname":xlist_engname[i],
            "description": xlist_description[i]            
                }
        data.append(item)  
    # data = [
    #         {
    #               "ip":"192.128.1.101",
    #               "macadr":"AA:BB:CC:DD:EE:01",
    #               "active": "True",                                    
    #               "engname": "morenof",
    #               "description": "Default Description1"
    #         },
    #         {
    #               "ip":"192.128.1.102",
    #               "macadr":"AA:BB:CC:DD:EE:02",
    #               "active": "True",                                    
    #               "engname": "morenof",
    #               "description": "Default Description2"                  
    #          },
    #         {
    #               "ip":"192.128.1.103",
    #               "macadr":"AA:BB:CC:DD:EE:03",
    #               "active": "True",                                    
    #               "engname": "morenof",
    #               "description": "Default Description3"
    #          },
    #         {
    #               "ip":"192.128.1.104",
    #               "macadr":"AA:BB:CC:DD:EE:04",
    #               "active": "True",                                    
    #               "engname": "morenof",
    #               "description": "Default Description4"
    #         },
    #   ]      
    return data


#**********************************************************
#
#**********************************************************
@app.get("/getipsdb")
def get_ips_db():
    print("Get IP addresses from Database")
    list_id             = []
    list_ip             = []
    list_engname        = []
    list_active         = []
    list_description    = []
    list_macadr         = []    
    myresult =  show_all_db_records()
    for row in myresult:
        print(row)
        list_id.append(row[0])        
        list_ip.append(row[1])
        list_engname.append(row[2])
        list_active.append(row[3])
        list_description.append(row[4])
        list_macadr.append(row[5])        

    data = []       
    total = len(list_ip)
    for i in range(total):
        item = {
            "id":list_id[i],
            "ip":list_ip[i],
            "macadr": list_macadr[i],
            "active": list_active[i],                                    
            "engname":list_engname[i],
            "description": list_description[i]            
                }
        data.append(item)              
    return data

#**********************************************************
#
#**********************************************************
@app.post("/insertdb")
def insert_db():
    print("Insert IP address in Database")
    return {"result":"SUCCESS"}


#**********************************************************
#
#**********************************************************
if __name__ == "__main__":
    print("******************************************************")
    print("The tool scans the 192.168.1.0/24 net with nmap")
    print("******************************************************")    
    t1 =threading.Thread(target=runnmp_command, args=(1000,))
    t1.daemon = True
    t1.start()
    # t1.join()   
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("******************************************************")
    print("PROGRAM TERMINATES")
    print("******************************************************")    
    t1.close()