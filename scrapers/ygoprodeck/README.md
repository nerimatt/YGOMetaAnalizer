https://ygoprodeck.com/tournaments/


format tcg
tier - premier


# STEP 1

downloaded all tournaments metadata, "/raw/tournaments-TCG-3.csv" and downloaded all html pages
of all tournaments to be parsed in r

# STEP 2

parsed all tournaments html to csv in "parsed/tournaments-TCG-3/<>.csv"
it has placement of player, name, what they played and deck link

# STEP 3

parse every deck of every person and divide in folders
ex: "parsed/tournaments-TCG-3/decks/<tournament_slug>/<deck_id>.csv"
and then ideally merge all decks in one huge dataset
