import Scraper
import matplotlib.pyplot as plt
import json
import argparse


# gets jam data and stores it as
def get_jam_data(jam_name):
    # scrape itch to get the data
    entries = Scraper.scrape_jam(jam_name)

    # convert the entries to json
    entries_json = []
    for entry in entries:
        dictionary = {
            "index": entry.index,
            "score": entry.score,
            "raw_score": entry.raw_score,
            "ratings": entry.ratings
        }
        entries_json.append(dictionary)

    # save the jam data as a json file
    json_string = json.dumps(
        {
            "jam_name": jam_name,
            "entries": entries_json
        }, indent=4
    )

    with open("data/"+jam_name+".json", "w") as file:
        file.write(json_string)


# get all of the jams
jams = []
series = [
]

# get the series
for jam in series:
    start_index = jam["start-index"]
    last_index = jam["last-index"]
    for i in range(start_index, last_index):
        jams.append(jam["name"]+str(i))

# read the text file
with open("jams-to-get.txt", "r") as file:
    for line in file:
        string = line[:-1]
        jams.append(string)


# get a lot of data
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
for jam in jams:
    try:
        get_jam_data(jam)
    except:
        print("Failed to scrape " + jam)
    else:
        print("Successfully scraped " + jam)
