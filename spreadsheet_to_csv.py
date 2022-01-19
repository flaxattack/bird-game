# create a new sheet in the test spreadsheet
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import json, itertools, time
import pandas as pd


SERVICE_ACCOUNT_FILE = 'servicekey.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a spreadsheet
spreadsheet_id = 'spreadsheet_id'

# Call the Sheets API
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.get(spreadsheetId=spreadsheet_id).execute()

# make a list of the individual sheet titles
titles = []
for item in result['sheets']:	
	for key, value in item.items():
		sheet_title = f"{value['title']}"
		title = sheet_title.replace('/', '_').replace(':', '')
		titles.append(sheet_title)


def sheet_to_df(title_list_index):
	all_dfs = []
	for title in title_list_index:
		request = sheet.values().get(spreadsheetId=spreadsheet_id, range=title)
		response = request.execute()

		data = response.get('values')
		names = [d.title() for d in data[0]]
		sheet_titles = [title for i in range(0, len(names[1:]))]
		sheet_titles.insert(0, '')
		columns = [sheet_titles, names]

		# generate a win/loss/draw count
		totals = [d for d in data[-1]]
		sums = [int(t) for t in totals[1:]]
		win = ['Win']
		draw = ['Draw']
		loss = ['Loss']
		for s in sums:
			if s == np.max(sums):
				win.append(1)
				loss.append(0)
				draw.append(0)
			if s < np.max(sums):
				win.append(0)
				loss.append(1)
				draw.append(0)
		if sum(win[1:]) > 1:
			for i,v in enumerate(win):
				if v == 1:
					draw[i] = 1
					win[i] = 0

		data.append(win)
		data.append(loss)
		data.append(draw)

		df = pd.DataFrame(data[1:], columns=columns)
		df[''] = df[''].str.capitalize()
		df.set_index('', inplace=True)
		df.columns.names = ['Game','Players']

		all_dfs.append(df)

		# this loop requires a delay so as not to exceed the Sheets API per-minute request quota
		time.sleep(1.0)
	
	# concatenate the list of dataframes
	all_values = pd.concat(all_dfs, axis=1)
	all_values = all_values.apply(pd.to_numeric)
	return all_values

# sheets 1-29 (index 28) are pre-Oceania; sheets 29+ are oceania
# save the dataframe to a csv file
sheet_to_df(titles[:28]).to_csv('original.csv')
sheet_to_df(titles[29:].to_csv('oceania.csv')
