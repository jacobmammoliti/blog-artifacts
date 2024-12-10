# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import psycopg2
import os
import sys
import gspread
import google.auth

class GoogleSheetsPipeline:
    def __init__(self):
        try:
            spreadsheet_name = os.environ['SPREADSHEET_NAME']
            worksheet_name = os.environ['WORKSHEET_NAME']
        except KeyError as e:
            sys.exit(f"Required environment variable {e} not set.")

        credentials, project_id = google.auth.default(
            scopes=[
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
        )

        gc = gspread.authorize(credentials)

        spreadsheet = gc.open(spreadsheet_name)
        self.worksheet = spreadsheet.worksheet(worksheet_name)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        body = [item["title"],
                item["price"],
                item["rating"]]

        self.worksheet.append_row(body, table_range="A1:C1")


# class PostgresPipeline:
#     def __init__(self):
#         hostname = os.getenv('PSQL_HOSTNAME', 'localhost')
#         username = os.getenv('PSQL_USERNAME', 'postgres')
#         password = os.getenv('PSQL_PASSWORD', 'postgres')
#         database = os.getenv('PSQL_DATABASE', 'postgres')

#         self.connection = psycopg2.connect(
#             host=hostname,
#             user=username,
#             password=password,
#             dbname=database
#         )

#         self.cursor = self.connection.cursor()

#         self.cursor.execute("""
#         CREATE TABLE IF NOT EXISTS books(
#             id serial PRIMARY KEY,
#             title VARCHAR(255),
#             price VARCHAR(255),
#             rating VARCHAR(255))
#         """)
    
#     def process_item(self, item, spider):
#         self.cursor.execute("""
#         INSERT INTO books (title, price, rating) values (%s, %s, %s)""", (
#             item["title"],
#             item["price"],
#             item["rating"]
#         ))

#         self.connection.commit()

#         return item
    
#     def close_spider(self, spider):
#         self.cursor.close()
#         self.connection.close()