
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

import pandas as pd          # For creating dataframes


# In[3]:

# Import functions from file
from functions import loadPage, extractYears, extractFilmData


# In[4]:

# Page 1- Best Picture
# Call function to read in URL and retrieve data from the page
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
# From the data get all the tables that have the following class
tables = data.findAll("table", class_= "wikitable")


# In[5]:

# Call function to get the film data from tables
data = extractFilmData("picture", tables)
# Create lists from the dictionary columns
films = data["films"]
producer = data["names"]
# Call function to get a list of years from tables
years = extractYears("picture", tables)


# In[6]:

# Check the length of each list. They are all the same length.
print(len(films))
print(len(producer))
print(len(years))


# In[7]:

# Create a data frame for storing each Best Picture Winner
df_picture = pd.DataFrame()
df_picture["Year"] = pd.to_numeric(years, errors='coerce')
df_picture["Film"] = films
df_picture["Producers"] = producer
# Show the dataframe
df_picture


# In[8]:

# Page2 - Best Director
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director")
tables = data.findAll("table", class_= "wikitable sortable")


# In[9]:

data = extractFilmData("director", tables)
films = data["films"]
directors = data["names"]
years = extractYears("director", tables)


# In[10]:

# Check the length of each list. Due to the 1st Oscars having multiple awards they are not the same length
print(len(films))
print(len(directors))
print(len(years))


# In[11]:

# To amend this lets insert a year at the position 1 with the same value as the year at position 0
years.insert(1, years[0])


# In[12]:

# Now they are all the same length
print(len(films))
print(len(directors))
print(len(years))


# In[13]:

df_directors = pd.DataFrame()
df_directors["Year"] = pd.to_numeric(years, errors='coerce')
df_directors["Director"] = directors
df_directors["Film"] = films
# Look at the data frame and see the first two indexes have the same year.
df_directors


# In[14]:

# Page 3- Best Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[15]:

data = extractFilmData("actor", tables)
films = data["films"]
actors = data["names"]
years = extractYears("actor", tables)


# In[16]:

# Check the length of each list. They are not the same length. There are two reasons for this.
# 1. In the 1st Oscars ceremony, the actor won awards for two films
# 2. In 1932 there was a tie for 1st place
print(len(films))
print(len(actors))
print(len(years))


# In[17]:

# To amend this lets insert the actor at position 0 into position 1 and insert the appropriate years at position 1 and 6 of years
actors.insert(1, actors[0])
years.insert(1, years[0])
years.insert(6, years[5])


# In[18]:

# Now they are all the same length
print(len(films))
print(len(actors))
print(len(years))


# In[19]:

df_actors = pd.DataFrame()
df_actors["Year"] = pd.to_numeric(years, errors='coerce')
df_actors["Actor"] = actors
df_actors["Film"] = films
# Show the dataframe and look at years 1928 and 1932
df_actors


# In[20]:

# Page 4- Best Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[21]:

data = extractFilmData("actress", tables)
films = data["films"]
actresses = data["names"]
years = extractYears("actress", tables)


# In[22]:

# Check the length of each list. They are not the same. There are two reasons for this.
# 1. In the 1st Oscars the actress won awards for three films
# 2. In 1968 there was a tie for 1st place
print(len(actresses))
print(len(films))
print(len(years))


# In[23]:

# Lets amend this by inserting the actress at the position 0 to positions 1 and 2. Do the same for the years
# Also insert the year at position 40 into position 41
actresses.insert(1, actresses[0])
actresses.insert(2, actresses[1])
years.insert(41, years[40])
years.insert(1, years[0])
years.insert(2, years[1])


# In[24]:

# Now they are all the same length
print(len(actresses))
print(len(films))
print(len(years))


# In[25]:

df_actresses = pd.DataFrame()
df_actresses["Year"] = pd.to_numeric(years, errors='coerce')
df_actresses["Actress"] = actresses
df_actresses["Film"] = films
# Show the dataframe and look at the first three rows which have the same year and actress but different films
df_actresses


# In[26]:

# Now check the year 1968 and see two actresses and two films
df_actresses.loc[df_actresses['Year'] == 1968]


# In[27]:

# Page 5 - Best Supporting Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[28]:

data = extractFilmData("supporting actor", tables)
films = data["films"]
actors = data["names"]
years = extractYears("supporting actor", tables)


# In[29]:

# Check all lists are the same length, they are
print(len(actors))
print(len(films))
print(len(years))


# In[30]:

df_supActors = pd.DataFrame()
df_supActors["Year"] = pd.to_numeric(years, errors='coerce')
df_supActors["Actor"] = actors
df_supActors["Film"] = films
df_supActors


# In[31]:

# Page 6 - Best Supporting Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[32]:

data = extractFilmData("supporting actress", tables)
films = data["films"]
actresses = data["names"]
years = extractYears("supporting actress", tables)


# In[33]:

# Check all the lists are the same length, they are
print(len(actresses))
print(len(films))
print(len(years))


# In[34]:

df_supActresses = pd.DataFrame()
df_supActresses["Year"] = pd.to_numeric(years, errors='coerce')
df_supActresses["Actress"] = actresses
df_supActresses["Film"] = films
df_supActresses


# In[35]:

# Print the number of rows in each data frame
print("total best picture winners       " '{0}'.format(df_picture.shape[0]))
print("total best director winners      " '{0}'.format(df_directors.shape[0]))
print("total best actor winners         " '{0}'.format(df_actors.shape[0]))
print("total best actress winners       " '{0}'.format(df_actresses.shape[0]))
print("total best supp. actor winners   " '{0}'.format(df_supActors.shape[0]))
print("total best supp. actress winners " '{0}'.format(df_supActresses.shape[0]))


# In[36]:

# Now all the data has been read into data frames, the next step is to connect to MYSQL and store it in the database
from sqlalchemy import create_engine    # For connecting to MySQL
from MySQL_connect import config        # Import connection parameters from file

# Use the parameters to create connection variables
user = config['user']
password = config['password']
host = config['host']
db = config['db']

# Connection object for MySQL
engine = create_engine("mysql+mysqldb://"+user+":"+password+"@"+host+"/"+db+"?charset=utf8")


# In[37]:

# Insert the data from each data frame into tables. If the table already exists overwrite it
df_picture.to_sql('winner_best_picture', con=engine, if_exists='replace', index_label='id')
df_directors.to_sql('winner_best_director', con=engine, if_exists='replace', index_label='id')
df_actors.to_sql('winner_best_actor', con=engine, if_exists='replace', index_label='id')
df_actresses.to_sql('winner_best_actress', con=engine, if_exists='replace', index_label='id')
df_supActors.to_sql('winner_best_supporting_actor', con=engine, if_exists='replace', index_label='id')
df_supActresses.to_sql('winner_best_supporting_actress', con=engine, if_exists='replace', index_label='id')


# In[38]:

# Show that the tables have been created
res = engine.execute("SHOW TABLES")
for x in res:
    print(x)


# In[39]:

# Now lets run some queries on the tables
# First return the number of rows in each table
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_picture")
print("Best Picture number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_director")
print("Best Director number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_actor")
print("Best Actor number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_actress")
print("Best Actress number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_supporting_actor")
print("Best Supporting Actor number of rows")
for x in num_res:
    print(x)
num_res = engine.execute("SELECT COUNT(*) FROM winner_best_supporting_actress")
print("Best Supporting Actress number of rows")
for x in num_res:
    print(x)


# In[40]:

# For displaying results in a table format
from prettytable import PrettyTable    


# In[41]:

# Query: Return a list of actors who have won an Oscar. In descending order of wins
# Explained: We are using two tables - best_actor and best_supporting_actor. Therefore we use UNION inside a subquery to 
# combine the results of two queries into one set. Each query counts the total for each actor so we sum both totals to get 
# the total number of wins for each actor.
actor_mostWins = engine.execute("SELECT actor, SUM(total_wins) AS total_wins FROM (SELECT actor, COUNT(actor) AS total_wins FROM winner_best_actor GROUP BY actor UNION SELECT actor, COUNT(actor) AS total_wins FROM winner_best_supporting_actor GROUP BY actor) AS res GROUP BY actor ORDER BY total_wins DESC, actor ASC")

table = PrettyTable(['Actor', 'Wins'])
for x in actor_mostWins:
    table.add_row([x['actor'], x['total_wins']])
print(table)


# In[42]:

# Query: Return a list of actresses who have won an Oscar. In descending order of wins
# Explained: We are using two tables - best_actress and best_supporting_actress. Therefore we use UNION inside a subquery to 
# combine the results of two queries into one set. Each query counts the total for each actress so we sum both totals to get 
# the total number of wins for each actress.
actress_mostWins = engine.execute("SELECT actress, SUM(total_wins) AS total_wins FROM ( SELECT actress, COUNT(actress) AS total_wins FROM winner_best_actress GROUP BY actress UNION SELECT actress, COUNT(actress) AS total_wins FROM winner_best_supporting_actress GROUP BY actress) AS res GROUP BY actress ORDER BY total_wins DESC, actress ASC")

table = PrettyTable(['Actress', 'Wins'])
for x in actress_mostWins:
    table.add_row([x['actress'], x['total_wins']])
print(table)


# In[43]:

# Query: Return a list of directors who have won an Oscar. In descending order of wins
# Explained: Because the 1st Osars had winners in different categories we have to use substring to get rid of any brackets at
# the end of any names. With the names correct we can now get the total for each director
director_mostWins = engine.execute("SELECT director, SUM(num_wins) AS total_wins FROM (SELECT IF(SUBSTRING(director, LENGTH(director)) = ')', SUBSTRING(director, 1, POSITION('(' IN director) -1), director) AS director, COUNT( IF(SUBSTRING(director, LENGTH(director)) = ')', SUBSTRING(director, 1, POSITION('(' IN Director) -1), Director)) AS num_wins FROM winner_best_director GROUP BY Director ) AS res GROUP BY Director ORDER BY total_wins DESC, director ASC");

table = PrettyTable(['Director', 'Wins'])
for x in director_mostWins:
    table.add_row([x['director'], x['total_wins']])
print(table)


# In[44]:

# Query: Return a list of best picture winning producers in descending order of total wins
# Explained: This query is difficult because the producers column can have multiple names in it. We are interested in the first
# name as that is usually the director. The names can be seperated by either commas or 'and' so we use search for the position 
# of the first comma. If a comma is found then use that as the maximum index for the substring. If not then search for the 
# position of ' and ' and use that as the maximum index. Finally return the substring and use it for the count.
picture_mostWins = engine.execute("SELECT IF (POSITION(',' IN producers) > 0, SUBSTRING(producers, 1, POSITION(',' IN producers) -1) , IF(POSITION(' and ' IN producers) > 0, SUBSTRING(producers, 1, POSITION(' and ' IN producers)), producers) ) AS name, COUNT(producers) AS total_wins FROM winner_best_picture GROUP BY name ORDER BY total_wins DESC, name ASC")

table = PrettyTable(['Producer', 'Wins'])
for x in picture_mostWins:
    table.add_row([x['name'], x['total_wins']])
print(table)

