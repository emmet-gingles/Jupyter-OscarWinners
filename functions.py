import urllib2;                     # For retrieving the contents of a page
from bs4 import BeautifulSoup;      # For parsing the contents of a page to HTML
import re  							# For regular expressions
import pandas as pd					# For creating dataframes
	
# Function that takes in a URL and returns the contents of the page as HTML
def loadPage(url):
    page = urllib2.urlopen(url)
    data = BeautifulSoup(page, "lxml")
    return data
	
	
# Function that takes in a table(s) as a parameter and outputs a dictionary with information relating to each film.
# The process of how it extracts the data from the tables differs depending on the pageType parameter.
# The third parameter winnersOnly is a boolean with a default value of True. If it is set to False then it returns it also returns a list of Oscar winners as part of the dictionary
def extractFilmData(pageType, tables, winnersOnly=True):
	# Winning style of table cells
	winnerStyle = 'background:#FAEB86'
	# List for storing films 
	films = []

	# Best Picture
	if pageType == "picture":
		# List for storing the producers of each film
		producers = []
		# List for Oscar winners
		winners = []	
		# Each decade is in a seperate table so 10 in total
		for i in range(10):	
			# If the winnersOnly parameter is True we only want the rows with winners data in them.
			# Else we want all rows
			if winnersOnly:
				search = tables[i].findAll("tr", style=re.compile('^'+winnerStyle))
			else:
				search = tables[i].findAll("tr")
			# Loop through the list of rows
			for row in search:
				# Variable to determine whether or not film is an Oscar winner. Default value is False
				isWinner = False
				# Only if winnersOnly is False AND the row has a style attribute
				if not winnersOnly and row.has_attr("style"):
				# Check that the starts with the winnerStyle ie. 'background:#FAEB86' or 'background:#FAEB86;'. 
				# If it is then it is an Oscar winner so set isWinner to True
					if row["style"].startswith(winnerStyle):
						isWinner = True
				# Get each cell within that row
				cells = row.findAll('td')				
				if len(cells) > 1:       
					# Get the text from within the first cell, encode it and add it to the films list
					film = cells[0].find(text=True).encode('utf-8').strip()
					films.append(film)
					# If winnersOnly is False and isWinner is True then add the film to the list of winners
					if not winnersOnly and isWinner:
						winners.append(film)
					# Get the text from within the second cell - text saved as an array  
					producer = cells[1].findAll(text=True)
					if len(producer) > 1:
						# If the last index is a line break then remove it from variable
						if producer[len(producer)-1] == '\n':
							producer = producer[:-1] 
					# If first item ends in a line break then remove it
					if producer[0].endswith("\n"):
						producer = producer[0][0:-1]
					# Join all the text to a single string and append it to the list of nominees
					producers.append("".join(producer).encode('utf-8').strip())  
					
		# Return lists of films and producers as a dictionary
		# If winnersOnly parameter is True then also return list of Oscar winners
		if winnersOnly:
			return {"films": films, "names": producers}
		else:
			return {"films": films, "names": producers, "winners": winners}

	# Best Director
	elif pageType == "director":
		# List for storing the director of each film
		directors = []		
		# If the winnersOnly parameter is False then create a dictionary for storing each winning director and film
		if not winnersOnly:
			winners = {'director': [], 'film': []}			
		# All data is in one table so return all rows 
		for row in tables[0].findAll("tr"):
			# If the winnersOnly parameter is True we only want the cells with winners data in them.
			# Otherwise we want all cells from within that row
			if winnersOnly:
				cells = row.findAll("td", style=re.compile('^'+winnerStyle))
			else:
				cells = row.findAll("td")			
			# Should find the director in first cell and the film in second cell so check there is enough
			if len(cells) > 1:
				# Variable to determine whether or not film is an Oscar winner. Default value is False
				isWinner = False
				# Only if winnersOnly is False AND the cell has a style attribute
				if not winnersOnly and cells[0].has_attr("style"):
					# Check that the cell starts with the winnerStyle ie. 'background:#FAEB86' or 'background:#FAEB86;'. 
					# If it is then it is an Oscar winner so set isWinner to True
					if cells[0]["style"].startswith(winnerStyle):
						isWinner = True							
				# Get all text from the first cell. We don't want the last part as this has "\n" characters
				director = cells[0].findAll(text=True)[:-1]
				# Join together array into a string and add to list of directors
				director = "".join(director).encode('utf-8').strip()
				directors.append(director)        
				# Get the text from within the second cell, encode it and add it to the list of nominees    
				film = cells[1].find(text=True).encode('utf-8').strip() 
				films.append(film) 
				# If winnersOnly is False AND isWinner is True then add the director film to the winners dictionary
				if not winnersOnly and isWinner:
					winners['director'].append(director)
					winners['film'].append(film)
			# In case a director has more than one film nominated, then the second film will be in a new cell 
			elif len(cells) == 1:
				# In this scenario the cell will have no rowspan or colspan
				if cells[0].has_attr("rowspan") == False and cells[0].has_attr("colspan") == False:
					film = cells[0].find(text=True).encode('utf-8').strip() 
					films.append(film) 
					
		# Return lists of films and directors as a dictionary
		# If winnersOnly parameter is True then also return the dictionary of Oscar winners				
		if winnersOnly:
			return {"films": films, "names": directors}
		else:
			return {"films": films, "names": directors, "winners": winners}
			
	
	# Any of Best Actor, Best Actress, Best Supporting Actor, Best Supporting Actress
	elif pageType in ["actor", "actress", "supporting actor", "supporting actress"]:
		# List for storing the actors/actresses for each film
		actors = []		
		# If the winnersOnly parameter is False then create a dictionary for storing each winning actor/actress and film
		if not winnersOnly:
			# Depending on the value of the pageType parameter create a dictionary for winners with either an actor or actress column
			if pageType in ["actor", "supporting actor"]:
				winners = {'actor': [], 'film': []}
			else:
				winners = {'actress': [], 'film': []}
				
		# All data is in one table so return all rows 	
		for row in tables[0].findAll("tr"):
			# If the winnersOnly parameter is True we only want the rows with winners data in them.
			# Otherwise we want all rows
			if winnersOnly:
				cells = row.findAll("td", style=re.compile('^'+winnerStyle))
			else:
				cells = row.findAll('td') 
			# Variable to store the current cell being searched
			index = 0
			if len(cells) > 1:  
				# Variable to determine whether or not film is an Oscar winner. Default value is False
				isWinner = False
				# Only if winnersOnly is False AND the row has a style attribute
				if not winnersOnly and cells[0].has_attr("style"):  
					# Check that the cell starts with the winnerStyle ie. 'background:#FAEB86' or 'background:#FAEB86;'. 
					# If it is then it is an Oscar winner so set isWinner to True
					if cells[0]["style"].startswith(winnerStyle):
						isWinner = True
			# Iterate through each cell
			for cell in cells:
				# Find all hyperlinks within the cell
				links = cell.findAll("a")
				# Iterate through each hyperlink
				for link in links:
					# We are only interested in links that include a title attribute
					if link.has_attr('title'):
						# First link contains the actor 
						if index == 0: 
							actor = link.find(text=True).encode('utf-8').strip()
							actors.append(actor)
						# Third link contains the film 
						elif index == 2: 
							film = link.find(text=True).encode('utf-8').strip()
							films.append(film)
							# If winnersOnly is False AND isWinner is True then add the film to the winners dictionary
							if not winnersOnly and isWinner:
								winners['film'].append(film)
								# Depending on the pageType add the actor to the appropriate column in the winners dictionary
								if pageType in ["actor", "supporting actor"]:
									winners['actor'].append(actor)
								else:
									winners['actress'].append(actor)								
				# Increment index after each cell
				index = index+1  
				
		# Return lists of films and actors as a dictionary
		# If winnersOnly parameter is True then also return the dictionary of Oscar winners		
		if winnersOnly:
			return {"films": films, "names": actors}
		else:
			return {"films": films, "names": actors, "winners": winners}
			
			
# Function that takes in a table(s) as a parameter and outputs a list of years
# The third parameter winnersOnly is a boolean with a default value of True. If it is set to False then it returns it instead returns a dictionary containing each year 
# and the number of films nominated for that year ie. the rowcount
def extractYears(pageType, tables, winnersOnly=True):
	# List to store the years
	years = []
	# List to store the rowcount for each year 
	list_nrows = []

	# Best Picture
	if pageType == "picture":
		# Each decade is in a seperate table so 10 in total
		for i in range(10):
			for cell in tables[i].findAll("td", style="text-align:center"):
				# Get each link within that cell
				links = cell.findAll('a')
				# If year is all in one link and in a format like 1927/28 then we want the first two and last two charaters so that 
				# it will be 1928
				if len(links[0].find(text=True)) == 7:
					year = links[0].find(text=True)[0:2] + links[0].find(text=True)[5:7]
				# If year is in two links and the second link has four numbers ie. 1927/1928 then we want the second link
				elif len(links[1].find(text=True)) == 4 and links[1].find(text=True).isnumeric():       
					year = links[1].find(text=True)
				# If the year is in two links and the second link has two numbers ie. 1927/28 then we want the first two characters 
				# of the first link and the last two of the second link
				elif len(links[1].find(text=True)) == 2 and links[1].find(text=True).isnumeric():
					year = links[0].find(text=True)[0:2] + links[1].find(text=True)
				# Else the year is in a standard format ie. 1928 so get four characters
				else:
					year = links[0].find(text=True)[0:4]
				# Add year to list of years
				years.append(int(year))
				if not winnersOnly and cell.has_attr('rowspan'):	
					# Add year and nrows to dataframe
					list_nrows.append(cell["rowspan"])
			
	# Best Director, Best Actor or Best Actress
	elif pageType in ["director", "actor", "actress"]:
		# All data is in one table so find all the row which match 
		for row in tables[0].findAll("th", scope="row"):
			# Get each link within that cell
			links = row.findAll('a')
			# If year is all in one link and in a format like 1927/28 then we want the first two and last two charaters so that 
			# it will be 1928
			if len(links[0].find(text=True)) == 7:
				year = links[0].find(text=True)[0:2] + links[0].find(text=True)[5:7]
			# If year is in two links and the second link has four numbers ie. 1927/1928 then we want the second link
			elif len(links[1].find(text=True)) == 4 and links[1].find(text=True).isnumeric():       
				year = links[1].find(text=True)
			# If the year is in two links and the second link has two numbers ie. 1927/28 then we want the first two characters 
			# of the first link and the last two of the second link
			elif len(links[1].find(text=True)) == 2 and links[1].find(text=True).isnumeric():
				year = links[0].find(text=True)[0:2] + links[1].find(text=True)
			# Else the year is in a standard format ie. 1928 so get four characters
			else:
				year = links[0].find(text=True)[0:4]
			# Add year to list of years
			years.append(int(year))
			# If winnersOnly is False and row has a rowspan attribute then add the rowspan value to the list of rowcounts
			if not winnersOnly and row.has_attr('rowspan'):	
				list_nrows.append(row['rowspan'])
				
	# Best Supporting Actor or Best Supporting Actress
	else:
		# All data is in one table so find the rows which match
		for row in tables[0].findAll("th", scope="row"):
			# Get each link within that cell 
			links = row.findAll('a')   
			if len(links) > 1:
				# All years are in the standard four digit format so add it to the list 
				year = links[0].find(text=True)
				years.append(int(year))
				# If winnersOnly is False and row has a rowspan attribute then add the rowspan value to the list of rowcounts
				if not winnersOnly and row.has_attr('rowspan'):	
					list_nrows.append(row['rowspan'])
					
	# If winnersOnly is True then return the list of years.
	# Otherwise return a dictionary containing the list of years and the list of rowcounts
	if winnersOnly:		
		return years
	else:
		return { "years": years, "numFilms": list_nrows }
		
				
# Function for creating a dataframe using input parameters - data_type (type estring), data, numFilmsByYear, winners (all type dictionary)			
def createDataFrame(data_type, data, numFilmsByYear, winners):	
	# Depending on the data_type parameter, a dataframe is created with different columns.
	# Lists are created using the columns of the data parameter
	if data_type == "picture":
		df_frame = pd.DataFrame(columns = ["Year","Film","Producers","Winner"])
		films = data["films"]
		producers = data["producers"]
	elif data_type == "director":
		df_frame = pd.DataFrame(columns = ["Year","Director","Film","Winner"])
		films = data["films"]
		directors = data["directors"]
	elif data_type in ["actor", "supporting actor"]:
		df_frame = pd.DataFrame(columns = ["Year","Actor","Film","Winner"])
		films = data["films"]
		actors = data["actors"]
	elif data_type in ["actress", "supporting actress"]:
		df_frame = pd.DataFrame(columns = ["Year","Actress","Film","Winner"])
		films = data["films"]
		actresses = data["actresses"]
	
	# Variable to track the current list index while looping through lists
	start = 0

	# Loop through each year stored in the dictionary
	for i in range(len(numFilmsByYear['years'])):
		# Get the year at the current index 
		year = numFilmsByYear['years'][i]
		# Get the number of films nominated for that year
		numFilms = int(numFilmsByYear['numFilms'][i])
		# A variable end is calculated by adding start anf numFilms together.
		end = start + numFilms
		# If data_type is "picture", then subtract 1 from it 
		if data_type == "picture":
			 end = end - 1
		# Loop through each number from start to end 
		for j in range(start, end):
			# We use a try/except here in case goes out of bounds
			try:
				# Variable to determine whether or not film is an Oscar winner - default value is "No"
				isWinner = "No"
				
				# Best Picture
				if data_type == "picture":
					# Variables to store the film and producer for the current index
					film = films[j]
					producer = producers[j]
					# If the film is in the list of winners then set variable to "Yes"
					if film in winners:
						isWinner = "Yes" 
						# We then want to find the key that stores that film so we can delete it. 
						# This is necessary in case of remakes of previous winners eg. "Mutiny on the Bounty". 
						# Break out of loop once deleted
						for key, value in enumerate(winners):
							if value == film:
								del winners[key]
								break
					# Append all variable to data frame
					df_frame.loc[df_frame.shape[0]] = [year, film, producer, isWinner]
					
				# Best Director
				elif data_type == "director":
					# Variables to store the film and director for the current index
					film = films[j]
					director = directors[j]
					# Check that both the director and film are in the list of winners.
					# If they are then change the value of isWinner to "Yes"
					if director in winners['director'] and film in winners['film']:
						isWinner = "Yes" 
						# We then want to find the key that stores that film so we can delete it. 
						# This is necessary in case of a previous winner being nominated for a later film
						for key, value in enumerate(winners['director']):
							if value == director:
								del winners['director'][key]
								del winners['film'][key]
								break
					# Append all variable to data frame
					df_frame.loc[df_frame.shape[0]] = [year, director, film, isWinner]
					
				# Best Actor/ Supporting Actor
				elif data_type in ["actor", "supporting actor"]:	
					# Variables to store the film and actor for the current index
					film = films[j]
					actor = actors[j]
					# Check that both the actor and film are in the list of winners.
					# If they are then change the value of isWinner to "Yes"
					if actor in winners['actor'] and film in winners['film']:
						isWinner = "Yes" 
						# We then want to find the key that stores that film so we can delete it. 
						# This is necessary in case of a previous winner being nominated for a later film
						# Break out of loop once deleted
						for key, value in enumerate(winners['actor']):
							if value == actor:
								del winners['actor'][key]
								del winners['film'][key]
								break
					# Append all variable to data frame
					df_frame.loc[df_frame.shape[0]] = [year, actor, film, isWinner]
					
				# Best Actress/Supporting Actress
				elif data_type in ["actress", "supporting actress"]:	
					# Variables to store the film and actress for the current index
					film = films[j]
					actress = actresses[j]
					# Check that both the actress and film are in the list of winners.
					# If they are then change the value of isWinner to "Yes"
					if actress in winners['actress'] and film in winners['film']:
						isWinner = "Yes" 
						# We then want to find the key that stores that film so we can delete it. 
						# This is necessary in case of a previous winner being nominated for a later film 
						# Break out of loop once deleted
						for key, value in enumerate(winners['actress']):
							if value == actress:
								del winners['actress'][key]
								del winners['film'][key]
								break
					# # Append all variable to data frame
					df_frame.loc[df_frame.shape[0]] = [year, actress, film, isWinner]
			# In case of an index out of bounds exception, break out of loop
			except IndexError:
				break
		# Increment start by numFilms. If data_type is "picture" then subtract 1 from it 	
		start = start + numFilms 
		if data_type == "picture":
			start = start - 1 
			
	# Now with all the data in the dataframe, convert the year column to an integer
	df_frame["Year"] = df_frame["Year"].astype(int)
	# Return the dataframe
	return df_frame
		