import connect_lol_db

def champ_box_1(image_path, text):
    image_path = '{' + image_path + '}'
    text = '{' + text + '}'
    return f"""<|{image_path}|image|height=150px|width=150px|>
    <|{text}|input|>
"""


def champ_box_2(image_path, text):
    image_path = '{' + image_path + '}'
    text = '{' + text + '}'
    return f"""<|{image_path}|image|height=150px|width=150px|>
    <|{text}|input|>
    <|Khóa|button|on_action=on_button_""" + text[-3:-1] + "|>"

def get_link_champ(id_champ):
    return "http://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/" + id_champ + ".png"


def show_top_champ(name_list_champ, title, num=5):
    partial = f"###{title} " + "<|{text_" + name_list_champ[-2:] + "}|>\n"
    for i in range(num):
        par = '<|{get_link_champ(' + f'{name_list_champ}[{i}][0]' + ')}|image|height=75px|width=75px|>\n'
        partial += par
    return partial[0:-1]


def show_top_champ_teamed(name_list_champ, title, num=5):
    partial = f"###{title} " + "<|{champ_" + name_list_champ[-2:] + "sel}|>\n"
    for i in range(num):
        par = '<|{get_link_champ(' + f'{name_list_champ}[{i}][0]' + ')}|image|height=75px|width=75px|>\n'
        partial += par
    return partial[0:-1]


if __name__ == "__main__":
    print(show_top_champ_teamed("champ_t11","egg"))