from fpl_scoring import FPLScoring

# Replace these with your actual values
SPREADSHEET_ID = '1socCB2cPuu8NU-P4ZqeOvClkQUw5e_6o53um7Ckqvug'
SHEET_NAME = 'RawScores'
CREDENTIALS_FILE = 'fpl-scoring-395719-a1fb260f15d1.json'

def main():
    fpl_scorer = FPLScoring(SPREADSHEET_ID, SHEET_NAME, CREDENTIALS_FILE)
    fpl_scorer.run()

if __name__ == "__main__":
    main()