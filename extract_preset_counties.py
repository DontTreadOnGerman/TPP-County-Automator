import pandas as pd
import json
import os

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
# get county skeleton
county_skeletons = {}
county_data_frame = pd.read_csv("base_county_csv.csv").to_dict(orient="records")
for county in county_data_frame:
    county_index = county["TPP County Name"] + (county["State code"].lower())
    county_skeletons[county_index] = county
# parse preset file
counties = []
for state in states:
    state_data = json_raw_data[f"{state.lower()}Stats"]["counties"]
    state_county_data = []
    for county in state_data:
        # demPop repPop indPop
        county_index = county["name"] + (state.lower())
        county_data = county_skeletons[county_index]
        print(county["name"] + ", " + state + " added to CSV datafile")
        for party in ["Dem", "Rep", "Ind"]:
            county_data[f"{party.replace('Rep', 'GOP').replace('Ind', 'Indy')} %"] = county[f"{party.lower()}Pop"]
        counties.append(county_data)
# finished
county_data = pd.DataFrame(counties)
cordova_data = county_data.loc[county_data["TPP County Name"] == "Valdez Cordova Borough"].to_dict(orient="records")[0]
boroughs = {2062: "Chugach", 2064: "Copper River"}
c_dataset = cordova_data.copy()
c_dataset["County Name"] = "Chugach"
c_dataset["FIPS"] = 2062
counties.append(c_dataset)
county_data = pd.DataFrame(counties)
county_data = county_data.set_index("FIPS")
county_data = county_data.sort_values(by=['State code', 'FIPS'], ascending=[True, True])
county_data.to_csv(preset_datafile)
print(f"County data saved to {preset_datafile}")
