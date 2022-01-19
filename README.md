# Wingspan Data Analysis

https://stonemaiergames.com/games/wingspan/

- Wingspan is a competitive, medium-weight, card-driven, engine-building board game
- Each player's overall score is composed of the following:
    - Points for each face-up bird played on the player mat
    - Points for each bonus card
    - Points for end-of-round goals
    - 1 point for each: egg laid on a bird card, food token cached on a bird card, and card tucked under a bird card
- The Oceania expansion, which changed gameplay significantly, was released in December 2020; I thus divided my analysis into "pre-Oceania" and "post-Oceania"
- Scores were initially manually entered into a Google spreadsheet, with each sheet corresponding to an individual gameplay session
    - I later created an iOS Shortcut that gathers score information and enters it into a new sheet
- I created a GCP project to make requests to the Google Sheets API, as outlined here: https://developers.google.com/sheets/api/quickstart/python/
    - The number of sheets in the spreadsheet caused me to exceed my per-minute Sheets API quota, so I ended up downloading scores as 2 csv files (corresponding to the pre-and post-Oceania scores)
