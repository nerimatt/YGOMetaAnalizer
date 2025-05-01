import requests
import json

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import pandas as pd

WEBSITE_CORE_LINK = "https://ygoprodeck.com/"
FORMAT = "TCG"
TIER = "3"

TOURNAMENTS_FOLDER = f"raw/tournaments-{FORMAT}-{TIER}/"

def generate_tournament_names_data():
    YCS_TCG_ENDPOINT = f"https://ygoprodeck.com/api/tournament/getTournaments.php?&tier={TIER}&format={FORMAT}"
    # https://ygoprodeck.com/api/tournament/getTournaments.php?&tier=3&format=TCG

    res = requests.get(YCS_TCG_ENDPOINT)
    data = res.json()["data"]
    print(type(data))

    df = pd.DataFrame(data = data)
    print(df)
    df.to_csv(f"data/tournaments-{FORMAT}-{TIER}.csv")

    # with open(f"data/tournaments-{FORMAT}-{TIER}.json", "w") as jsonfile:
    #     json.dump(data, jsonfile, indent = 4)


def download_all_tournament_pages():
    tournaments_df = pd.read_csv("./raw/tournaments-TCG-3.csv")

    for tournament in tournaments_df["slug"]:
        get_tournament_page_html(tournament)



def get_tournament_page_html(slug):

    TOURNAMENT_ENDPOINT = "https://ygoprodeck.com/tournament/"
    webpage = TOURNAMENT_ENDPOINT + slug
    print(f"downloading html: {webpage}")

    session = HTMLSession()
    response = session.get(webpage)

    response.html.render(sleep = 3, keep_page = True, scrolldown = 1)

    with open(f"raw/tournaments-{FORMAT}-{TIER}/{slug}.html", "w") as htmlfile:
        htmlfile.write(response.html.html)


    session.close()


def get_tournament_data_from_html(slug):
    TOURNAMENT_ENDPOINT = "https://ygoprodeck.com/tournament/"
    webpage = TOURNAMENT_ENDPOINT + slug
    print(f"parsing: {webpage}")

    # session = HTMLSession()
    # response = session.get(webpage)

    # response.html.render(sleep = 3, keep_page = True, scrolldown = 1)
    # soup = BeautifulSoup(response.html.html, "html.parser")

    file = open(f"{TOURNAMENTS_FOLDER}{slug}.html", "r")
    soup = BeautifulSoup(file, "html.parser")



    # NOTE: no metadata needed, its all stored in tournaments file
    # metadata = soup.find(class_ = "d-block").string
    # date, location, n_duelists, tier = metadata.split(" - ")
    # data = {
    #     "date": date,
    #     "location": location,
    #     "n_duelists": int(n_duelists.split()[0]),
    #     "tier": int(tier.split()[-1])

    # }

    partecipants_elem = soup.find_all(class_ = "tournament_table_row")


    partecipants = []
    for n, person in enumerate(partecipants_elem):
        name = person.find(class_ = "player-name")
        if name != None: name = name.string

        deck_name = person.find(class_  = "badge-ygoprodeck")
        if deck_name != None: deck_name = deck_name.get_text(strip = True)

        deck_id = person.get("href", None)
        if deck_id != None: deck_id = deck_id.split("/")[-1]

        # NOTE: deck link is deck name, cluster decks together using deck_name
        # and contrast them with other decks if differ in deck_id

        partecipants.append({
            "placement": n + 1,
            "player": name,
            "archetype": deck_name,
            "deck_id": deck_id,
        })


    #print(json.dumps(data, indent = 4))

    df = pd.DataFrame(data = partecipants)
    # print(df)
    df.to_csv(f"parsed/tournaments-{FORMAT}-{TIER}/{slug}.csv")

    file.close()
    # session.close()
    # del session

def parse_all_tournament_html():
    from os import listdir

    tournaments_html = listdir(f"raw/tournaments-{FORMAT}-{TIER}/")

    for tournament in tournaments_html:
        get_tournament_data_from_html(tournament.split(".")[0])




def get_deck_data(deck_id):
    webpage = WEBSITE_CORE_LINK + "deck/" + deck_id
    print(f"scraping {webpage}... ", end = "")

    session = HTMLSession()
    response = session.get(webpage)

    response.html.render(sleep = 3, keep_page = True, scrolldown = 1)
    print(response.status_code)

    soup = BeautifulSoup(response.html.html, "html.parser")


    def process_cards(cards_element_arr):

        tmp = [
            [
                x.find(class_ = "master-duel-card").get("data-card"),
                x.find(class_ = "master-duel-card").get("data-cardname")
            ]
            for x in cards_element_arr
        ]

        processed = []
        cards_id = []
        for n, element in enumerate(tmp):
            if element[0] in cards_id: continue # already counted, avoids creating duplicates
            cards_id.append(element[0])
            processed.append(
                {
                    "id": element[0],
                    "name": element[1],
                    "copies": tmp.count(element)
                }
            )

        return processed

    main_deck = soup.find(id = "main_deck").find_all(class_ = "ygodeckcard")
    main_deck = process_cards(main_deck)
    main_df = pd.DataFrame(data = main_deck)
    main_df["deck_part"] = 0 # NOTE: 0: main, 1: extra, 2: side

    extra_deck = soup.find(id = "extra_deck").find_all(class_ = "ygodeckcard")
    extra_deck = process_cards(extra_deck)
    extra_df = pd.DataFrame(data = extra_deck)
    extra_df["deck_part"] = 1

    side_deck = soup.find(id = "side_deck").find_all(class_ = "ygodeckcard")
    side_deck = process_cards(side_deck)
    side_df = pd.DataFrame(data = side_deck)
    side_df["deck_part"] = 2

    df = pd.concat([main_df, extra_df, side_df])
    print(df)
    df.to_csv(f"data/decks/{deck_id}.csv")


    session.close()
    del session


if __name__ == "__main__":
    # generate_tournament_names_data()
    # get_tournament_data_from_html("ycs-houston-2930")
    parse_all_tournament_html()
    # download_all_tournament_pages()
    # get_deck_data("goblin-biker-memento-588729")
