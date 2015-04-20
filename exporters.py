
import re

def export_as_tex(data):

    sent_players = data[0]
    recd_players = data[1]
    data_sp      = data[2]
    data_rp      = data[3]

    f = open("tex_template.txt", "r")
    w = open("result.tex", "w")
    for line in f:
        if re.search(r"SENT_PLAYER", line):
            for player in sent_players:
                w.write("\item " + player + "\n")
        elif re.search(r"RECEIVED_PLAYER", line):
            for player in recd_players:
                w.write("\item " + player + "\n")
        elif re.search(r"PLAYER_TABLE", line):
            for i in range(len(sent_players)):
                create_player_table(w, sent_players[i], data_sp[i])
            for i in range(len(recd_players)):
                create_player_table(w, recd_players[i], data_rp[i])
        else:
            w.write(line)
    f.close()
    w.close()

def create_player_table(write_file, player, player_data):
    template = open("player_table.txt", "r")
    for line in template:
        if re.search(r"DATA_LINE", line):
            for row in player_data[1:]:
                row_to_string(row)
                string  = "Week " + str(player_data.index(row)) + " & " 
                string += " & ".join(row) + "\\\\"
                write_file.write(string + "\n")
        elif re.search(r"HEADER", line):
            string = " & " + " & ".join(player_data[0]) + "\\\\"
            write_file.write(string + "\n")
        elif re.search(r"TABLE_SPEC", line):
            string = "l|"
            string += "c" * len(player_data[0])
            line = re.sub(r"TABLE_SPEC", string, line)
            write_file.write(line)
        elif re.search(r"PLAYER_NAME", line):
            line = re.sub(r"PLAYER_NAME", player, line)
            write_file.write(line)
        else:
            write_file.write(line)
    template.close()
    
def row_to_string(row):
    for i in range(len(row)):
        row[i] = str(row[i])
