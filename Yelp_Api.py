import requests
import pandas as pd
import sqlalchemy
import os
#  import json
from sqlalchemy import create_engine
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


#  collect input
def collect_state_input():
   state = input("Enter a state: ")
   while(not state.isalpha()):
      state = input("Enter a state: ")
   return state

def collect_zip_input():
   while True:
      try:
         zip_code= int(input("Enter a ZipCode: "))
         break
      except:
            continue
   zip_code= str(zip_code)      
   return zip_code

def collect_liked_input():
   food_type_liked = input("Enter the type of food liked (ex; Italian, Mexican,etc ): ")
   while(not food_type_liked.isalpha()):
      food_type_liked = input("Enter the type of food liked (ex; Italian, Mexican,etc ): ")
   return food_type_liked


   
# SQL, save database, save to file, load file, load database    
def saveSQLtoFile(database_name, file_name):
   os.system('mysqldump -u root -pcodio '+database_name+' > '+ file_name)

   
def loadSQLfromFile(database_name, file_name):
   os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+database_name+';"')
   os.system("mysql -u root -pcodio "+database_name+" < " + file_name)
   
def saveDatasetToFile(database_name, file_name, dataframe, table_name):
   engine= create_engine('mysql://root:codio@localhost/'+database_name+'?charset=utf8', encoding='utf-8')
   dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)
   saveSQLtoFile(database_name,file_name)

def loadDataset(database_name, table_name, file_name):
   loadSQLfromFile(database_name,file_name)
   df= pd.read_sql_table(table_name, con=createEngine(database_name))
   return df

def makeBarchart(df, xcol, ycol):
   df.plot.barh(x = xcol, y = ycol )
   plt.show()
   
   
   
   
api_key ='eUJ17k9QVRaQVpchITGQszLJGOhhyE52aMFr1o1AO4v52d3_-La_yyI1gj-FiGOEKFG62RrVMqh5rN7Ab12hw60MC6euNHD7mYV5sARgZS4GNYFc-g_FQH4c7c7jYHYx'
headers = {
    'Authorization': 'Bearer %s' % api_key,
}

base_url='https://api.yelp.com/v3/businesses/search?'
zip_code= collect_zip_input()
state= collect_state_input()
preference= collect_liked_input()
# print("ZipCode: "+ zip_code + " state: " + state + " term 1: " + preference)

search_url=base_url+ 'location=' + zip_code + '&' + 'term=' + preference

response= requests.get(search_url, headers=headers)
print(response.status_code)
restaurantList =response.json()
#  print(restaurantList)

main = restaurantList['businesses'] #inside businesses dictionary)

   
   
# main_info= main[0]
# print(main_info)

col_names = ['Name','Rating', 'Location', 'ZipCode', 'Food Type']
df = pd.DataFrame(columns = col_names)

for business in main:  
    df.loc[len(df.index)] = [business['name'], business['rating'], business['location']['address1'], business['location']['zip_code'],                   
                         business['categories'][0]['alias']]
    
df.sort_values(by=['Rating'], inplace=True, ascending=False)    
print(df)

database_name= 'restaurants'   
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+database_name+';"')
engine = create_engine('mysql://root:codio@localhost/restaurants')
df.to_sql('restaurant_information', con = engine, if_exists='replace', index=False)

makeBarchart(df, 'name', 'rating')