import pyodbc


def get_db_conn():
    ket_noi = pyodbc.connect('DRIVER={SQL Server};SERVER=MINHTRIHO;DATABASE=LolDB;UID=mt;PWD=123456')
    return ket_noi


def get_champs(lenh_truy_van):
    ket_noi = get_db_conn()
    cursor = ket_noi.cursor()
    cursor.execute(lenh_truy_van)
    champs = cursor.fetchmany(10)
    cursor.close()
    ket_noi.close()
    return champs


def khac_che(champ_id):
    return f"""SELECT dbo.ChampionGoLane.IDChampion, dbo.ChampionGoLane.IDLane, {champ_id}.RatePlus
FROM dbo.ChampionGoLane
INNER JOIN (SELECT * FROM dbo.ChampionGoLane INNER JOIN dbo.ChampionGoLaneWith
ON ChampionGoLane.IDChampLane = ChampionGoLaneWith.Loser
WHERE ChampionGoLaneWith.Loser LIKE '{champ_id}%' AND Tier <> 'Off Meta') AS {champ_id}
ON {champ_id}.Winner = ChampionGoLane.IDChampLane
WHERE ChampionGoLane.Tier <> 'Off Meta'
ORDER BY RatePlus DESC"""


def teamed_well(champ_id):
    return f"""SELECT ChampionGoLane.IDChampion AS KeyChamp, ChampionGoLane.IDLane AS Subchamp, RatePlus
FROM dbo.ChampionGoLane
INNER JOIN(SELECT * FROM dbo.ChampionGoLane INNER JOIN dbo.ChampionTeamedWith
ON ChampionGoLane.IDChampLane = ChampionTeamedWith.IDChampLane1
WHERE ChampionTeamedWith.IDChampLane1 LIKE '{champ_id}%' AND Tier <> 'Off Meta') AS {champ_id}
ON ChampionGoLane.IDChampLane = {champ_id}.IDChampLane2
WHERE ChampionGoLane.Tier <> 'Off Meta'
UNION
SELECT ChampionGoLane.IDChampion AS KeyChamp, ChampionGoLane.IDLane AS Subchamp, RatePlus
FROM dbo.ChampionGoLane
INNER JOIN(SELECT * FROM dbo.ChampionGoLane INNER JOIN dbo.ChampionTeamedWith
ON ChampionGoLane.IDChampLane = ChampionTeamedWith.IDChampLane2
WHERE ChampionTeamedWith.IDChampLane2 LIKE '{champ_id}%' AND Tier <> 'Off Meta') AS {champ_id}
ON ChampionGoLane.IDChampLane = {champ_id}.IDChampLane1
WHERE ChampionGoLane.Tier <> 'Off Meta'
ORDER BY RatePlus DESC"""


def team_all(first_champ, *list_sub_champ):
    if len(list_sub_champ)<1:
        return
    if len(list_sub_champ)==1:
        and_like = "'" + list_sub_champ[0] + "%" + "'"
        and_like_2 = and_like
    if len(list_sub_champ) > 1:
        and_like = and_like_2 = ""
        for champ in list_sub_champ[:-1]:
            and_like += "'"+champ + "%"+"' "+"OR IDChampLane2 LIKE "
            and_like_2 += "'"+champ + "%"+"' "+"OR IDChampLane1 LIKE "
        and_like += "'" + list_sub_champ[-1] + "%" + "'"
        and_like_2 += "'" + list_sub_champ[-1] + "%" + "'"
    return f"""SELECT IDChampLane1, IDChampLane2, RatePlus FROM dbo.ChampionGoLane INNER JOIN
(SELECT * FROM dbo.ChampionTeamedWith INNER JOIN dbo.ChampionGoLane
ON ChampionTeamedWith.IDChampLane2 = ChampionGoLane.IDChampLane
WHERE IDChampLane1 LIKE '{first_champ}%' AND (IDChampLane2 LIKE {and_like})) AS CHAMP
ON ChampionGoLane.IDChampLane = CHAMP.IDChampLane1
WHERE ChampionGoLane.Tier <> 'Off Meta' AND CHAMP.Tier <> 'Off Meta'
UNION
SELECT IDChampLane1, IDChampLane2, RatePlus FROM dbo.ChampionGoLane INNER JOIN
(SELECT * FROM dbo.ChampionTeamedWith INNER JOIN dbo.ChampionGoLane
ON ChampionTeamedWith.IDChampLane2 = ChampionGoLane.IDChampLane
WHERE IDChampLane2 LIKE '{first_champ}%' AND (IDChampLane1 LIKE {and_like_2})) AS CHAMP
ON ChampionGoLane.IDChampLane = CHAMP.IDChampLane1
WHERE ChampionGoLane.Tier <> 'Off Meta' AND CHAMP.Tier <> 'Off Meta'
"""


def in_team(*list_champ_in_team):
    list_que = []
    for champ in list_champ_in_team:
        first_champ = champ
        list_sub_champ = list_champ_in_team[1:]
        print("đầu ", first_champ, " Sau ", list_sub_champ)
        list_que.append(team_all(first_champ, *list_sub_champ))
        list_champ_in_team = list_sub_champ
        if len(list_champ_in_team) == 1:
            break
    return list_que

def rate_in_team(list_que):
    list_rate = []
    for que in list_que:
        for result in get_champs(que):
            if result[2] == 0:
                list_rate.append(50)
            if result[2] < 0:
                list_rate.append(49 + result[2])
            if result[2] > 0:
                list_rate.append(51 + result[2])
    return sum(list_rate)/ len(list_rate)


def win_opponent(champ, *list_champ_opponent_team):
    if len(list_champ_opponent_team) < 1:
        return
    or_like = ""
    for champ_2 in list_champ_opponent_team[:-1]:
        or_like += f"Loser LIKE '{champ_2}%' OR "
    or_like += f"Loser LIKE '{list_champ_opponent_team[-1]}%'"
    return f"""SELECT RatePlus FROM dbo.ChampionGoLane INNER JOIN
(SELECT * FROM dbo.ChampionGoLaneWith INNER JOIN dbo.ChampionGoLane
ON ChampionGoLaneWith.Loser = ChampionGoLane.IDChampLane
WHERE Winner LIKE '{champ}%' AND ({or_like})) AS CHAMP
ON ChampionGoLane.IDChampLane = CHAMP.Winner
WHERE ChampionGoLane.Tier <> 'Off Meta' AND CHAMP.Tier <> 'Off Meta'"""


def lose_opponent(champ, *list_champ_opponent_team):
    if len(list_champ_opponent_team) < 1:
        return
    or_like = ""
    for champ_2 in list_champ_opponent_team[:-1]:
        or_like += f"Winner LIKE '{champ_2}%' OR "
    or_like += f"Winner LIKE '{list_champ_opponent_team[-1]}%'"
    return f"""SELECT RatePlus FROM dbo.ChampionGoLane INNER JOIN
(SELECT * FROM dbo.ChampionGoLaneWith INNER JOIN dbo.ChampionGoLane
ON ChampionGoLaneWith.Loser = ChampionGoLane.IDChampLane
WHERE Loser LIKE '{champ}%' AND ({or_like})) AS CHAMP
ON ChampionGoLane.IDChampLane = CHAMP.Winner
WHERE ChampionGoLane.Tier <> 'Off Meta' AND CHAMP.Tier <> 'Off Meta'"""


def rate_win_opponent(list_champ_team, list_champ_opponent_team):
    for c in list_champ_team:
        a = get_champs(win_opponent(c, *list_champ_opponent_team))
        list_rate = []
        if len(a) != 0:
            for i in a:
                list_rate.append(i[0]+51)
        return list_rate


def rate_lose_opponent(list_champ_team, list_champ_opponent_team):
    for c in list_champ_team:
        a = get_champs(lose_opponent(c, *list_champ_opponent_team))
        list_rate = []
        if len(a) != 0:
            for i in a:
                list_rate.append(49-i[0])

        return list_rate


truy_van_champ1 = '''
SELECT IDChampion, IDLane, WinRate FROM dbo.ChampionGoLane
WHERE Tier = 'S+'
ORDER BY Winrate DESC
'''

truy_van_test = """
SELECT IDChampion, IDLane, WinRate FROM dbo.ChampionGoLane
WHERE Tier = 'S+'
ORDER BY Winrate DESC
"""


truy_van_id_champs = """
SELECT IDChampion FROM dbo.Champion
"""

if __name__ == "__main__":
    #print(team_all("Shen", "Jinx", "Hayate"))
    team_1 = ["Shen", "Yasuo", "Maokai", "Jinx", "LeeSin"]
    team_2 = ["Aatrox", "Zed", "Jhin", "Kayle", "Teemo"]
    #a_2 = in_team('Shen', 'Lillia', 'Karthus', 'Skarner', 'Annie')
    list_rate = rate_win_opponent(team_1, team_2) + rate_lose_opponent(team_1, team_2)
    print(sum(list_rate)/len(list_rate))