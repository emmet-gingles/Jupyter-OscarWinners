
# coding: utf-8

# In[1]:

# This project follows the same structure as Oscar_Nominees.ipynb but it focuses on all nominees not just the winners


# In[2]:

# Import functions from file
from functions import loadPage, extractYears, extractFilmData, createDataFrame


# In[3]:

# Page 1- Best Picture
# Call function to read in URL and retrieve data from the page
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
# From the data get all the tables that have the following class
tables = data.findAll("table", class_= "wikitable")


# In[4]:

# Call function to get the years and the number of films nominated for each year
yearData = extractYears("picture", tables, False)
# Create lists from the dictionary columns
years = yearData['years']
numFilms = yearData['numFilms']


# In[5]:

# Call function to get the film data from tables. 
# Notice the third parameter False. This is to change its default value of True so that the function returns all data not just 
# the winners
data = extractFilmData("picture", tables, False)
# Create lists from the dictionary columns
producers = data['names']
films = data['films']
winners = data['winners']


# In[6]:

# Check the length of each lists. Nominees and films are the same length.
print(len(years))
print(len(producers))
print(len(films))


# In[7]:

# Call function to create a dataframe by passing in the lists
df_picture = createDataFrame("picture", {"films": films, "producers": producers}, {"years": years, "numFilms": numFilms}, winners)
# Show the dataframe with all the winning films
df_picture.loc[df_picture["Winner"] == "Yes"]


# In[8]:

# Page2 - Best Director
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director")
tables = data.findAll("table", class_= "wikitable sortable")


# In[9]:

yearData = extractYears("director", tables, False)
years = yearData['years']
numFilms = yearData['numFilms']


# In[10]:

data = extractFilmData("director", tables, False)
directors = data['names']
films = data['films']
winners = data['winners']


# In[11]:

# Check the length of each list. Directors and films are not the same. This is because in the years 1929, 1930 and 1938 a 
# director was twice nominated
print(len(years))
print(len(directors))
print(len(films))


# In[12]:

# Lets amend this by inserting the necessary director at each position
directors.insert(45, directors[44])
directors.insert(13, directors[12])
directors.insert(10, directors[9])


# In[13]:

# Now they are the same length
print(len(years))
print(len(directors))
print(len(films))


# In[14]:

df_directors = createDataFrame("director", {"directors": directors, "films": films}, {"years": years, "numFilms": numFilms}, winners)
df_directors.loc[df_directors["Winner"] == "Yes"]


# In[15]:

# Now check the years 1929, 1930 and 1938 and see the directors twice nominated
df_directors.loc[(df_directors['Year'].isin([1929, 1930, 1938])) & (df_directors['Winner'] == "No")]


# In[16]:

# Page 3- Best Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[17]:

yearData = extractYears("actor", tables, False)
years = yearData['years']
numFilms = yearData['numFilms']


# In[18]:

data = extractFilmData("actor", tables, False)
actors = data['names']
films = data['films']
winners = data['winners']


# In[19]:

# Check the length of the lists. Actors and films are not the same. This is due to several years having actors nominated for 
# multiple films and several films having multiple actors nominated
print(len(years))
print(len(actors))
print(len(films))


# In[20]:

# To amend this we have to insert several times in both lists
actors.insert(1, actors[0])
actors.insert(3, actors[2])
actors.insert(13, actors[12])
actors.insert(15, actors[14])
films.insert(33, films[32])
films.insert(125, films[124])
films.insert(178, films[177])
films.insert(218, films[217])
films.insert(275, films[274])


# In[21]:

# Now they are the same length
print(len(years))
print(len(actors))
print(len(films))


# In[22]:

# Because of the actors we just inserted, we need to update numFilms to accomodate this
numFilms[0] = int(numFilms[0]) + 2
numFilms[2] = int(numFilms[2]) + 2


# In[23]:

df_actors = createDataFrame("actor", {"films": films, "actors": actors}, {"years": years, "numFilms": numFilms}, winners)
df_actors.loc[df_actors["Winner"] == "Yes"]


# In[24]:

# Now check the years 1928 and 1930 and see the actors that were twice nominated
df_actors.loc[(df_actors["Year"].isin([1928, 1930])) & (df_actors["Winner"] == "No")]


# In[25]:

# Now check the years inserted and see that multiple actor nominations for the same films
years = [1935, 1953, 1964, 1972, 1983]
df_actors.loc[(df_actors["Year"].isin(years)) & (df_actors["Winner"] == "No")]


# In[26]:

# Page 4 - Best Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[27]:

yearData = extractYears("actress", tables, False)
years = yearData['years']
numFilms = yearData['numFilms']


# In[28]:

data = extractFilmData("actress", tables, False)
actresses = data['names']
films = data['films']
winners = data['winners']


# In[29]:

# Check the lengths of the lists. They are not the same. The reasons for this are 
# 1. The same actress receiving multiple nominations for different films in the same year
# 2. Different actresses receiving nominations for the same film
print(len(years))
print(len(actresses))
print(len(films))


# In[30]:

actresses.insert(1, actresses[0])
actresses.insert(2, actresses[0])
actresses.insert(15, actresses[14])
films.insert(111, films[110])
films.insert(158, films[157])


# In[31]:

# Now they are the same length
print(len(years))
print(len(actresses))
print(len(films))


# In[32]:

# Because of the actresses we just inserted, we need to update numFilms to accomodate this
numFilms[0] = int(numFilms[0]) +2
numFilms[2] = int(numFilms[2]) +1


# In[33]:

df_actresses = createDataFrame("actress", {"films": films, "actresses": actresses}, {"years": years, "numFilms": numFilms}, winners)
df_actresses.loc[df_actresses["Winner"] == "Yes"]


# In[34]:

# Now check the year 1930 and see Greta Garbo received two nominations
df_actresses.loc[(df_actresses["Year"] == 1930) & (df_actresses["Winner"] == "No")]


# In[35]:

# Now check the years 1950 and 1959 and see that multiple actress nominations for the same films
df_actresses.loc[(df_actresses["Year"].isin([1950, 1959])) & (df_actresses["Winner"] == "No")]


# In[36]:

# Page 5 - Best Supporting Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[37]:

yearData = extractYears("supporting actor", tables, False)
years = yearData['years']
numFilms = yearData['numFilms']


# In[38]:

data = extractFilmData("supporting actor", tables, False)
actors = data['names']
films = data['films']
winners = data['winners']


# In[39]:

# Check the length of the lists. Actors and films are not the same because in several years multiple actors were nominated for
# the same film
print(len(years))
print(len(actors))
print(len(films))


# In[40]:

films.insert(88, films[87])
films.insert(92, films[91])
films.insert(93, films[91])
films.insert(109, films[108])
films.insert(117, films[116])
films.insert(129, films[128])
films.insert(183, films[182])
films.insert(184, films[182])
films.insert(194, films[193])
films.insert(252, films[251])
films.insert(278, films[277])


# In[41]:

# Now they are the same length
print(len(years))
print(len(actors))
print(len(films))


# In[42]:

df_supActors = createDataFrame("supporting actor", {"films": films, "actors": actors}, {"years": years, "numFilms": numFilms}, winners)
df_supActors.loc[df_supActors["Winner"] == "Yes"]


# In[43]:

# Now check each of the years that were inserted and see that each one has two or more occurrences of the same film
years = [1953, 1954, 1957, 1959, 1961, 1972, 1974, 1986, 1991]
df_supActors.loc[(df_supActors["Year"].isin(years)) & (df_supActors["Winner"] == "No")]


# In[44]:

# Page 6 - Best Supporting Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[45]:

yearData = extractYears("supporting actress", tables, False)
years = yearData['years']
numFilms = yearData['numFilms']


# In[46]:

data = extractFilmData("supporting actress", tables, False)
actresses = data['names']
films = data['films']
winners = data['winners']


# In[47]:

# Check the length of the lists. Actresses and films are not the same because in several years multiple actresses were nominated 
# for the same film
print(len(years))
print(len(actresses))
print(len(films))


# In[48]:

films.insert(28, films[27])
films.insert(47, films[46])
films.insert(62, films[61])
films.insert(68, films[67])
films.insert(94, films[93])
films.insert(109, films[108])
films.insert(118, films[117])
films.insert(137, films[136])
films.insert(138, films[136])
films.insert(148, films[147])
films.insert(267, films[266])
films.insert(323, films[322])
films.insert(327, films[326])
films.insert(362, films[361])
films.insert(414, films[413])


# In[49]:

# Now they are the same length
print(len(years))
print(len(actresses))
print(len(films))


# In[50]:

df_supActresses = createDataFrame("supporting actress", {"films": films, "actresses": actresses}, {"years": years, "numFilms": numFilms}, winners)
df_supActresses.loc[df_supActresses["Winner"] == "Yes"]


# In[51]:

# Now check each of the years that were inserted and see that each one has two or more occurrences of the same film
years = [1941, 1945, 1948, 1949, 1954, 1957, 1959, 1963, 1965, 1989, 2000, 2001, 2008, 2018]
df_supActresses.loc[(df_supActresses["Year"].isin(years)) & (df_supActresses["Winner"] == "No")]


# In[52]:

# Look at the number of rows in each data frame
print("total best picture winners       " '{0}'.format(df_picture.shape[0]))
print("total best director winners      " '{0}'.format(df_directors.shape[0]))
print("total best actor winners         " '{0}'.format(df_actors.shape[0]))
print("total best actress winners       " '{0}'.format(df_actresses.shape[0]))
print("total best supp. actor winners   " '{0}'.format(df_supActors.shape[0]))
print("total best supp. actress winners " '{0}'.format(df_supActresses.shape[0]))


# In[53]:

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


# In[54]:

# Insert the data from each data frame into tables. If the table already exists overwrite it
df_picture.to_sql('nominee_best_picture', con=engine, if_exists='replace', index_label='id')
df_directors.to_sql('nominee_best_director', con=engine, if_exists='replace', index_label='id')
df_actors.to_sql('nominee_best_actor', con=engine, if_exists='replace', index_label='id')
df_actresses.to_sql('nominee_best_actress', con=engine, if_exists='replace', index_label='id')
df_supActors.to_sql('nominee_best_supporting_actor', con=engine, if_exists='replace', index_label='id')
df_supActresses.to_sql('nominee_best_supporting_actress', con=engine, if_exists='replace', index_label='id')
# You can ignore any warnings here. They are just foreign characters and are replaced by '?' in database


# In[55]:

# Show that the tables have been created
res = engine.execute("SHOW TABLES")
for x in res:
    print x


# In[56]:

# Now lets run some queries on the tables
# First return the number of rows in each table
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_picture")
print("Nominee Best Picture number of rows")
for x in num_res:
    print x
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_director")
print("Nominee Best Director number of rows")
for x in num_res:
    print x
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_actor")
print("Nominee Best Actor number of rows")
for x in num_res:
    print x
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_actress")
print("Nominee Best Actress number of rows")
for x in num_res:
    print x
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_supporting_actor")
print("Nominee Best Supporting Actor number of rows")
for x in num_res:
    print x
num_res = engine.execute("SELECT COUNT(*) FROM nominee_best_supporting_actress")
print("Nominee Best Supporting Actress number of rows")
for x in num_res:
    print x


# In[57]:

# For displaying results in a table format
from prettytable import PrettyTable


# In[58]:

# Query: Return a list of actors ordered by most nominations and wins
# Explained: We are using two tables - nominee_best_actor and nominee_best_supporting_actor. Therefore we use UNION inside a
# subquery to combine the results of two queries into one set. Each query counts the number of nominatins for each actor as well 
# as the number of times they won. We get the total for each actor by summing the results of each query.
actor_mostNom = engine.execute("SELECT actor, SUM(total_wins) AS total_wins, SUM(total_nom) AS total_nom FROM (SELECT actor, COUNT(actor) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_actor GROUP BY actor UNION SELECT actor, COUNT(actor) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_supporting_actor GROUP BY actor) AS res GROUP BY actor ORDER BY total_nom DESC, total_wins DESC, actor ASC")

table = PrettyTable(['Actor', 'Nominations', 'Wins'])
for x in actor_mostNom:
    table.add_row([x['actor'], x['total_nom'], x['total_wins']])
print(table)


# In[59]:

# Query: Return a list of actresses ordered by most nominations and wins
# Explained: We are using two tables - nominee_best_actress and nominee_best_supporting_actress. Therefore we use UNION inside a
# subquery to combine the results of two queries into one set. Each query counts the number of nominations for each actress as well 
# as the number of times they won. We get the total for each actress by summing the results of each query.
supActor_mostNom = engine.execute("SELECT actress, SUM(total_wins) AS total_wins, SUM(total_nom) AS total_nom FROM (SELECT actress, COUNT(actress) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_actress GROUP BY actress UNION SELECT actress, COUNT(actress) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_supporting_actress GROUP BY actress) AS res GROUP BY actress ORDER BY total_nom DESC, total_wins DESC, actress ASC")

table = PrettyTable(['Actress', 'Nominations', 'Wins'])
for x in supActor_mostNom:
    table.add_row([x['actress'], x['total_nom'], x['total_wins']])
print(table)


# In[60]:

# Query: Return a list of directors ordered by most nominations and wins
# Explained: Because the 1st Osars had winners in different categories we have to use substring to get rid of any brackets 
# at the end of any names. With the names correct we can now count the number of nominations and the number of wins for each 
# director.
director_mostNom = engine.execute("SELECT director, SUM(total_wins) AS total_wins, SUM(total_nom) AS total_nom FROM (SELECT IF(SUBSTRING(director, LENGTH(director)) = ')', SUBSTRING(director, 1, POSITION('(' IN director) -1), director) AS director, COUNT(IF(SUBSTRING(director, LENGTH(director)) = ')', SUBSTRING(director, 1, POSITION('(' IN director) -1), director)) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_director GROUP BY director ) AS res GROUP BY director ORDER BY total_nom DESC, total_wins DESC, director ASC")
 
table = PrettyTable(['Director', 'Nominations', 'Wins'])
for x in director_mostNom:
    table.add_row([x['director'], x['total_nom'], x['total_wins']])
print(table)


# In[61]:

# Query: Return a list of producers ordered by most nominations and wins
# Explained: This query is difficult because the producers column can have multiple names in it. We are interested in the first name as
# that is usually the director. The names can be seperated by either commas or 'and' so we use search for the position of 
# the first comma. If a comma is found then use that as the maximum index for the substring. If not then search for the 
# position of ' and ' and use that as the maximum index. Finally return the substring and use it to count each occurrence and
# the number of wins for each.
picture_mostNom = engine.execute("SELECT IF (POSITION(',' IN producers) > 0, SUBSTRING(producers, 1, POSITION(',' IN producers) -1) , IF(POSITION(' and ' IN producers) > 0, SUBSTRING(producers, 1, POSITION(' and ' IN producers)), producers) ) AS name, COUNT(producers) AS total_nom, COUNT(IF(winner = 'Yes', 1, null)) AS total_wins FROM nominee_best_picture GROUP BY name ORDER BY total_nom DESC, total_wins DESC, name ASC")
 
table = PrettyTable(['Producer', 'Nominations', 'Wins'])
for x in picture_mostNom:
    table.add_row([x['name'], x['total_nom'], x['total_wins']])
print(table)

