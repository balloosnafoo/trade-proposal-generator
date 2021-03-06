
import nflgame as nfl
from exporters import *

from trade_parameters import *
from points_system import *

# Set export type
create_tex  = True
create_html = False # HTML output is unfinished, don't set to True

# Positional stat getting functions
def get_qb_stats(player_stats):
    stats = []
    if type(player_stats) == str:
        stats = [player_stats] * 5
    else:
        stats.append(player_stats.passing_yds)
        stats.append(player_stats.rushing_yds)
        stats.append(player_stats.passing_ints)
        stats.append(player_stats.passing_tds)
        stats.append(player_stats.rushing_tds)
    return stats

def get_wr_stats(player_stats):
    stats = []
    if type(player_stats) == str:
        stats = [player_stats] * 3
    else:
        stats.append(player_stats.receiving_yds)
        stats.append(player_stats.receiving_rec)
        stats.append(player_stats.receiving_tds)
    return stats

def get_rb_stats(player_stats):
    if type(player_stats) == str:
        stats = [player_stats] * 5
    else:
        stats = []
        stats.append(player_stats.rushing_yds)
        stats.append(player_stats.rushing_att)
        stats.append(player_stats.rushing_tds)
        stats.append(player_stats.receiving_yds)
        stats.append(player_stats.receiving_tds)
    return stats

def get_te_stats(player_stats):
    if type(player_stats) == str:
        stats = [player_stats] * 3
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
    "QB": ["Pass Yds", "Rush Yds", "Ints", "Pass TDs", "Rush TDs", "FP"],
    "WR": ["Rec Yds", "Receptions", "Rec TDs", "FP"],
    "RB": ["Rush Yds", "Rush Att", "Rush TDs", "Rec Yds", "Rec TDs", "FP"],
    "TE": ["Rec Yds", "Receptions", "Rec TDs", "FP"]
}

# Functions
def get_player_stats(player):

    team = player.team
    weeks = range(1, week)

    stats = []
    stats.append(HEADERS[player.position])

    for w in weeks:
        try:
            game = nfl.games(year, w, home=team, away=team)
            players = nfl.combine(game)
            player_game_stats = players.name(player.gsis_name)
            if not player_game_stats:
                player_game_stats = "DNP"
        except:
            player_game_stats = "BYE"
        stats.append(STAT_FUNCTIONS[player.position](player_game_stats))
        stats[-1].append(score_player(player_game_stats, player.position))

    return stats

def get_player_object(player_info):
    name, team = player_info.split(", ")
    for p in nfl.find(name):
        if team == p.team:
            player = p
    return player

def get_all_player_stats():

    data_sp = []
    for i in range(len(sent_players)):
        sent_players[i] = get_player_object(sent_players[i])
        data_sp.append(get_player_stats(sent_players[i]))

    data_rp = []
    for i in range(len(recd_players)):
        recd_players[i] = get_player_object(recd_players[i])
        data_rp.append(get_player_stats(recd_players[i]))

    return data_sp, data_rp

def score_player(player_stats, position):
    if player_stats == "BYE":
        return "BYE"
    elif player_stats == "DNP":
        return "DNP"
    score = 0
    for item in REL_STATS[position]:
        try:
            score += player_stats.stats[item] * VALUES[item]
        except:
            score += 0
    return str(score/100.0)


if __name__ == '__main__':
    data_sp, data_rp = get_all_player_stats()
    data = [sent_players, recd_players, data_sp, data_rp]

    if create_tex:
        export_as_tex(data)

