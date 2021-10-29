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

titles = []
#print(result['sheets'])
for item in result['sheets']:	# access the list associated with "sheets"
	for key, value in item.items():	# access the dictionary inside the list
		# print(f"{value['title']}")
		sheet_title = f"{value['title']}"	# find value for key 'title' in list of dictionaries
		title = sheet_title.replace('/', '_').replace(':', '')
		titles.append(sheet_title)

# sheets 1-28 (index 27) are the original bird game
# sheets 25+ are oceania
indexed_dfs = []
for title in titles[]:
	request = sheet.values().get(spreadsheetId=spreadsheet_id, range=title)
	response = request.execute()
	data = response.get('values')
	names = [d.title() for d in data[0]]
		# creates a (capitalized) list of names that is the first item in the list "data"
	df = pd.DataFrame(data[1:], columns=names)
		# 'data' is an array of values representing rows in the sheet
		# data[0] is the first item in the array, i.e. the columns (['', 'name1', 'name2'])
		# set the dataframe to the data array excluding the first item
		# the first item is set to 'columns'
	df[''] = df[''].str.capitalize()
		# capitalizes the index names
	indexed = df.set_index('')
		# sets the index of the dataframe to the first actual column ('birds', 'bonus cards', etc)
	indexed_dfs.append(indexed)
		# appends the reindexed dataframe to a list
	

all_values = pd.concat(indexed_dfs, axis=1)
#print(all_values)
all_values = all_values.apply(pd.to_numeric)
#print(all_values)
#print(all_values.groupby(axis=1, level=0).mean())
#all_values.to_csv('oceania_bird_scores2a.csv')
