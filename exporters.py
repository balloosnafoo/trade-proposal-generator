
import re
from trade_parameters import header, closing_argument

def export_as_tex(data):

    sent_players = data[0]
    recd_players = data[1]
    data_sp      = data[2]
    data_rp      = data[3]
    likes = find_like_for_like(sent_players, recd_players)

    f = open("templates/tex_template.txt", "r")
    w = open("output/result.tex", "w")

    write = True
    for line in f:
        match = re.search(r"{{(.*)}}", line)
        if not match and write:
            w.write(line)
            continue
        match = match.group(1).strip()
        if   match == "SENT_PLAYER":
            for player in sent_players:
                w.write("\item " + player.name + ", " + player.team + "\n")
        elif match == "RECEIVED_PLAYER":
            for player in recd_players:
                w.write("\item " + player.name + ", " + player.team + "\n")
        elif match == "PLAYER_TABLE":
            for i in range(len(sent_players)):
                create_player_table(w, sent_players[i], data_sp[i])
            for i in range(len(recd_players)):
                create_player_table(w, recd_players[i], data_rp[i])
        elif match == "POSITION_TABLE" and likes:
            for position in likes:
                create_position_table(w, data, position)
        elif match == "POSITION_SECTION":
            if likes:
                continue
            write = not write
        elif match == "CLOSING_ARGUMENT":
            if closing_argument:
                write_closing_argument(w)
        elif match == "HEADER":
            if header:
                write_header(w)
    f.close()
    w.close()

def create_player_table(write_file, player, player_data):
    template = open("templates/player_table.txt", "r")
    for line in template:
        match = re.search(r"{{(.*)}}", line)
        if not match:
            write_file.write(line)
            continue
        match = match.group(1).strip()
        if match == "DATA_LINE":
            for row in player_data[1:]:
                row_to_string(row)
                string  = "Week " + str(player_data.index(row)) + " & " 
                string += " & ".join(row) + "\\\\"
                write_file.write(string + "\n")
        elif match == "HEADER":
            string = " & " + " & ".join(player_data[0]) + "\\\\"
            write_file.write(string + "\n")
        elif match == "TABLE_SPEC":
            string = "l|"
            string += "c" * len(player_data[0])
            string = string[0:-1] + "|" + string[-1] + "|"
            line = re.sub(r"{{.*}}", string, line)
            write_file.write(line)
        elif match == "PLAYER_NAME":
            line = re.sub(r"{{.*}}", player.name, line)
            write_file.write(line)
    template.close()

def create_position_table(write_file, data, position):
    table_data = filter_data_by_pos(position, data)
    template = open("templates/position_table.txt", "r")
    for line in template:
        match = re.search(r"{{(.*)}}", line)
        if not match:
            write_file.write(line)
            continue
        match = match.group(1).strip()
        if match == "DATA_LINE":
            for i in range(len(table_data)):
                player = table_data[i][0]
                if table_data[i] == "---":
                    write_file.write("\hline \n")
                else:
                    ave_stats = weekly_to_average(table_data[i][1])
                    string =  player.name + " & "
                    row_to_string(ave_stats)
                    string += " & ".join(ave_stats) + "\\\\"
                    write_file.write(string + "\n")
        elif match == "HEADER":
            string = " & " + " & ".join(table_data[0][1][0]) + "\\\\"
            write_file.write(string + "\n")
        elif match == "TABLE_SPEC":
            string =  "l|"
            string += "c" * len(table_data[0][1][0])
            string = string[0:-1] + "|" + string[-1] + "|"
            line = re.sub(r"{{.*}}", string, line)
            write_file.write(line)
        elif match == "TITLE":
            string = table_data[0][0].position + " Comparison"
            line = re.sub(r"{{.*}}", string, line)
            write_file.write(line)
    template.close()

def find_like_for_like(sent, received):
    likes = []
    for player_s in sent:
        for player_r in received:
            if player_s.position == player_r.position:
                if player_s.position not in likes:
                    likes.append(player_s.position)
    if len(likes) == 0:
        likes = False
    return likes

def row_to_string(row):
    for i in range(len(row)):
        if type(row[i]) == int:
            row[i] = str(row[i])
        elif type(row[i]) == float:
            if row[i] != 0:
                row[i] = "%.2f" % row[i]
            else:
                row[i] = "0"

def weekly_to_average(stats):
    averages = []
    num_stat_categories = len(stats[0])
    for i in range(num_stat_categories):
        total = 0
        items = 0
        for row in stats:
            if row == stats[0]:
                continue
            elif row[i] not in ["BYE", "DNP"] and type(row[i]) != str: 
                total += row[i]
                items += 1
            elif row[i] not in ["BYE", "DNP"] and type(row[i]) == str:
                total += float(row[i])
                items += 1
        items *= 1.0
        averages.append(total / items)
    return averages

def filter_data_by_pos(position, data):
    filtered_data = []
    counter = 0

    for player in data[0]: # sent_players
        if player.position == position:
            # Grabs player object and stat list
            filtered_data.append([data[0][counter], data[2][counter]])
        counter += 1
    counter = 0

    filtered_data.append("---")

    for player in data[1]: # recd_players
        if player.position == position:
            # Grabs player object and stat list
            filtered_data.append([data[1][counter], data[3][counter]])
        counter += 1

    return filtered_data

def write_closing_argument(write_file):
    c = open("templates/closing_argument.txt", "r")
    for line in c:
        write_file.write(line)
    c.close()

def write_header(write_file):
    h = open("templates/header.txt", "r")
    for line in h:
        write_file.write(line)
    h.close()

def compare_averages(ave_stats):
    """
    Have to figure out the best way to make sure negative stats and positive stats pick appropriate winners before writing this function.
    """
    pass


