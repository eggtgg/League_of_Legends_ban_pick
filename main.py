from taipy.gui import Gui, notify
import connect_lol_db

show_dialog = ""
text = "Original text"
value = "Item 1"
ren = False
online_image_path_1 = ""
online_image_path_2 = ""
online_image_path_3 = ""
# Definition of the page
page = """
# Getting started with LOL DATA

Team 1

<|{online_image_path_1}|image|height=150px|width=150px|>
<|{online_image_path_2}|image|height=150px|width=150px|>
<|{online_image_path_3}|image|height=150px|width=150px|>


<|{champ_11_sel}|selector|lov={champ1}|type=connect_lol_db.Champion|adapter={lambda u: (u.id_champ, u.info)}|dropdown|width=130px|filter=True|>
<|{champ_sel2}|selector|lov={champ2}|type=User|adapter={lambda u: (u.id, u.name)}|dropdown|width=130px|propagate=True|>
<|{champ_sel3}|selector|lov={champ3}|type=User|adapter={lambda u: (u.id, u.name)}|dropdown|width=130px|propagate=True|>
<|part|partial={partial_A}|render={ren}|>
"""
A = """
Team 2

<|{online_image_path_1}|image|height=150px|width=150px|>
<|{online_image_path_2}|image|height=150px|width=150px|>
<|{online_image_path_3}|image|height=150px|width=150px|>
"""

def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.online_image_path_3 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + state.text +".png"
    state.text = "Button Pressed"


def on_change(state, var_name, var_value):
    if var_name == "champ_11_sel":
        state.online_image_path_1 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + var_value.id_champ +".png"
        print(var_value.id_champ)
        state.ren = True
    if var_name == "champ_sel2":
        state.online_image_path_2 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + var_value.name +".png"
        print(var_value.id)
    if var_name == "champ_sel3":
        state.online_image_path_3 = "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + var_value.name + ".png"
        print(var_value.id)
        return


class User:
    def __init__(self, id, name, birth_year):
        self.id , self.name, self.birth_year = (id, name, birth_year)
champ1 = connect_lol_db.champ_1

champ2 = [
    User("1", "Jhin", 1987),
    User("2", "Zed", 1979),
    User("3",   "Shen", 1968),
    User("4",  "Akali", 1974)
    ]

champ3 = [
    User("1", "Aatrox", 1987),
    User("2", "Yasuo", 1979),
    User("3",   "Yone", 1968),
    User("4",  "Kaisa", 1974)
    ]
champ_sel1 = champ1[1]
champ_sel2 = champ2[2]
champ_sel3 = champ3[3]

gui = Gui(page)
partial_A = gui.add_partial(A)
gui.run()
