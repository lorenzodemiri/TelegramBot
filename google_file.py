import pprint

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class googleSheets:

    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('Mubbylab_order.json', self.scope)
        self.client = gspread.authorize(self.credentials)
        self.worksheet = self.client.open('Telegram_orders').sheet1
        self.data = self.worksheet.get_all_values()
        pp = pprint.PrettyPrinter()
        self.newRow = self.next_available_row(self.worksheet)
        print(self.newRow)

    def next_available_row(self, worksheet, cols_to_sample=2):
        # looks for empty row based on values appearing in 1st N columns
        cols = worksheet.range(1, 1, worksheet.row_count, cols_to_sample)
        return max([cell.row for cell in cols if cell.value]) + 1


    def insert_Order(self, row):
        self.worksheet.insert_row(row, self.newRow)
