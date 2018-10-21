
# coding: utf-8

# In[1]:

# This project involves using Beautiful Soup to extract information relating to Oscar winners from Wikipedia pages. In total 
# six different pages will be accessed in order to obtain the following:
# 1. Best Picture 
# 2. Best Director
# 3. Best Actor
# 4. Best Actress
# 5. Best Supporting Actor
# 6. Best Supporting Actress
# Once the data has been retrieved from each page, it will be stored in dataframes. I will then connect to MySQL, create tables
# and insert the data there. Finally I will run queries on the database to provide useful insight.


# In[2]:

import urllib2;                    # for retrieving the contents of a page
from bs4 import BeautifulSoup;     # for parsing the contents of a page to HTML
import pandas as pd                # for creating dataframes
import re                          # for regular expressions


# In[3]:

# function that takes in a URL and returns the contents of the page
def loadPage(url):
    page = urllib2.urlopen(url)
    data = BeautifulSoup(page, "lxml")
    return data

# style of table cells that have Oscar winners in them
winnerStyle = 'background:#FAEB86'


# In[4]:

# Page 1- Best Picture
# Call function to read in URL and retrieve data from the page
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
# from the data get all the tables that have the following class
tables = data.findAll("table", class_= "wikitable")


# In[5]:

# There are tables for each decade starting from the 1920's. We want to go through each table and extract the appropriate information
# Create empty lists for each film and nominee
films = []
nominees = []

# There are ten tables so we use range to keep track 
for i in range(0, 11):
    # For each table get each row start with the following style ie. could be 'background:#FAEB86' or 'background:#FAEB86;'
    for row in tables[i].findAll("tr", style=re.compile('^'+winnerStyle)):
        # Get each cell within that row
        cells = row.findAll('td')
        # Get the text from within the first cell, encode it to utf-8 and add it to the films list
        if(len(cells) > 0):        
            film = cells[0].find(text=True).encode('utf-8').strip()
            films.append(film)
            # Get the text from within the second cell, encode it and add it to the list of nominees
        if(len(cells) > 1):      
            nominee = cells[1].findAll(text=True)[:-1]
            nominees.append("".join(nominee).encode('utf-8').strip() )    


# In[6]:

# Here we extract the years. Years can be different formats depending on how far back they are ie. 1927/28, 1927/1928, 1928
# Create an empty list for each year
years = []
for i in range(0, 11):  
    # For each table row get each cell with the following style
    for row in tables[i].findAll("td", style="text-align:center"):
            # Get each link within that row
            cells = row.findAll('a')
            # If year is all in one link and in a format like 1927/28 then we want the first two and last two charaters so 
            # that it will be 1928
            if(len(cells[0].find(text=True)) == 7):
                year = cells[0].find(text=True)[0:2] + cells[0].find(text=True)[5:7]
            # If year is in two links and the second link has four numbers ie. 1927/1928 then we want the second link
            elif(len(cells[1].find(text=True)) == 4):       
                if (cells[1].find(text=True).isnumeric()):
                    year = cells[1].find(text=True)
            # If the year is in two links and the second link has two numbers ie. 1927/28 then we want the first two characters
            # of the first link and the last two of the second link
            elif(len(cells[1].find(text=True)) == 2):
                if (cells[1].find(text=True).isnumeric()):
                    year = cells[0].find(text=True)[0:2] + cells[1].find(text=True)
            # Else the year is in a standard format ie. 1928 so get four characters
            else:
                year = cells[0].find(text=True)[0:4]
            # add year to list of years
            years.append(year)


# In[7]:

# Check the length of each list. They are all the same
print(len(films))
print(len(nominees))
print(len(years))


# In[8]:

# Create a data frame for storing each list
df_picture = pd.DataFrame()
df_picture["Year"] = pd.to_numeric(years, errors='coerce')
df_picture["Film"] = films
df_picture["Nominee"] = nominees
df_picture


# In[9]:

# Page2 - Best Director
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director")
tables = data.findAll("table", class_= "wikitable sortable")


# In[10]:

# Here we extract each film and its director. All the data is stored in one table.
# Create empty lists for storing each film and director
films =[]
directors = []
# Get each row within the table
for row in tables[0].findAll("tr"):
        cells = row.findAll("td", style=re.compile('^'+winnerStyle))
        # For the first year there was two categories of winners so we want to include that information. It is inside a span tag.
        # FindAll() gets all the text within the cell including child tags. 
        #Finally use join() to merge the text into one string and add it to the list of direcors
        if(len(cells) > 0):
            director = cells[0].findAll(text=True)[:-1]
            directors.append("".join(director).encode('utf-8').strip())  
        # Get the film from the second cell and add it to the list of films
        if(len(cells) > 1):
            film = cells[1].find(text=True).encode('utf-8').strip() 
            films.append(film)


# In[11]:

# Here we extract the years.
years = []
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')     
    if(len(cells[0].find(text=True)) == 7):
        year = cells[0].find(text=True)[0:2] + cells[0].find(text=True)[5:7]
    elif(len(cells[1].find(text=True)) == 4):       
        if (cells[1].find(text=True).isnumeric()):
            year = cells[1].find(text=True)  
    elif(len(cells[1].find(text=True)) == 2):
        if (cells[1].find(text=True).isnumeric()):
            year = cells[0].find(text=True)[0:2] + cells[1].find(text=True)
    else:
        year = cells[0].find(text=True)[0:4]
    years.append(year)


# In[12]:

# Check the length of each list. Due to the 1st Oscars having multiple awards they are not the same length
print(len(films))
print(len(directors))
print(len(years))


# In[13]:

# To amend this lets insert a year at the position 1 with the same value as the position 0
years.insert(1, years[0])


# In[14]:

# Now they are all the same length
print(len(films))
print(len(directors))
print(len(years))


# In[15]:

# Create a data frame for storing each list and print it
df_directors = pd.DataFrame()
df_directors["Year"] = pd.to_numeric(years, errors='coerce')
df_directors["Director"] = directors
df_directors["Film"] = films
# Look at the data frame.
df_directors


# In[16]:

# Page 3- Best Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[17]:

# Here we extract each actor and film
films =[]
actors = []
for row in tables[0].findAll("tr"):
    cells = row.findAll("td", style=re.compile('^'+winnerStyle))    
    # Index variable to keep track of the cell we are in
    index = 0
    for c in cells:
        # Get all the links within each cell
        links = c.findAll("a")
        for l in links:
            # If link has the attribute 'title' then we want it
            if(l.has_attr('title')):
                # If it is the first cell then get the text and add it to the list of actors
                if(index == 0): 
                    actor = l.find(text=True).encode('utf-8').strip()
                    actors.append(actor)
                # If it is the third cell then get the text and add it to the list of films
                elif(index == 2): 
                    film = l.find(text=True).encode('utf-8').strip()
                    films.append(film)
        # increment index
        index = index+1         
        


# In[18]:

# Here we extract the years
years = []
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')     
    if(len(cells[0].find(text=True)) == 7):
        year = cells[0].find(text=True)[0:2] + cells[0].find(text=True)[5:7]
    elif(len(cells[1].find(text=True)) == 4):       
        if (cells[1].find(text=True).isnumeric()):
            year = cells[1].find(text=True)  
    elif(len(cells[1].find(text=True)) == 2):
        if (cells[1].find(text=True).isnumeric()):
            year = cells[0].find(text=True)[0:2] + cells[1].find(text=True)
    else:
        year = cells[0].find(text=True)[0:4]
    years.append(year)


# In[19]:

# Check the length of each list. They are not the same. There are two reasons for this.
# 1. In the 1st Oscars the actor won awards for two films
# 2. In 1932 there was a tie for 1st place
print(len(films))
print(len(actors))
print(len(years))


# In[20]:

# To amend this lets insert the actor at position 0 into position 1 and insert the appropriate years at position 1 and 6 of years
actors.insert(1, actors[0])
years.insert(1, years[0])
years.insert(6, years[5])


# In[21]:

# Now they are all the same length
print(len(films))
print(len(actors))
print(len(years))


# In[22]:

# Create a data frame for storing the lists
df_actors = pd.DataFrame()
df_actors["Year"] = pd.to_numeric(years, errors='coerce')
df_actors["Actor"] = actors
df_actors["Film"] = films
# Print the data frame and look at years 1928 and 1932
df_actors


# In[23]:

# Page 4- Best Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[24]:

# Here we extract each actress and film
films =[]
actresses = []
for row in tables[0].findAll("tr"):
    cells = row.findAll("td", style=re.compile('^'+winnerStyle))   
    index = 0
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actress = l.find(text=True).encode('utf-8').strip()
                    actresses.append(actress)
                elif(index == 2): 
                    movie = l.find(text=True).encode('utf-8').strip()
                    films.append(movie)
        index = index+1         


# In[25]:

# Here we extract each year
years = []
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')     
    if(len(cells[0].find(text=True)) == 7):
        year = cells[0].find(text=True)[0:2] + cells[0].find(text=True)[5:7]
    elif(len(cells[1].find(text=True)) == 4):       
        if (cells[1].find(text=True).isnumeric()):
            year = cells[1].find(text=True)  
    elif(len(cells[1].find(text=True)) == 2):
        if (cells[1].find(text=True).isnumeric()):
            year = cells[0].find(text=True)[0:2] + cells[1].find(text=True)
    else:
        year = cells[0].find(text=True)[0:4] 
    years.append(year)


# In[26]:

# Check the length of each list. They are not the same. There are two reasons for this.
# 1. In the 1st Oscars the actress won awards for three films
# 2. In 1968 there was a tie for 1st place
print(len(actresses))
print(len(films))
print(len(years))


# In[27]:

# Lets amend this by inserting the actress at the position 0 to position 1 and 2. Do the same for the years
# Also insert the year at position 40 into position 41
actresses.insert(1, actresses[0])
actresses.insert(2, actresses[1])
years.insert(41, years[40])
years.insert(1, years[0])
years.insert(2, years[1])


# In[28]:

# Now they are all the same length
print(len(actresses))
print(len(films))
print(len(years))


# In[29]:

# Create a data frame for storing the lists
df_actresses = pd.DataFrame()
df_actresses["Year"] = pd.to_numeric(years, errors='coerce')
df_actresses["Actress"] = actresses
df_actresses["Film"] = films
# Print the dataframe and look at the first three indexes which have the same year and actress but different films
df_actresses


# In[30]:

# Now check the year 1968 and see two actresses and films
df_actresses.loc[df_actresses['Year'] == 1968]


# In[31]:

# Page 5 - Best Supporting Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[32]:

# Here we extract each actor and film
films =[]
actors = []
for row in tables[0].findAll("tr"):
    cells = row.findAll("td", style=re.compile('^'+winnerStyle))   
    index = 0
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actor = l.find(text=True).encode('utf-8').strip()
                    actors.append(actor)
                elif(index == 2): 
                    movie = l.find(text=True).encode('utf-8').strip()
                    films.append(movie)
        index = index+1  


# In[33]:

# Here we extract the years. Because these awards started in 1936 all the years are in the correct format
years = []
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a') 
    if(len(cells) > 1):        
        year = cells[0].find(text=True)[0:4] 
        years.append(year)


# In[34]:

# Check all lists are the same length, they are
print(len(actors))
print(len(films))
print(len(years))


# In[35]:

# Create a data frame for storing the lists
df_supActors = pd.DataFrame()
df_supActors["Year"] = pd.to_numeric(years, errors='coerce')
df_supActors["Actor"] = actors
df_supActors["Film"] = films
# Print data frame
df_supActors


# In[36]:

# Page 6 - Best Supporting Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[37]:

# Here we extract each actress and film
films =[]
actresses = []
for row in tables[0].findAll("tr"):
    cells = row.findAll("td", style=re.compile('^'+winnerStyle))   
    index = 0
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actress = l.find(text=True).encode('utf-8').strip()
                    actresses.append(actress)
                elif(index == 2): 
                    movie = l.find(text=True).encode('utf-8').strip()
                    films.append(movie)
        index = index+1  


# In[38]:

# Here we extract the years. Because these awards started in 1936 all the years are in the correct format
years = []
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')  
    if(len(cells) > 1):
        year = cells[0].find(text=True)
        years.append(year)


# In[39]:

# Check all the lists are the same length, they are
print(len(actresses))
print(len(films))
print(len(years))


# In[40]:

# Create a data frame for storing the lists
df_supActresses = pd.DataFrame()
df_supActresses["Year"] = pd.to_numeric(years, errors='coerce')
df_supActresses["Actress"] = actresses
df_supActresses["Film"] = films
# Print data frame
df_supActresses


# In[41]:

# Print the number of rows in each data frame
print(df_picture.shape[0])
print(df_directors.shape[0])
print(df_actors.shape[0])
print(df_actresses.shape[0])
print(df_supActors.shape[0])
print(df_supActresses.shape[0])


# In[42]:

# Now all the data has been read into data frames, the next step is to connect to MYSQL and store it in the database
from sqlalchemy import create_engine    # for connecting to MySQL
from MySQL_connect import config        # import MySQL_connect.py for connection parameters

# use the parameters from file to create connection variables
user = config['user']
password = config['password']
host = config['host']
db = config['db']

# Connection object for MySQL
engine = create_engine("mysql+mysqldb://"+user+":"+password+"@"+host+"/"+db+"?charset=utf8")


# In[43]:

# Insert the data from each data frame into tables. If the table already exists overwrite it
df_picture.to_sql('best_picture', con=engine, if_exists='replace', index_label='id')
df_directors.to_sql('best_director', con=engine, if_exists='replace', index_label='id')
df_actors.to_sql('best_actor', con=engine, if_exists='replace', index_label='id')
df_actresses.to_sql('best_actress', con=engine, if_exists='replace', index_label='id')
df_supActors.to_sql('best_supporting_actor', con=engine, if_exists='replace', index_label='id')
df_supActresses.to_sql('best_supporting_actress', con=engine, if_exists='replace', index_label='id')


# In[44]:

# Show that the tables have been created
res = engine.execute("SHOW TABLES")
for x in res:
    print(x)


# In[45]:

# Now lets run some queries on the tables
# First return the number of row in each table
num_res = engine.execute("SELECT COUNT(*) FROM best_picture")
print("Best Picture number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM best_director")
print("Best Director number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM best_actor")
print("Best Actor number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM best_actress")
print("Best Actress number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM best_supporting_actor")
print("Best Supporting Actor number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM best_supporting_actress")
print("Best Supporting Actress number of rows")
for x in num_res:
    print(x)


# In[46]:

from prettytable import PrettyTable    # allow us to output results of queries in table format


# In[47]:

# Return a list of actors who have won more than 1 Oscar. In descending order of wins
actor_mostWins = engine.execute("SELECT actor, COUNT(actor) AS total_wins FROM best_actor GROUP BY actor HAVING total_wins > 1 ORDER BY total_wins DESC, actor ASC")
table = PrettyTable(['Actor', 'Wins'])
for x in actor_mostWins:
    table.add_row([x['actor'], x['total_wins']])
print(table)


# In[48]:

# Return a list of actresses who have won more than 1 Oscar. In descending order of wins
actress_mostWins = engine.execute("SELECT actress, COUNT(actress) AS total_wins FROM best_actress GROUP BY actress HAVING total_wins > 1 ORDER BY total_wins DESC, actress ASC")
table = PrettyTable(['Actress', 'Wins'])
for x in actress_mostWins:
    table.add_row([x['actress'], x['total_wins']])
print(table)


# In[49]:

# Return a list of directors who have won more than 1 Oscar. In descending order of wins
director_mostWins = engine.execute("SELECT director, COUNT(director) AS total_wins FROM best_director GROUP BY director HAVING total_wins > 1 ORDER BY total_wins DESC, director ASC")
table = PrettyTable(['Director', 'Wins'])
for x in director_mostWins:
    table.add_row([x['director'], x['total_wins']])
print(table)


# In[50]:

# Return a list of supporting actors who have won more than 1 Oscar. In descending order of wins
supActor_mostWins = engine.execute("SELECT actor, COUNT(actor) AS total_wins FROM best_supporting_actor GROUP BY actor HAVING total_wins > 1 ORDER BY total_wins DESC, actor ASC")
table = PrettyTable(['Actor', 'Wins'])
for x in supActor_mostWins:
    table.add_row([x['actor'], x['total_wins']])
print(table)


# In[51]:

# Return a list of supporting actresses who have won more than 1 Oscar. In descending order of wins
actress_mostWins = engine.execute("SELECT actress, COUNT(actress) AS total_wins FROM best_supporting_actress GROUP BY actress HAVING total_wins > 1 ORDER BY total_wins DESC, actress ASC")
table = PrettyTable(['Actress', 'Wins'])
for x in actress_mostWins:
    table.add_row([x['actress'], x['total_wins']])
print(table)


# In[52]:

# Return a list of best picture winning directors/companies in descending order of total wins
# This query is more complex because the nominee column can have multiple names in it. We are interested in the first name as
# that is usually the director. The names can be seperated by commas or 'and' so we use search for the position of the first comma.
# If a comma is found then use that as the maximum index for the substring. If not then search for the position of ' and ' and
# use that as the maximum index. Return the substring
picture_mostWins = engine.execute("SELECT IF (POSITION(',' IN nominee) > 0 , SUBSTRING(nominee, 1, POSITION(',' IN nominee) -1) , IF(POSITION(' and ' IN nominee) > 0, SUBSTRING(nominee, 1, POSITION(' and ' IN nominee)), nominee) ) AS director, COUNT(nominee) AS total_wins FROM best_picture GROUP BY director ORDER BY total_wins DESC, director ASC")
table = PrettyTable(['Director/Company', 'Wins'])
for x in picture_mostWins:
    table.add_row([x['director'], x['total_wins']])
print(table)


# In[ ]:



