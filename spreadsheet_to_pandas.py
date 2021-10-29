# create a new sheet in the test spreadsheet
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import json
import pandas as pd


SERVICE_ACCOUNT_FILE = 'servicekey.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
spreadsheet_id = 'spreadsheet_id'

# Call the Sheets API
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.get(spreadsheetId=spreadsheet_id).execute()

# make a list of all the sheet names in the spreadsheet
# this will allow you to get the data from each sheet
titles = []
for item in result['sheets']:	
	for key, value in item.items():
		sheet_title = f"{value['title']}"
		title = sheet_title.replace('/', '_').replace(':', '')
		titles.append(sheet_title)

# sheets 1-28 (index 27) are the original bird game
# sheets 25+ are oceania
indexed_dfs = []
for title in titles[]:
	request = sheet.values().get(spreadsheetId=spreadsheet_id, range=title)
	response = request.execute()
	data = response.get('values')
	
	# create a (capitalized) list of names that is the first item in the list "data"
	names = [d.title() for d in data[0]]
	
	# 'data' is an array of values representing rows in the sheet
	# data[0] is the first item in the array, i.e. the columns (['', 'name1', 'name2'])
	# set the dataframe to the data array (excluding the first item)
	# the first item is set to 'columns'
	df = pd.DataFrame(data[1:], columns=names)

	# capitalize the index names
	df[''] = df[''].str.capitalize()
		
	# sets the index of the dataframe to the first actual column ('birds', 'bonus cards', etc)
	df.set_index('', inplace=True)	
	indexed_dfs.append(df)

# concatenate into a single dataframe 	
all_values = pd.concat(indexed_dfs, axis=1)

# convert values to numeric from string
all_values = all_values.apply(pd.to_numeric)

# save the new dataframe to a csv file
#all_values.to_csv('oceania_bird_scores2a.csv')
