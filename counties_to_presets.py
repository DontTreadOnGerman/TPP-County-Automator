import pandas as pd
import numpy as np
import json
import os
import decimal


tpp_folder = str(os.getenv('APPDATA')).replace("Roaming", "Local")+r"\the_political_process\User Data\Default\saveFiles\advancedOptions"
pd.options.mode.chained_assignment = None
states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
          'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
slash = r"\."
print(f"Thanks for using the acctuallydavid.com TPP preset automator.\n"
      f"When you're typing in a path, use / instead of {slash}.\n"
      f"Files inside of the working directory can be referenced using just the file name+the file extension.")
print("Where's the path for your preset? (use .json)\nType 'N/A' for vanilla\nType 'TPPFolder' if the preset is in your TPP folder.")
preset_path = input()
if preset_path == "N/A":
    preset_path = "advop_template.json"
elif preset_path == "TPPFolder":
    print("What's the name of your preset? (use .json)")
    preset_path = rf"{tpp_folder}\{input()}"
print(preset_path)
print("Where's the path for your county data? (use .csv)")
county_data_path = input()
print("What do you want to name your newly generated preset? (add .json to the end)")
preset_name = input()
print(f"Where do you want your newly generated preset to go?\n"
      f"Don't add the preset file name to your input.\n"
      f"When you're typing in a path, use / instead of {slash}\n"
      f"Type 'N/A' if you want it automatically sent to your TPP preset folder")
preset_send_path = input()
if preset_send_path == "N/A":
    preset_send_path = tpp_folder
    preset_name = rf"\{preset_name}"
else:
    preset_name = f"/{preset_name}"
# read county data
county_data_frame = pd.read_csv(county_data_path)
# fix alaska boroughs - valdez-cordova is still unsplit in TPP
borough_pops = {2062: 4865, 2064: 2065}
dem_vals = []
gop_vals = []
indy_vals = []
try:
    for borough in list(borough_pops.keys()):
        borough_data = county_data_frame.loc[county_data_frame["FIPS"] == borough]
        gop_vals.append(borough_data["GOP %"].to_list()[0])
        dem_vals.append(borough_data["Dem %"].to_list()[0])
        indy_vals.append(borough_data["Indy %"].to_list()[0])
        county_data_frame = county_data_frame[county_data_frame["FIPS"] != borough]
except Exception:
    pass
else:
    dem_average = np.average(dem_vals, weights=list(borough_pops.values()))
    gop_average = np.average(gop_vals, weights=list(borough_pops.values()))
    indy_average = np.average(indy_vals, weights=list(borough_pops.values()))
    valdez_cordova = {"FIPS": 0, "County Name": "Valdez Cordova",
                      "TPP County Name": "Valdez Cordova Borough",
                      "Population": 4865+2065, "State": "Alaska",
                      "State code": "AK", "Dem %": dem_average,
                      "GOP %": gop_average, "Indy %": indy_average}
    county_data_frame = county_data_frame.to_dict(orient="records")
    county_data_frame.append(valdez_cordova)
    for county in county_data_frame:
        county["County Index"] = county["TPP County Name"] + (county["State code"].lower())
    county_data_frame = pd.DataFrame(county_data_frame)
# read preset file
with open(preset_path) as json_data:
    json_raw_data = json.load(json_data)
# parse preset file
for state in states:
    state_dem_pop = 0
    state_rep_pop = 0
    state_indy_pop = 0
    counties = []
    state_data = json_raw_data[f"{state.lower()}Stats"]["counties"]
    state_county_data = []
    for county in state_data:
        # demPop repPop indPop
        county_index = county["name"] + (state.lower())
        print(county["name"]+", "+state+" added to JSON preset")
        try:
            county_election_data = \
                county_data_frame.loc[county_data_frame["County Index"] == county_index].to_dict(orient="records")[0]
        except Exception:
            print(county_index+" errored. Either you don't have all counties or you should contact the dev")
            exit()
        total_sum = 0
        for party in ["Dem", "Rep", "Ind"]:
            party_data = np.round(county_election_data[party.replace("Rep", "GOP").replace("Ind", "Indy") + " %"], 3)
            county[f"{party.lower()}Pop"] = party_data
            total_sum += party_data
        new_sum = 0
        for party in ["Dem", "Rep", "Ind"]:
            county[f"{party.lower()}Pop"] = float(decimal.Decimal(county[f"{party.lower()}Pop"])/decimal.Decimal(total_sum))
            new_sum += county[f"{party.lower()}Pop"]
        state_dem_pop += county[f"demPop"]*county[f"pop"]
        state_indy_pop += county[f"indPop"]*county[f"pop"]
        state_rep_pop += county[f"repPop"]*county[f"pop"]
        counties.append(county)
    state_pop = state_dem_pop+state_rep_pop+state_indy_pop
    json_raw_data[f"{state.lower()}Stats"]["demPop"] = state_dem_pop/state_pop
    json_raw_data[f"{state.lower()}Stats"]["repPop"] = state_rep_pop/state_pop
    json_raw_data[f"{state.lower()}Stats"]["indPop"] = state_indy_pop/state_pop
    json_raw_data[f"{state.lower()}Stats"]["counties"][0] = counties[0]
# finished
with open(preset_send_path+preset_name, "w") as fp:
    json.dump(json_raw_data, fp)
print(f"JSON preset saved to {preset_send_path+preset_name}")
