import requests
import pandas as pd
import sqlalchemy
import os
from sqlalchemy import create_engine
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


#  Collect input from user and return it.
def collect_state_input():
    state = input("Enter a state: ")
    while(not state.isalpha()):
        state = input("Enter a state: ")
    return state


#  Collect zip_code input from user and return it.
def collect_zip_input():
    while True:
        try:
            zip_code = int(input("Enter a ZipCode: "))
            break
        except:
            continue
    zip_code = str(zip_code)
    return zip_code


#  Return collected user preference iput.
def collect_liked_input():
    food_type_liked = input(
       "Enter the type of food liked (ex; Italian, Mexican,etc): ")
    while(not food_type_liked.isalpha()):
        food_type_liked = input(
            "Enter the type of food liked (ex; Italian, Mexican,etc ): ")
    return food_type_liked


# SQL, save database, save to file, load file, load database.
def saveSQLtoFile(database_name, file_name):
    os.system('mysqldump -u root -pcodio ' + database_name + ' > ' + file_name)


# Load a SQL database from a file.
def loadSQLfromFile(database_name, file_name):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + database_name + ';"')
    os.system("mysql -u root -pcodio " + database_name + " < " + file_name)


#   Save the dataset.
def saveDatasetToFile(database_name, file_name, dataframe, table_name):
    engine = create_engine('mysql://root:codio@localhost/' +
                           database_name + '?charset=utf8', encoding='utf-8')
    dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)
    saveSQLtoFile(database_name, file_name)


#  Load dataset from file.
def loadDataset(database_name, table_name, file_name):
    loadSQLfromFile(database_name, file_name)
    engine = create_engine('mysql://root:codio@localhost/' +
                           database_name + '?charset=utf8', encoding='utf-8')
    df = pd.read_sql_table(table_name, con=engine,
                           if_exists='replace', index=False)
    return df


#  Make a scatter plot from dataframe and save it as html file.
def makeScatterchart(df, xcol, ycol):
    data = df
    fig = px.scatter(data, x=xcol, y=ycol, color="Name",
                     size="Rating")
    fig.write_html('scatter.html')


# Make a scatter plot from dataframe and save it as a html file.
def makeBarchart(df, xcol, ycol):
    data = df
    fig = px.bar(data, x=xcol, y=ycol, color="Rating",
                 title="Restaurant Search Results")
    fig.write_html('barchart.html')


#  Create and return the search url.
def create_search_url(base_url, zip_code, state, term1, term2='None'):
    location = str(state + zip_code)
    search_url = base_url + 'location=' + location + '&' + 'term=' + term1
    return search_url


#  Git information from API and return as json.
def api_to_json(search_url, headers):
    r = requests.get(search_url, headers=headers)
    print(r.status_code)
    response_json = r.json()
    return response_json


# Parse information and return as a dataframe.
def add_all_info_df(col_names, main_dictionary):
    df = pd.DataFrame(columns=col_names)
    for business in main_dictionary:
        df.loc[len(df.index)] = [business['name'], business['rating'],
                                 business['location']['address1'],
                                 business['location']['zip_code'],
                                 business['categories'][0]['alias']]
    df.sort_values(by=['Rating'], inplace=True, ascending=False)
    return df


#  Main code-
#  Collect user input
base_url = 'https://api.yelp.com/v3/businesses/search?'
zip_code = collect_zip_input()
state = collect_state_input()
preference = collect_liked_input()

# Get API information and access.
search_url = create_search_url(base_url, zip_code, state, preference)
api_key = 'eUJ17k9QVRaQVpchITGQszLJGOhhyE52aMFr1o1AO4v52d3_-La_yyI1gj-FiGOEKFG62RrVMqh5rN7Ab12hw60MC6euNHD7mYV5sARgZS4GNYFc-g_FQH4c7c7jYHYx'
headers = {
    'Authorization': 'Bearer %s' % api_key,
}

restaurantList = api_to_json(search_url, headers)
main = restaurantList['businesses']

#  Turn API info into dataframe.
col_names = ['Name', 'Rating', 'Location', 'ZipCode', 'Food Type']
df = add_all_info_df(col_names, main)
df2 = df.iloc[:3]
print(df2)

#  make database
database_name = 'restaurants'
file_name = 'test_file.sql'
table_name = 'restaurant_information'

os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' +
          database_name + ';"')
engine = create_engine('mysql://root:codio@localhost/restaurants' +
                       '?charset=utf8', encoding='utf-8')
df2.to_sql('restaurant_information', con=engine,
           if_exists='replace', index=False)
makeBarchart(df2, "Name", "Rating")

# saveSQLtoFile(database_name, file_name)
# loadSQLfromFile(database_name, file_name)
# makeScatterchart(df2, "Name", "Rating")
