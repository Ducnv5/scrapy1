from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import logging
import os

log = logging.getLogger('googlesheet')

# Setup the Sheets API
class GoogleSheetFunc:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    clientsecret = 'client_secret_ducnv.json'
    
    def __init__(self):
        self.store = file.Storage('credentials.json')
        self.creds = self.store.get()
        
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(self.clientsecret, self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
        self.service = build('sheets', 'v4', http=self.creds.authorize(Http()), cache_discovery=False)
        self.numCols = 0
        self.numRows = 0
        
    def resetAPI(self):
        self.store = file.Storage(self.clientsecret)
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(self.clientsecret, self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
        self.service = build('sheets', 'v4', http=self.creds.authorize(Http()), cache_discovery=False)
        
    def checkSheetStatus(self, SPREADSHEET_ID, RANGE_NAME, majorDimension="ROWS"):  
        ### Check service
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                     range=RANGE_NAME,majorDimension="ROWS").execute()
            arr = result.get('values',[])
            self.numRows = len(arr)   
            
            result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                     range=RANGE_NAME, majorDimension="COLUMNS").execute()
            arr = result.get('values',[])
            self.numCols = len(arr)
            if (self.numCols > 0 and self.numRows > 0) :
                log.info("Get success Rows and Columns: " + str(self.numRows) + "x" + str(self.numCols))
                return 1
            else:
                log.error("Can't get Column and Rows of " + SPREADSHEET_ID)
                return -1
        except Exception as ex:
            log.error(str(ex))
            return -1
            

    # Call the Sheets API
    def read_from_sheet(self, SPREADSHEET_ID, RANGE_NAME):
        result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            log.error('No data found. NONE VALUE')
            return []
        else:
            return values
    def write_to_sheet(self,  SPREADSHEET_ID, RANGE_NAME, WRITE_VALUE, majorDimension="ROWS"):
        body = {
                    'values': WRITE_VALUE,
                    "majorDimension": majorDimension
                }
        value_input_option = "USER_ENTERED"        
        result = self.service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                    valueInputOption=value_input_option, body=body).execute()
                    
        log.info('{0} cells updated.'.format(result.get('updatedCells')));
                    