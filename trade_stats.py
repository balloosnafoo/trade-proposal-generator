
import nflgame as nfl
from exporters import *

# Information specific to the trade

year = 2014
week = 10 # Number of the next unplayed week

sent_players = [
    "Tom Brady, NE", 
    "DeMarco Murray, DAL"
]

recd_players = [
    "Andrew Luck, IND", 
    "Eddie Lacy, GB"
]

# Set export type
create_tex  = True
create_html = False

# Positional stat getting functions

def get_qb_stats(player_stats):
    stats = []
    if player_stats == "BYE":
        stats = ["BYE", "BYE", "BYE", "BYE", "BYE"]
    else:
        stats.append(player_stats.passing_yds)
        stats.append(player_stats.rushing_yds)
        stats.append(player_stats.passing_ints)
        stats.append(player_stats.passing_tds)
        stats.append(player_stats.rushing_tds)
    return stats

def get_wr_stats(player_stats):
    stats = []
    if player_stats == "BYE":
        stats = ["BYE", "BYE", "BYE"]
    else:
        stats.append(player_stats.receiving_yds)
        stats.append(player_stats.receiving_rec)
        stats.append(player_stats.receiving_tds)
    return stats

def get_rb_stats(player_stats):
    if player_stats == "BYE":
        stats = ["BYE", "BYE", "BYE", "BYE", "BYE"]
    else:
        stats = []
        stats.append(player_stats.rushing_yds)
        stats.append(player_stats.rushing_att)
        stats.append(player_stats.rushing_tds)
        stats.append(player_stats.receiving_yds)
        stats.append(player_stats.receiving_tds)
    return stats

def get_te_stats(player_stats):
    if player_stats == "BYE":
        stats = ["BYE", "BYE", "BYE"]
    else:
        stats = []
        stats.append(player_stats.receiving_yds)
        stats.append(player_stats.receiving_rec)
        stats.append(player_stats.receiving_tds)
    return stats

# Globals

STAT_FUNCTIONS = {
    "QB": get_qb_stats,
    "WR": get_wr_stats,
    "RB": get_rb_stats,
    "TE": get_te_stats
}

HEADERS = {
    "QB": ["Pass Yds", "Rush Yds", "Ints", "Pass TDs", "Rush TDs"],
    "WR": ["Rec Yds", "Receptions", "Rec TDs"],
    "RB": ["Rush Yds", "Rush Att", "Rush TDs", "Rec Yds", "Rec TDs"],
    "TE": ["Rec Yds", "Receptions", "Rec TDs"]
}

def get_player_stats(player_info):

    player = get_player_object(player_info)
    team = player.team
    weeks = range(1, week)

    stats = []
    stats.append(HEADERS[player.position])

    for w in weeks:
        try:
            game = nfl.games(year, w, home=team, away=team)
            players = nfl.combine(game)
            player_game_stats = players.name(player.gsis_name)
        except:
            player_game_stats = "BYE"
        stats.append(STAT_FUNCTIONS[player.position](player_game_stats))

    return stats

def get_player_object(player_info):
    name, team = player_info.split(", ")
    for p in nfl.find(name):
        if team == p.team:
            player = p
    return player

def get_all_player_stats():
    data_sp = []
    for player in sent_players:
        data_sp.append(get_player_stats(player))

    data_rp = []
    for player in recd_players:
        data_rp.append(get_player_stats(player))

    return data_sp, data_rp


if __name__ == '__main__':
    data_sp, data_rp = get_all_player_stats()
    data = [sent_players, recd_players, data_sp, data_rp]

    if create_tex:
        export_as_tex(data)

