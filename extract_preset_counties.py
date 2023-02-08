import pandas as pd
import numpy as np
import json
import os
import decimal

tpp_folder = str(os.getenv('APPDATA')).replace("Roaming",
                                               "Local") + r"\the_political_process\User Data\Default\saveFiles\advancedOptions"
pd.options.mode.chained_assignment = None
states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
          'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
slash = r"\."
print(f"Thanks for using the acctuallydavid.com TPP preset county data extractor.\n"
      f"When you're typing in a path, use / instead of {slash}.\n"
      f"Files inside of the working directory can be referenced using just the file name+the file extension.")
print(
    "Where's the path for your preset? (use .json)\nType 'N/A' for vanilla\nType 'TPPFolder' if the preset is in your TPP folder.")
preset_path = input()
if preset_path == "N/A":
    preset_path = "advop_template.json"
elif preset_path == "TPPFolder":
    print("What's the name of your preset? (use .json)")
    preset_path = rf"{tpp_folder}\{input()}"
print("What do you want to name the preset county data file and where should it go? (use .csv)")
preset_datafile = input()
# read preset file
with open(preset_path) as json_data:
    json_raw_data = json.load(json_data)
# parse preset file
counties = []
for state in states:
    state_data = json_raw_data[f"{state.lower()}Stats"]["counties"]
    state_county_data = []
    for county in state_data:
        # demPop repPop indPop
        county_index = county["name"] + (state.lower())
        print(county["name"] + ", " + state + " added to CSV datafile")
        counties.append({"TPP County Name": county["name"],
                         "State": state, "Dem %":
                             county[f"demPop"], "GOP %":
                             county[f"repPop"], "Indy %":
                             county[f"indPop"]})
# finished
county_data = pd.DataFrame(counties)
county_data = county_data.set_index("TPP County Name")
county_data.to_csv(preset_datafile)
print(f"County data saved to {preset_datafile}")
