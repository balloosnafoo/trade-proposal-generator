
import nflgame as nfl
from trade_parameters import *

VALUES = {
    "passing_yds"   : 4,
    "passing_tds"   : 600,
    "passing_ints"  : -200,
    "rushing_yds"   : 10,
    "rushing_tds"   : 800,
    "receiving_yds" : 10,
    "receiving_rec" : 50,
    "receiving_tds" : 800,
    "fumbles_lost"  : -200
}

qb = [
    "passing_yds",
    "passing_tds",
    "passing_ints",
    "rushing_yds",
    "rushing_tds",
    "fumbles_lost"
]

wr = [
    "rushing_yds",
    "rushing_tds",
    "receiving_yds",
    "receiving_rec",
    "receiving_tds"
]

rb = wr

te = wr

REL_STATS = {
    "QB" : qb,
    "WR" : wr,
    "RB" : rb,
    "TE" : te
}