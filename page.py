from taipy.gui import Gui, notify
import connect_lol_db

champ_a21 = champ_a22 = champ_a23 = champ_a24 = champ_a25 = []
champ_t11 = champ_t12 = champ_t13 = champ_t14 = []
name_champ_11 = name_champ_12 = name_champ_13 = name_champ_14 = name_champ_15 = ""
text_21 = text_22 = text_23 = text_24 = text_25 = ''

rate = rate_1 = rate_2 = 0
s_rate = False

s11 = True
a21 = a22 = a23 = a24 = False
t11 = t12 = t13 = False

unknow_champ = "http://ddragon.leagueoflegends.com/cdn/13.6.1/img/profileicon/29.png"

image_team_1_champ_1 = image_team_1_champ_2 = image_team_1_champ_3 = image_team_1_champ_4 = image_team_1_champ_5 = \
    unknow_champ

image_team_2_champ_1 = image_team_2_champ_2 = image_team_2_champ_3 = image_team_2_champ_4 = image_team_2_champ_5 = \
    unknow_champ

page = """
<|layout|columns= 5 4|
    <|
# Getting started with LOL DATA
    |>
    <|
<|part|partial={partial_rate}|render={s_rate}|>
    |>
|>
## Team 1
<|layout|columns= 5 4|
    <|
<|layout|columns=1 1 1 1 1|
    <|
<|{image_team_1_champ_1}|image|height=150px|width=150px|>
<|{champ_11_sel}|selector|lov={champ_11}|type=set|adapter={lambda u: (u[0], u[0])}|dropdown|width=130px|> 
    |>
    <|
<|part|partial={partial_12}|render={image_team_2_champ_2}|>
    |>
    <|
<|part|partial={partial_13}|render={image_team_2_champ_2}|>
    |>
    <|
<|part|partial={partial_14}|render={image_team_2_champ_4}|>
    |>
    <|
<|part|partial={partial_15}|render={image_team_2_champ_4}|>
    |>
|>

## Team 2

<|layout|columns=1 1 1 1 1|
    <|
<|part|partial={partial_21}|render={image_team_1_champ_1}|>
    |>
    <|
<|part|partial={partial_22}|render={image_team_1_champ_1}|>
    |>
    <|
<|part|partial={partial_23}|render={image_team_1_champ_3}|>
    |>
    <|
<|part|partial={partial_24}|render={image_team_1_champ_3}|>
    |>
    <|
<|part|partial={partial_25}|render={image_team_1_champ_5}|>
    |>
|>
    |>
    <|
<|part|partial={partial_top}|render={s11}|>

<|part|partial={partial_top_a21}|render={a21}|>

<|part|partial={partial_top_a22}|render={a22}|>

<|part|partial={partial_top_a23}|render={a23}|>

<|part|partial={partial_top_a24}|render={a24}|>

<|part|partial={partial_top_t11}|render={t11}|>

<|part|partial={partial_top_t12}|render={t12}|>

<|part|partial={partial_top_t13}|render={t13}|>
    |>
|>
"""


def on_button_21(state):
    notify(state, 'info', f'The text is: {state.text_21}')
    state.champ_a21 = connect_lol_db.get_champs(connect_lol_db.khac_che(state.text_21))
    state.s11 = False
    state.champ_12 = state.champ_a21 + state.champ_t11
    state.a21 = True


def on_button_22(state):
    notify(state, 'info', f'The text is: {state.text_22}')
    state.champ_a22 = connect_lol_db.get_champs(connect_lol_db.khac_che(state.text_22))
    state.champ_13 = state.champ_a22 + state.champ_t11
    state.a22 = True


def on_button_23(state):
    notify(state, 'info', f'The text is: {state.text_23}')
    state.champ_a23 = connect_lol_db.get_champs(connect_lol_db.khac_che(state.text_23))
    state.champ_14 = state.champ_a23 + state.champ_t12
    state.a23 = True


def on_button_24(state):
    notify(state, 'info', f'The text is: {state.text_24}')
    state.champ_a24 = connect_lol_db.get_champs(connect_lol_db.khac_che(state.text_24))
    state.champ_15 = state.champ_a24 + state.champ_t13
    state.a24 = True


def on_button_25(state):
    notify(state, 'info', f'The text is: {state.text_25}')
    que_team_2 = connect_lol_db.in_team(state.text_21, state.text_22, state.text_23, state.text_24, state.text_25)
    que_team_1 = connect_lol_db.in_team(state.name_champ_11, state.name_champ_12, state.name_champ_13, state.name_champ_14, state.name_champ_15)
    state.rate_2 = connect_lol_db.rate_in_team(que_team_2)
    state.rate_1 = connect_lol_db.rate_in_team(que_team_1)
    rate_in_team = state.rate_1/ (state.rate_1+state.rate_2)*100
    rate_with_opponent = connect_lol_db.rate_win_opponent([state.name_champ_11, state.name_champ_12, state.name_champ_13, state.name_champ_14, state.name_champ_15],
                                                          [state.text_21, state.text_22, state.text_23, state.text_24, state.text_25]) + connect_lol_db.rate_lose_opponent(
        [state.name_champ_11, state.name_champ_12, state.name_champ_13, state.name_champ_14, state.name_champ_15],
        [state.text_21, state.text_22, state.text_23, state.text_24, state.text_25])
    print(sum(rate_with_opponent)/len(rate_with_opponent))
    print(rate_in_team)
    state.rate = (rate_in_team + sum(rate_with_opponent)/len(rate_with_opponent))/2
    state.s_rate = True



def champ_box_2(image_path, text):
    image_path = '{' + image_path + '}'
    text = '{' + text + '}'
    return f"""<|{image_path}|image|height=150px|width=150px|>
    <|{text}|input|>
    <|Khóa|button|on_action=on_button_{text[-3:-1]}|>
"""


def champ_box_1(image_path, champ_sel, champ_list):
    return "<|{" + image_path + """}|image|height=150px|width=150px|>
    <|{""" + champ_sel + \
           "}|selector|lov={" + champ_list + \
           "}|type=pyodbc.Row|adapter={lambda u: (u[0], u[0])}|dropdown|width=130px|>"


def get_link_champ(id_champ):
    return "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + id_champ + ".png"


def show_top_champ_anti(name_list_champ, title, num=5):
    partial = f"###{title} " + "<|{text_" + name_list_champ[-2:] + "}|>\n"
    for i in range(num):
        par = '<|{get_link_champ(' + f'{name_list_champ}[{i}][0]' + ')}|image|height=75px|width=75px|>\n'
        partial += par
    return partial[0:-1]


def show_top_champ_teamed(name_list_champ, title, num=5):
    partial = f"###{title} " + "<|{champ_" + name_list_champ[-2:] + "_sel[0]}|>\n"
    for i in range(num):
        par = '<|{get_link_champ(' + f'{name_list_champ}[{i}][0]' + ')}|image|height=75px|width=75px|>\n'
        partial += par
    return partial[0:-1]


def on_change(state, var_name, var_value):
    if var_name == "champ_11_sel":
        state.image_team_1_champ_1 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + \
                                     var_value[0] + ".png"
        state.champ_t11 = connect_lol_db.get_champs(connect_lol_db.teamed_well(var_value[0]))
        state.t11 = True
        state.name_champ_11 = var_value[0]

    if var_name == "champ_12_sel":
        state.image_team_1_champ_2 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + \
                                     var_value[0] + ".png"
        state.champ_t12 = connect_lol_db.get_champs(connect_lol_db.teamed_well(var_value[0]))
        state.t12 = True
        state.name_champ_12 = var_value[0]

    if var_name == "champ_13_sel":
        state.image_team_1_champ_3 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + \
                                     var_value[0] + ".png"
        state.champ_t13 = connect_lol_db.get_champs(connect_lol_db.teamed_well(var_value[0]))
        state.t13 = True
        state.a21 = state.a22 = state.t11 = False
        state.name_champ_13 = var_value[0]

    if var_name == "champ_14_sel":
        state.image_team_1_champ_4 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + \
                                     var_value[0] + ".png"
        state.name_champ_14 = var_value[0]

    if var_name == "champ_15_sel":
        state.image_team_1_champ_5 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + \
                                     var_value[0] + ".png"
        state.name_champ_15 = var_value[0]

    if var_name == "text_21":
        state.image_team_2_champ_1 = get_link_champ(state.text_21)

    if var_name == "text_22":
        state.image_team_2_champ_2 = get_link_champ(state.text_22)

    if var_name == "text_23":
        state.image_team_2_champ_3 = get_link_champ(state.text_23)

    if var_name == "text_24":
        state.image_team_2_champ_4 = get_link_champ(state.text_24)

    if var_name == "text_25":
        state.image_team_2_champ_5 = get_link_champ(state.text_25)


champ_11 = connect_lol_db.get_champs(connect_lol_db.truy_van_champ1)
champ_11_sel = champ_11[1]

champ_12 = champ_11
champ_12_sel = champ_12[1]

champ_13 = champ_11
champ_13_sel = champ_13[3]

champ_14 = champ_11
champ_14_sel = champ_14[1]

champ_15 = champ_11
champ_15_sel = champ_15[3]

gui = Gui(page)

# 2 vong for la qua ok
partial_12 = gui.add_partial(champ_box_1('image_team_1_champ_2', 'champ_12_sel', 'champ_12'))
partial_13 = gui.add_partial(champ_box_1('image_team_1_champ_3', 'champ_13_sel', 'champ_13'))
partial_14 = gui.add_partial(champ_box_1('image_team_1_champ_4', 'champ_14_sel', 'champ_14'))
partial_15 = gui.add_partial(champ_box_1('image_team_1_champ_5', 'champ_15_sel', 'champ_15'))

partial_21 = gui.add_partial(champ_box_2('image_team_2_champ_1', 'text_21'))
partial_22 = gui.add_partial(champ_box_2('image_team_2_champ_2', 'text_22'))
partial_23 = gui.add_partial(champ_box_2('image_team_2_champ_3', 'text_23'))
partial_24 = gui.add_partial(champ_box_2('image_team_2_champ_4', 'text_24'))
partial_25 = gui.add_partial(champ_box_2('image_team_2_champ_5', 'text_25'))

partial_top = gui.add_partial(show_top_champ_anti('champ_11', "Chọn đầu (5 tướng mạnh nhất)"))
partial_top_t11 = gui.add_partial(show_top_champ_teamed('champ_t11', "Phối hợp tốt với"))
partial_top_t12 = gui.add_partial(show_top_champ_teamed('champ_t12', "Phối hợp tốt với"))
partial_top_t13 = gui.add_partial(show_top_champ_teamed('champ_t13', "Phối hợp tốt với"))

partial_top_a21 = gui.add_partial(show_top_champ_anti("champ_a21", "Khắc chế"))
partial_top_a22 = gui.add_partial(show_top_champ_anti("champ_a22", "Khắc chế"))
partial_top_a23 = gui.add_partial(show_top_champ_anti("champ_a23", "Khắc chế"))
partial_top_a24 = gui.add_partial(show_top_champ_anti("champ_a24", "Khắc chế"))

partial_rate = gui.add_partial("###Ti le thang: <|{rate}|>")
gui.run()
