import unittest
import pandas as pd
from Yelp import collect_state_input, collect_zip_input
from Yelp import collect_liked_input, makeScatterchart
from Yelp import makeBarchart, create_search_url
from Yelp import api_to_json, add_all_info_df


class TestFileName(unittest.TestCase):
#  State length is greater than abbreviation
   def test_collect_state_input(self):
      length= len(collect_state_input())
      if(length>=2):
         isvalid = True
      else:
         isvalid = False
      self.assertTrue(isvalid)
      print()

# All zipcodes must be greater than 5
   def test_collect_zip_input(self):
      length= len(collect_zip_input())
      if(length==5):
         isvalid = True
      else:
         isvalid = False
      self.assertTrue(isvalid)
      print()

# Input must be a valid length longer than 3 characters.
   def test_collect_liked_input(self):
      length= len(collect_liked_input())
      if(length>3):
         isvalid = True
      else:
         isvalid = False
      self.assertTrue(isvalid)
      print()
      
# Check no errors are happening when you put a valid data frame
   def test_makeScatterchart(self):
      test_data = [['restaurant_1', 1], ['restaurant_2', 2], ['restaurant_3', 4]]
      xcol ="Name"
      ycol = "Rating"
      df = pd.DataFrame(test_data, columns= ['Name', 'Rating'])
      isworking = True
      try:
         makeScatterchart(df, xcol,ycol)
      except:
         isworking= False
      self.assertTrue(isworking)
      print()
 
#  Test that there are no errors when trying to make a chart, using a 
#  Valid dataframe.
   def test_makeBarchart(self):
      test_data = [['restaurant_1', 1], ['restaurant_2', 2], ['restaurant_3', 4]]
      xcol = "Name"
      ycol = "Rating"
      df = pd.DataFrame(test_data, columns= ['Name', 'Rating'])
      isworking = True
      try:
         makeBarchart(df, xcol,ycol)
      except:
         isworking= False
         
      self.assertTrue(isworking)
      print()
      
# Check that a string is created    
   def test_create_search_url(self):
      base_url = 'testurl.com'
      zip_code = 'test'
      state = 'test'
      term1 = 'test'
      url= create_search_url(base_url, zip_code,state, term1)
      self.assertEqual(type(url), str)
      print()

      
# Check that returned dictionary is not empty and that there is no error
   def test_api_to_json(self):
      search_url='https://api.yelp.com/v3/businesses/search?location=illinois&term=italian'
      api_key ='eUJ17k9QVRaQVpchITGQszLJGOhhyE52aMFr1o1AO4v52d3_-La_yyI1gj-FiGOEKFG62RrVMqh5rN7Ab12hw60MC6euNHD7mYV5sARgZS4GNYFc-g_FQH4c7c7jYHYx'
      headers = {
       'Authorization': 'Bearer %s' % api_key,
      }
      test1= {}
      try:
         dictionary= api_to_json(search_url,headers)
      except:
         dictionary= 'error'
      self.assertNotEqual(dictionary, test1)
      self.assertNotEqual(dictionary, 'error')
      print()
      
      

if __name__ == '__main__':
    unittest.main()