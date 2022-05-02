from hashlib import sha256
import os
from pprint import pprint
import json
import sqlite3


class webTools:
      def Encrypt(password):
            shaClass = sha256()
            shaClass.update(password)
            hash = shaClass.hexdigest()
            return hash



      
      def scanDX(directory,language,jsonLocation): #directory is language folders
            
            def writeJSON(Array):
                  jsonString = json.dumps(Array) #converts dictArray to JSON string
                  jsonFile = open(jsonLocation, "w")
                  jsonFile.write(jsonString)
                  jsonFile.close()
                  print("JSON file created successfully")


            def scan(dir_):
                  dir = os.listdir(dir_) #list contents of project
                  cont_list = [] 
                  for file in dir: #iterate through files and folders inside project
                        FilePath = dir_ + file + '/' #create path to selected file/folder
                        if os.path.isdir(FilePath): #checks if it is a file or folder
                              cont = scan(FilePath)
                              dict = {'id':dir.index(file),"Name":file + ' >', "Type":'directory', "Lang":language ,"Path": FilePath, "Contents":cont}
                              cont_list.append(dict)

                        else: 
                              dict = {'id':dir.index(file), "Name":file, "Lang": language ,"Type": "File", "Path":FilePath} #if type=file create dictionary containing file details
                              cont_list.append(dict) #append dict to contents list

                  return(cont_list)

            conts = scan(directory)
            writeJSON(conts)
            #print(language, '=')
            #pprint(conts)
            return conts
                         

wt = webTools()
print("")



            