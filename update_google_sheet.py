#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from datetime import timezone

from store.service import Service

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1x9lxJ98q8EO6bXQgrvW5oKLtKDIniDXmuNtjhlDoeQc'
SHEET_ID = '0'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    range_ = "'Search Results'"

    clear_values_request_body = {
        # TODO: Add desired entries to the request body.
    }

    request = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=range_, body=clear_values_request_body)
    response = request.execute()

    store_service = Service()
    result_dicts = store_service.get_search_results()

    pprint(result_dicts)

    fields = [
        'first_crawl_at',
        'last_seen_at',
        'url',
        'address',
        'neighborhood',
        'city',
        'price',
        'sqft',
        'bedrooms',
        'pet_friendly',
        'furnished'
    ]

    rows = list()
    rows.append(fields)

    for d in result_dicts:
        for k in ['first_crawl_at', 'last_seen_at']:
            d[k] = d[k].replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")     

        row = [d[k] for k in fields]
        rows.append(row)

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {

        'majorDimension': 'ROWS',
        'values': rows
    }

    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

if __name__ == '__main__':
    main()
    