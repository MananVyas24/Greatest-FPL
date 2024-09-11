import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import warnings
from .config import LEAGUE_IDS, LEAGUE_NAMES

class FPLScoring:
    def __init__(self, spreadsheet_id, sheet_name, credentials_file):
        self.SPREADSHEET_ID = spreadsheet_id
        self.SHEET_NAME = sheet_name
        self.CREDENTIALS_FILE = credentials_file
        
        warnings.filterwarnings("ignore")
        
        self._setup_google_sheets()

    def _setup_google_sheets(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE, scope)
        client = gspread.authorize(credentials)

        self.spreadsheet = client.open_by_key(self.SPREADSHEET_ID)
        self.worksheet = self.spreadsheet.worksheet(self.SHEET_NAME)
        
        print("Connected to the Sheet")

    def live_scoring(self):
        team_points_all = []
        df_overall_players = pd.DataFrame(columns=['Manager Name', 'GW Points'])

        for league_id in LEAGUE_IDS:
            url = f"https://www2.livefpl.net/leagues/{league_id}"
            df_iterations = pd.DataFrame(columns=['Manager Name', 'Total Points'])

            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find("table", {"id": "livetable"})

                for row in table.find_all("tr")[1:]:
                    cells = row.find_all("td")
                    if cells:
                        manager_name = cells[3].text.strip()
                        gw_points = int(cells[7].text.strip())
                        hits = int(cells[8].text.strip().split("\n")[0])
                        gw_points_updated = gw_points + hits

                        df_iterations.loc[len(df_iterations)] = [manager_name, gw_points_updated]
                        df_overall_players.loc[len(df_overall_players)] = [manager_name, gw_points_updated]

            else:
                print(f"Failed to fetch the webpage for league {league_id}.")

            team_points_all.append(df_iterations['Total Points'].sum())

        print(f"Data collected at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return df_overall_players, team_points_all

    def update_sheet(self, df):
        values = [df.columns.tolist()] + df.values.tolist()
        self.worksheet.update('A1', values)
        print(f"Sheet updated at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def run(self, update_interval=3):
        while True:
            df, team_points = self.live_scoring()
            if min(team_points) > 0:
                self.update_sheet(df)
            time.sleep(update_interval)