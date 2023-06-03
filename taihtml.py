from taipy.gui import Gui

text = "Original text"

page = """
<|Click me|button|id=my_button|>
"""

my_theme = {
"my_button" : {
  "color": "red"
    }
}
if __name__ == "__main__":
    Gui(page).run(theme=my_theme)