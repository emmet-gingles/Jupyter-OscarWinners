
# coding: utf-8

# In[1]:

# This project follows the same structure as Oscar_Nominees.ipynb but it focuses on all nominees not just the winners


# In[1]:

import urllib2;                    # for retrieving the contents of a page
from bs4 import BeautifulSoup;     # for parsing the contents of a page to HTML
import pandas as pd                # for creating dataframes


# In[2]:

# Function that takes in a URL and returns the contents of the page
def loadPage(url):
    page = urllib2.urlopen(url)
    data = BeautifulSoup(page, "lxml")
    return data

# Style of table cells that have Oscar winners in them
winnerStyle = 'background:#FAEB86'


# In[3]:

# Page 1- Best Picture
# Call function to read in URL and retrieve data from the page
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
# from the data get all the tables that have the following class
tables = data.findAll("table", class_= "wikitable")


# In[4]:

# Here we extract each film, nominee and year
# There are tables for each decade starting from the 1920's. We want to go through each table and extract the appropriate information
# Create empty lists for each film, nominee and year
films = []
nominees = []
years = []
# Create an empty list for Oscar winners
winners = []
# Dataframe will be used to store each year along with the number of rows it covers ie. the rowspan
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

# There are ten tables so we use range to keep track 
for i in range(0, 11):
    # First get the year. Search the table for all cells that match the style
    for row in tables[i].findAll("td", style="text-align:center"):
        # Check that cell has a rowspan attribute and set it to a variable
        if row.has_attr("rowspan"):
            nrows = row["rowspan"]
            # Get each link within that cell
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
            # Add year and nrows to dataframe
            df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
            # Add year to list of years
            years.append(int(year))
        
    # Next we want information about each film. Find all table rows
    for row in tables[i].findAll("tr"):
        # Variable to determine whether or not film is an Oscar winner. Default value is false
        isWinner = False
        # Check each row has a style attribute, then check it starts with the winnerStyle ie. 'background:#FAEB86' or 
        # 'background:#FAEB86;'. If it is then it is an Oscar winner so set isWinner to true
        if row.has_attr("style"):
            if(row["style"].startswith(winnerStyle)):
                isWinner = True
        # Get each cell within that row
        cells = row.findAll('td')
        # Get the text from within the first cell, encode it to utf-8 and add it to the films list
        if(len(cells) > 1):        
            film = cells[0].find(text=True).encode('utf-8').strip()
            films.append(film)
            # If true then add the film to the list of winners
            if(isWinner):
                winners.append(film)
            # Get the text from within the second cell - text saved as an array  
            nominee = cells[1].findAll(text=True)
            # If the last index is a line break then remove it from variable
            if(len(nominee) > 1):
                if(nominee[len(nominee)-1] == '\n'):
                    nominee = nominee[:-1] 
            # If first item ends in a line break then remove it
            if (nominee[0].endswith("\n")):
                nominee = nominee[0][0:-1]
            # Join all the text to a single string and append it to the list of nominees
            nominees.append("".join(nominee).encode('utf-8').strip() )     


# In[5]:

# Check the length of each lists. Nominees and films are the same length
print(len(years))
print(len(nominees))
print(len(films))


# In[6]:

# Data frame to store the following information - year, film, nominees and whether or not it is an Oscar winner
df_picture = pd.DataFrame(columns = ["Year","Film","Nominee","Winner"])
# Variable to track the list index to start from - 0 to start with
start = 0
# Iterate through each row of data frame and get the year and number of films for each row
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    # Variable to track index to stop at - the number of films - 1
    end = start + numFilms-1
    # Loop through from start up to the end and for each index get the respective film and nominee
    for i in range(start, end):
        # Variable to determine whether or not film is an Oscar winner - default value is "No"
        isWinner = "No"
        film = films[i]
        nominee = nominees[i]
        # If the film is in the list of winners then set variable to "Yes"
        if film in winners:
            isWinner = "Yes" 
        # Append all variable to data frame
        df_picture.loc[df_picture.shape[0]] = [year, film, nominee, isWinner]
    # Increment start 
    start = start+numFilms-1
# Print data frame to show each Oscar winner
df_picture.loc[df_picture["Winner"] == "Yes"]


# In[7]:

# Page2 - Best Director
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director")
tables = data.findAll("table", class_= "wikitable sortable")


# In[8]:

# Here we extract each film, director and year - All subsequent pages follow the a similar process
# Create empty lists for each film, director and year
films = []
directors = []
years = []
# We use a dictionary to store both the film and the director
winners = {'director': [], 'film': []}
# Dataframe will be used to store each year along with the number of rows it covers ie. the rowspan
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

# First get the year. Search the table for all table headers with the scope "row"
for row in tables[0].findAll("th", scope="row"):
    # Check that cell has a rowspan attribute and set it to a variable
    if row.has_attr("rowspan"):
        nrows = row["rowspan"]
        # Get each link within that cell
        cells = row.findAll('a')
        # If year is all in one link and in a format like 1927/28 then we want the first two and last two charaters so that 
        # it will be 1928
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
        # Add year and nrows to dataframe
        df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
        # Add year to list of years
        years.append(int(year))

# Next we want information about each film. Find all table rows
for row in tables[0].findAll("tr"):
    # Get each cell within that row
    cells = row.findAll('td')   
    # Get the text from within the first cell, encode it to utf-8 and add it to the films list
    if(len(cells) > 1):
        # Variable to determine whether or not it is an Oscar winner - default is false
        isWinner = False
        # # Check each row has a style attribute, then check it starts with the winnerStyle ie. 'background:#FAEB86' or 
        # 'background:#FAEB86;'. If it does then set isWinner to true
        if(cells[0].has_attr("style")):  
            if(cells[0]["style"].startswith(winnerStyle)):
                isWinner = True
        # Get all text from the first cell. We don't want the last part as this has "\n" characters
        director = cells[0].findAll(text=True)[:-1]
        # Join together array into a string and add to list of directors
        director = "".join(director).encode('utf-8').strip()
        directors.append(director)        
        # Get the text from within the second cell, encode it and add it to the list of nominees    
        film = cells[1].find(text=True).encode('utf-8').strip() 
        films.append(film) 
        # If it is an Oscar winner add it to list
        if(isWinner):
            winners['director'].append(director)
            winners['film'].append(film)
    # In case a director has more than one film nominated, get all films in cell  
    elif(len(cells) == 1):
        if cells[0].has_attr("rowspan") == False and cells[0].has_attr("colspan") == False:
            film = cells[0].find(text=True).encode('utf-8').strip() 
            films.append(film) 


# In[9]:

# Check the length of each list. Directors and films are not the same. This is because in the years 1929, 1930 and 1938 a 
# director was twice nominated
print(len(years))
print(len(directors))
print(len(films))


# In[10]:

# Lets amend this by inserting the necessary director at each position
directors.insert(45, directors[44])
directors.insert(13, directors[12])
directors.insert(10, directors[9])


# In[11]:

# Now they are the same length
print(len(years))
print(len(directors))
print(len(films))


# In[12]:

df_directors = pd.DataFrame(columns = ["Year","Director","Film","Winner"])
start = 0
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    end = start + numFilms   
    for i in range(start, end):      
        isWinner = "No"
        film = films[i]
        director = directors[i]
        if director in winners['director'] and film in winners['film']:
            isWinner = "Yes"           
        df_directors.loc[df_directors.shape[0]] = [year,director,film,isWinner]
    start = start + numFilms
df_directors.loc[df_directors['Winner'] == "Yes"]


# In[13]:

# Now check the years 1929, 1930 and 1938 and see the directors twice nominated
df_directors["Year"] = df_directors["Year"].astype(int)
df_directors.loc[(df_directors['Year'].isin([1929, 1930, 1938])) & (df_directors['Winner'] == "No")]


# In[14]:

# Page 3- Best Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[15]:

# Here we extract each actor, film and year
films =[]
actors = []
years = []
winners = {'actor' : [], 'film' : [] }
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

for row in tables[0].findAll("th", scope="row"):
    if row.has_attr("rowspan"):
        nrows = row["rowspan"]
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
        df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
        years.append(int(year))
    
for row in tables[0].findAll("tr"):
    cells = row.findAll("td")    
    index = 0
    if(len(cells) > 1):  
        isWinner = False
        if(cells[0].has_attr("style")):  
            if(cells[0]["style"].startswith(winnerStyle)):
                isWinner = True
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actor = l.find(text=True).encode('utf-8').strip()
                    actors.append(actor)
                elif(index == 2): 
                    film = l.find(text=True).encode('utf-8').strip()
                    films.append(film)
                    if isWinner:
                        winners['actor'].append(actor)
                        winners['film'].append(film)
        index = index+1   


# In[16]:

# Check the length of the lists. Actors and films are not equal. This is due to several years having actors nominated for multiple
# films and serveral films having multiple actors nominated
print(len(years))
print(len(actors))
print(len(films))


# In[17]:

# To amend this we have to insert several times in both lists
actors.insert(1, actors[0])
actors.insert(3, actors[2])
actors.insert(13, actors[12])
actors.insert(15, actors[14])
films.insert(33, films[32])
films.insert(34, films[32])
films.insert(125, films[124])
films.insert(178, films[177])
films.insert(218, films[217])
films.insert(275, films[274])


# In[18]:

# Now they are the same length
print(len(years))
print(len(actors))
print(len(films))


# In[19]:

# Because of the actors inserted, the rowcount needs to be updated for the years 1928 and 1930. We increment the 
# current value by 2
print("before increment", int(df_yearRows.loc[0, ["Rows"]][0]))
df_yearRows.set_value(0, 'Rows', int(df_yearRows.loc[0, ["Rows"]][0]) +2)
print("after increment", int(df_yearRows.loc[0, ["Rows"]][0]))

print("before increment", int(df_yearRows.loc[2, ["Rows"]][0]))
df_yearRows.set_value(2, 'Rows', int(df_yearRows.loc[2, ["Rows"]][0]) +2)
print("before increment", int(df_yearRows.loc[2, ["Rows"]][0]))


# In[20]:

df_actors = pd.DataFrame(columns = ["Year","Actor","Film","Winner"])
start = 0
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    end = start + numFilms   
    for i in range(start, end):  
        isWinner = "No"
        actor = actors[i]   
        film = films[i]
        if actor in winners['actor'] and film in winners['film']:
            isWinner = "Yes"           
        df_actors.loc[df_actors.shape[0]] = [year,actor,film,isWinner]
    start = start + numFilms
df_actors.loc[df_actors['Winner'] == "Yes"]


# In[21]:

# Now check the years 1928 and 1930 and see the actors that were twice nominated
df_actors["Year"] = df_actors["Year"].astype(int)
df_actors.loc[(df_actors["Year"].isin([1928, 1930])) & (df_actors["Winner"] == "No")]


# In[22]:

# Now check the years inserted and see that multiple actor nominations for the same films
years = [1935, 1953, 1964, 1972, 1983]
df_actors.loc[(df_actors["Year"].isin(years)) & (df_actors["Winner"] == "No")]


# In[23]:

# Page 4 - Best Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[24]:

# Here we extract each actress, film and year
films =[]
actresses = []
years = []
winners = {'actress' : [], 'film' : [] }
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

for row in tables[0].findAll("th", scope="row"):
    if row.has_attr("rowspan"):
        nrows = row["rowspan"]
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
        df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
        years.append(int(year))
    
for row in tables[0].findAll("tr"):
    cells = row.findAll("td")    
    index = 0
    if(len(cells) > 1):  
        isWinner = False
        if(cells[0].has_attr("style")):  
            if(cells[0]["style"].startswith(winnerStyle)):
                isWinner = True
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actress = l.find(text=True).encode('utf-8').strip()
                    actresses.append(actress)                    
                elif(index == 2): 
                    film = l.find(text=True).encode('utf-8').strip()
                    films.append(film)
                    if isWinner:
                        winners['actress'].append(actress)
                        winners['film'].append(film)
        index = index+1   


# In[25]:

# Check the lengths of the lists. They are not the same. The reasons for this are 
# 1. The same actress receiving multiple nominations for different films in the same year
# 2. Different actresses receiving nominations for the same film
print(len(years))
print(len(actresses))
print(len(films))


# In[26]:

actresses.insert(1, actresses[0])
actresses.insert(2, actresses[0])
actresses.insert(15, actresses[14])
films.insert(111, films[110])
films.insert(158, films[157])


# In[27]:

# Now they are the same length
print(len(years))
print(len(actresses))
print(len(films))


# In[28]:

# Because of the actresses inserted, the rowcount needs to be updated for the years 1928 and 1930.
print("before increment", int(df_yearRows.loc[0, ["Rows"]][0]))
df_yearRows.set_value(0, 'Rows', int(df_yearRows.loc[0, ["Rows"]][0]) +2)
print("after increment",  int(df_yearRows.loc[0, ["Rows"]][0]))

print("before increment", int(df_yearRows.loc[2, ["Rows"]][0]))
df_yearRows.set_value(2, 'Rows', int(df_yearRows.loc[2, ["Rows"]][0]) +1)
print("after increment",  int(df_yearRows.loc[2, ["Rows"]][0]))


# In[30]:

df_actresses = pd.DataFrame(columns = ["Year","Actress","Film","Winner"])
start = 0
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    end = start + numFilms   
    for i in range(start, end): 
        isWinner = "No"
        actress = actresses[i]   
        film = films[i]        
        if actress in winners['actress'] and film in winners['film']:
            isWinner = "Yes"           
        df_actresses.loc[df_actresses.shape[0]] = [year,actress,film,isWinner]
    start = start + numFilms
# Print dataframe and look at the first 3 rows which have the same actress
df_actresses.loc[df_actresses["Winner"] == "Yes"]


# In[31]:

# Now check the year 1930 and see Greta Garbo received two nominations
df_actresses["Year"] = df_actresses["Year"].astype(int)
df_actresses.loc[(df_actresses["Year"] == 1930) & (df_actresses["Winner"] == "No")]


# In[32]:

# Now check the years 1950 and 1959 and see that multiple actress nominations for the same films
df_actresses.loc[(df_actresses["Year"].isin([1950, 1959])) & (df_actresses["Winner"] == "No")]


# In[33]:

# Page 5 - Best Supporting Actor
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor")
tables = data.findAll("table", class_= "wikitable sortable")


# In[34]:

# Here we extract each actor, film and year
films =[]
actors = []
years = []
winners = {'actor' : [], 'film' : [] }
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

# All years are in a four digit format so we dont need to do any formatting
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')     
    if(len(cells) > 1 and row.has_attr('rowspan')):
        year = cells[0].find(text=True)
        nrows = row['rowspan']
        df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
        years.append(int(year))
    
for row in tables[0].findAll("tr"):
    cells = row.findAll("td")    
    index = 0
    if(len(cells) > 1):  
        isWinner = False
        if(cells[0].has_attr("style")):  
            if(cells[0]["style"].startswith(winnerStyle)):
                isWinner = True
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actor = l.find(text=True).encode('utf-8').strip()
                    actors.append(actor)
                elif(index == 2): 
                    film = l.find(text=True).encode('utf-8').strip()
                    films.append(film)
                    if isWinner:
                        winners['actor'].append(actor)
                        winners['film'].append(film)
        index = index+1   


# In[35]:

# Check the length of the lists. Actors and films are not the same because in several years multiple actors were nominated for
# the same film
print(len(years))
print(len(actors))
print(len(films))


# In[36]:

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


# In[37]:

# Now they are the same length
print(len(years))
print(len(actors))
print(len(films))


# In[38]:

df_supActors = pd.DataFrame(columns = ["Year","Actor","Film","Winner"])
start = 0
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    end = start + numFilms   
    for i in range(start, end):  
        isWinner = "No"
        actor = actors[i]   
        film = films[i]
        if actor in winners['actor'] and film in winners['film']:
            isWinner = "Yes"           
        df_supActors.loc[df_supActors.shape[0]] = [year,actor,film,isWinner]
    start = start + numFilms
df_supActors.loc[df_supActors["Winner"] == "Yes"]


# In[39]:

# Now check each of the years that were inserted and see that each one has two or more occurrences of the same film
df_supActors["Year"] = df_supActors["Year"].astype(int)
years = [1953, 1954, 1957, 1959, 1961, 1972, 1974, 1986, 1991]
df_supActors.loc[(df_supActors["Year"].isin(years)) & (df_supActors["Winner"] == "No")]


# In[40]:

# Page 6 - Best Supporting Actress
data = loadPage("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress")
tables = data.findAll("table", class_= "wikitable sortable")


# In[41]:

# Here we extract each actress, film and year
films =[]
actresses = []
years = []
winners = {'actress' : [], 'film' : [] }
df_yearRows = pd.DataFrame(columns = ["Year","Rows"])

# All years are in a four digit format so we dont need to do any formatting
for row in tables[0].findAll("th", scope="row"):
    cells = row.findAll('a')  
    if(len(cells) > 1 and row.has_attr('rowspan')):
        year = cells[0].find(text=True)
        nrows = row['rowspan']
        df_yearRows.loc[df_yearRows.shape[0]] = [year,nrows]
        years.append(year)
    
for row in tables[0].findAll("tr"):
    cells = row.findAll("td")    
    index = 0
    if(len(cells) > 1):  
        isWinner = False
        if(cells[0].has_attr("style")):  
            if(cells[0]["style"].startswith(winnerStyle)):
                isWinner = True
    for c in cells:
        links = c.findAll("a")
        for l in links:
            if(l.has_attr('title')):
                if(index == 0): 
                    actress = l.find(text=True).encode('utf-8').strip()
                    actresses.append(actress)                    
                elif(index == 2): 
                    film = l.find(text=True).encode('utf-8').strip()
                    films.append(film)
                    if isWinner:
                        winners['actress'].append(actress)
                        winners['film'].append(film)
        index = index+1   


# In[42]:

# Check the length of the lists. Actresses and films are not the same because in several years multiple actresses were nominated 
# for the same film
print(len(years))
print(len(actresses))
print(len(films))


# In[43]:

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


# In[44]:

# Now they are the same length
print(len(years))
print(len(actresses))
print(len(films))


# In[45]:

df_supActresses = pd.DataFrame(columns = ["Year","Actress","Film","Winner"])
start = 0
for index, row in df_yearRows.iterrows():
    year = row["Year"]
    numFilms = pd.to_numeric(row["Rows"])
    end = start + numFilms   
    for i in range(start, end):  
        isWinner = "No"
        actress = actresses[i]   
        film = films[i]
        if actress in winners['actress'] and film in winners['film']:
            isWinner = "Yes"           
        df_supActresses.loc[df_supActresses.shape[0]] = [year,actress,film,isWinner]
    start = start + numFilms
df_supActresses.loc[df_supActresses["Winner"] == "Yes"]


# In[46]:

# Now check each of the years that were inserted and see that each one has two or more occurrences of the same film
df_supActresses["Year"] = df_supActresses["Year"].astype(int)
years = [1941, 1945, 1948, 1949, 1954, 1957, 1959, 1963, 1965, 1989, 2000, 2001, 2008]
df_supActresses.loc[(df_supActresses["Year"].isin(years)) & (df_supActresses["Winner"] == "No")]


# In[47]:

# Look at the number of rows in each data frame
print(df_picture.shape[0])
print(df_directors.shape[0])
print(df_actors.shape[0])
print(df_actresses.shape[0])
print(df_supActors.shape[0])
print(df_supActresses.shape[0])


# In[48]:

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


# In[49]:

# Insert the data from each data frame into tables. If the table already exists overwrite it
df_picture.to_sql('nominee_best_picture', con=engine, if_exists='replace', index_label='id')
df_directors.to_sql('nominee_best_director', con=engine, if_exists='replace', index_label='id')
df_actors.to_sql('nominee_best_actor', con=engine, if_exists='replace', index_label='id')
df_actresses.to_sql('nominee_best_actress', con=engine, if_exists='replace', index_label='id')
df_supActors.to_sql('nominee_best_supporting_actor', con=engine, if_exists='replace', index_label='id')
df_supActresses.to_sql('nominee_best_supporting_actress', con=engine, if_exists='replace', index_label='id')


# In[50]:

# Show that the tables havebeen created
res = engine.execute("SHOW TABLES")
for x in res:
    print x


# In[51]:

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


# In[52]:

# For displaying results in a table format
from prettytable import PrettyTable


# In[53]:

# Return a list of actors ordered by nominations and wins
actor_mostNom = engine.execute("SELECT actor, (COUNT(actor)) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_actor GROUP BY actor ORDER BY total_nom DESC, total_wins DESC, actor ASC")
table = PrettyTable(['Actor', 'Nominations', 'Wins'])
for x in actor_mostNom:
    table.add_row([x['actor'], x['total_nom'], x['total_wins']])
print(table)


# In[54]:

# Return a list of actresses ordered by nominations and wins
actress_mostNom = engine.execute("SELECT actress, COUNT(actress) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_actress GROUP BY actress ORDER BY total_nom DESC, total_wins DESC, actress ASC")
table = PrettyTable(['Actress', 'Nominations', 'Wins'])
for x in actress_mostNom:
    table.add_row([x['actress'], x['total_nom'], x['total_wins']])
print(table)


# In[55]:

# Return a list of directors ordered by nominations and wins
director_mostNom = engine.execute("SELECT director, COUNT(director) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_director GROUP BY director ORDER BY total_nom DESC, total_wins DESC, director ASC")
table = PrettyTable(['Director', 'Nominations', 'Wins'])
for x in director_mostNom:
    table.add_row([x['director'], x['total_nom'], x['total_wins']])
print(table)


# In[56]:

# Return a list of actors ordered by nominations and wins
supActor_mostNom = engine.execute("SELECT actor, (COUNT(actor)) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_supporting_actor GROUP BY actor ORDER BY total_nom DESC, total_wins DESC, actor ASC")
table = PrettyTable(['Actor', 'Nominations', 'Wins'])
for x in supActor_mostNom:
    table.add_row([x['actor'], x['total_nom'], x['total_wins']])
print(table)


# In[57]:

# Return a list of actresses ordered by nominations and wins
supActress_mostNom = engine.execute("SELECT actress, COUNT(actress) AS total_nom, COUNT(IF (winner = 'Yes', 1, null )) AS total_wins FROM nominee_best_supporting_actress GROUP BY actress ORDER BY total_nom DESC, total_wins DESC, actress ASC")
table = PrettyTable(['Actress', 'Nominations', 'Wins'])
for x in supActress_mostNom:
    table.add_row([x['actress'], x['total_nom'], x['total_wins']])
print(table)

