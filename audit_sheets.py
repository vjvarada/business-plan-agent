import gspread
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('token.json')
client = gspread.authorize(creds)
ss = client.open_by_key('1sLuti-TDhI7Hi1YRmF6WDfn7ZsNDMm6-C-Dr4viMiLU')

# Read all sheets
sheets = ['Assumptions', 'Revenue', 'Operating Costs', 'P&L', 'Balance Sheet', 'Cash Flow']

for sheet_name in sheets:
    print(f'\n=== {sheet_name} ===')
    sheet = ss.worksheet(sheet_name)
    data = sheet.get_all_values()
    for row in data[:15]:  # First 15 rows
        print(row)
