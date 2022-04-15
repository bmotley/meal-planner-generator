#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup

URL = "https://www.hellofresh.com/recipes/vegetarian-recipes?page=50"
#grabs list of vegetarian recipes from hellofresh, 
#unfortunately not a complete list of vegetarian recipes, but a large number nonetheless.
page = requests.get(URL)
#saves url as page
soup = BeautifulSoup(page.content, "html.parser")
#saves page as BeautifulSoup object, parsing for html


title_elements = [title.get_text() for title in soup.find_all('h3')]
#looks for the title text of all h3 classes
titles_end = title_elements.index('Recipes by Ingredient')
#creates an index for where the recipe titles end
titles = title_elements[:titles_end-0]
#creates list of cleaned recipe titles


text_elements2 = [link.get('href') for link in soup.find_all('a')]
#gets all the links from the web page under the 'a' class
target_ibdex1 = text_elements2.index('/recipes/ingredients')
#creates index for end of link list
target_ibdex2 = text_elements2.index('/recipes/casserole-recipes')
#creates index for beginning of link list
links = text_elements2[target_ibdex2+1:target_ibdex1-0]
#creates clean list of links that correspond to title list

#for i in range( len(links)):
#    links[i] = "https://www.hellofresh.com" + links[i]
#adds the full url so it's a clickable link



from pandas import pandas as pd
#importing pandas to create dataframes
recipe_df = pd.DataFrame(list(zip(titles, links)),
               columns =['Name', 'Link'])
#creates dataframe with the recipe title and link to recipe
recipe_df


random_recipes = recipe_df.sample(n=2)
#creates a sub-dataframe from the recipe dataframe above, selecting two recipes at random.
#change n number to increase or decrease random recipe amounts. 
#(will have to add to the below code to compensate for changes)


#First Recipe
recipe_URL = random_recipes.iloc[0]['Link']
#pulls string of first link
recipe_page = requests.get(recipe_URL)
#grabs the web page for first recipe
recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
#creates a soup object for easier html parsing

#Second Recipe
recipe_URL2 = random_recipes.iloc[1]['Link']
#pulls string of second link
recipe_page2 = requests.get(recipe_URL2)
#grabs the web page for second recipe
recipe_soup2 = BeautifulSoup(recipe_page2.content, "html.parser")
#creates a soup object for easier html parsing

whitelist = [
  'p'
]
#Creates a whitelist of only 'p' html classes, which is where the recipe elements are.
recipe_elements = [t for t in recipe_soup.find_all(text=True) if t.parent.name in whitelist]
#Finds all text objects from 'p' html classes
target_ibdex = recipe_elements.index('Salt')
#Final recipe item index

recipe_parts = recipe_elements[1:target_ibdex-0]
#gets all the ingredients from the recipe starting from the second object to the created index
recipe = [' '.join(recipe_parts[i:i+2]) for i in range(0, len(recipe_parts), 2)]
#creates a list to join amounts and ingredient labels for easy viewing


recipe_elements2 = [t for t in recipe_soup2.find_all(text=True) if t.parent.name in whitelist]
#Finds all text objects from 'p' html classes
target_ibdex3 = recipe_elements2.index('Salt')
#Final recipe item index
recipe_parts2 = recipe_elements2[1:target_ibdex3-0]
#gets all the ingredients from the recipe starting from the second object to the created index
recipe2 = [' '.join(recipe_parts2[i:i+2]) for i in range(0, len(recipe_parts2), 2)]
#creates a list to join amounts and ingredient labels for easy viewing


grocerylist_df = pd.DataFrame({"ingredient":recipe + recipe2})
#creates dataframe of both recipe ingredients


grocerylist_df_clean = grocerylist_df[grocerylist_df["ingredient"].str.contains("unit")==False]
#cleans dataframe of non-ingredients

print(random_recipes.iloc[0,0])
#prints first recipe title
print(random_recipes.iloc[1,0])
#prints second recipe title
print(grocerylist_df_clean)
#prints clean grocery list
print(random_recipes.iloc[0,1])
#prints first recipe link (clickable)
print(random_recipes.iloc[1,1])
#prints second recipe link (clickable)






