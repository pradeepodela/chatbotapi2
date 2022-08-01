# Import required modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("mypy-19226-54185204634e.json", scope)
client = gspread.authorize(creds)
print('Connected to Google Sheets')
sheet = client.open("Untitled spreadsheet").sheet1



# # display data
data = sheet.get_all_records()


# # Inserting data
def insert_data(data):
    sheet.insert_row(data)
    print('Data inserted')
    return 'Data inserted'

