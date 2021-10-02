import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt


# from utils.config import GS_CLIENT_SECRET, GS_CLIENT_ID, GMAIL

# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials(client_id=GS_CLIENT_ID, 
#                                     service_account_email=GMAIL, 
#                                     signer=crypt, scopes=scope)
# client = gspread.authorize(creds)