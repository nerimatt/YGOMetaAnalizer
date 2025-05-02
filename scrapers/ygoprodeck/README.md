https://ygoprodeck.com/tournaments/


format tcg
tier - premier


# STEP 1

downloaded all tournaments metadata, "/raw/tournaments-TCG-3.csv"
`generate_tournament_names_data`


and downloaded all html pages of all tournaments to be parsed in r
`download_all_tournament_pages()`

# STEP 2

parsed all tournaments html to csv in "parsed/tournaments-TCG-3/<>.csv"
it has placement of player, name, what they played and deck link
`parse_all_tournament_html()`

parsed in r tournaments, removed those with no winners, and chose only those in 6 months
also removed team events



# STEP 3

download every deck html of parsed tournaments
ex: "raw/tournaments-TCG-3/decks/<tournament_slug>/<deck_id>.html"

parse every deck of every person and divide in folders
ex: "parsed/tournaments-TCG-3/decks/<tournament_slug>/<deck_id>.csv"
and then ideally merge all decks in one huge dataset
