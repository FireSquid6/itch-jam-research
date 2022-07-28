from numpy import number
import requests
import re
from bs4 import BeautifulSoup


# scrapes a jam and returns an array of entries
def scrape_jam(jam_name):
    # setup variables
    entries = []

    # get the URL of the results
    url_prefix = "https://itch.io/jam/"+jam_name+"/results?page="
    page = 1
    index = 0

    # iterate through each page of the results
    while page < 1000:  # It's assumed that no jam will have more than 1000 pages
        # get the html
        request = requests.get(url_prefix + str(page))

        # if the website doesn't exist, break the loop
        if request.status_code != 200:
            break

        # get the website data
        soup = BeautifulSoup(request.content, "html.parser")

        # iterate through each game rank class
        for data in soup.find_all("div", class_="game_rank"):
            # find the results table
            numbers_found = []
            results_table = data.find("table", class_="ranking_results_table")

            # iterate through the table rows
            for tr in results_table.find_all("tr"):
                if "Overall" in tr.text:
                    # if overall is found inside the table, iterate through the table data
                    for td in tr.find_all("td"):
                        # if a period is found, it must be a number, therefore append it to an array
                        if "." in td.text:
                            numbers_found.append(td.text)

            # set score and raw score
            # score will always come first, and raw score second
            score = float(numbers_found[0])
            raw_score = float(numbers_found[1])

            # find the game summary
            game_summary = data.find("div", class_="game_summary")
            for h3 in game_summary.find_all("h3"):
                # if the h3 has the word "ratings" in it, it must be the correct one
                if "ratings" in h3.text:
                    # get all of the numbers out of the text
                    text = str(h3.text)
                    numbers = re.findall(r'\d+', text)

                    # the ratings will always be the second number found
                    ratings = float(numbers[1])

                    # break out of the loop
                    break

            # add the entry to the list
            index += 1
            entry = Entry(index, score, raw_score, ratings)
            entries.append(entry)

        # add to page
        page += 1

    # return the entries
    return entries


# class to use for each entry
class Entry:
    index = 0
    score = 0
    raw_score = 0
    ratings = 0

    def __init__(self, index, score, raw_score, ratings):
        self.index = index
        self.score = score
        self.raw_score = raw_score
        self.ratings = ratings
