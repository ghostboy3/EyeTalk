from taipy.gui import Gui
from taipy.gui import Html

my_theme = {
    
}
def hi():
    print("hi")

page = """
<h1>Welcome to Eye Talk</h1>

<h2>Eye Talk helps ensure clear communication between patients and their care givers.</h2>

<taipy:button  on_action="hi()">View Communication Board</taipy:button>

"""

html_page = Html(page)
Gui(page=html_page).run(theme=my_theme)
# Html(page=).run()
# print(value)