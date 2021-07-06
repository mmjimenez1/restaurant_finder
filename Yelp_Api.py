import requests
import pandas as pd
import sqlalchemy
import os
from sqlalchemy import create_engine


api_key='eUJ17k9QVRaQVpchITGQszLJGOhhyE52aMFr1o1AO4v52d3_-La_yyI1gj-FiGOEKFG62RrVMqh5rN7Ab12hw60MC6euNHD7mYV5sARgZS4GNYFc-g_FQH4c7c7jYHYx'
headers = {
    'Authorization': 'Bearer %s' % api_key,
}

base_url='https://api.yelp.com/v3/businesses/search?'
location= 'NYC'
term= 'Italian'
search_url=base_url+ 'location=' + location + '&' + 'term=' + term

response= requests.get(search_url, headers=headers)
print(response.status_code)
restaurantList =response.json()
#  print(restaurantList)

main = restaurantList['businesses'] #inside businesses dictionary


   
   
# main_info= main[0]
# print(main_info)

col_names = ['name','rating', 'location', 'ZipCode', 'Food Type']
df = pd.DataFrame(columns = col_names)

for business in main:
    df.loc[len(df.index)] = [business['name'], business['rating'], business['location']['address1'], business['location']['zip_code'],                   
                         business['categories'][0]['alias']]
    df.sort_values(by=['name'], ascending=False)
print(df)

database_name= 'restaurants'   
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+database_name+';"')
engine = create_engine('mysql://root:codio@localhost/restaurants')
df.to_sql('restaurant_information', con = engine, if_exists='replace', index=False)

# new stuff