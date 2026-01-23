# TODO: Make an app that uses your CNN and perhaps other regression models etc.
# TODO: Add a lot of images to the app to enhance its appearance
# TODO: Add a gif at the start or at the top of a page to again, improve its appearance
# TODO: Add a section to view each model's cnn structure
# TODO: Start making scaffolds for the app, for example, have a section for the cnn prediction but for now just make it an if else statement and so on
#       this allows for you to get a better feel of how the final app will look
 
# TODO: Have a diagram of sector 1 and maybe the images of all the turns it has. 
from shiny import reactive, req
from shiny.express import input, render, ui
from faicons import icon_svg as icon
from shinywidgets import render_plotly
from pathlib import Path

# TODO: fix the css issue (not having the multiple page setup is a solution.)
print("CWD:", Path.cwd())
print("CSS resolves to:", (Path(__file__).parent / "styles.css").resolve())
print("Exists:", (Path(__file__).parent / "styles.css").exists())

ui.page_opts(title="F1", fillable=True)

with ui.nav_panel("About the Project"):
    "info about project here. Explain what apexes are and how all of it works, how every tenth or hundredth of a second matters etc."

    with ui.card(full_screen=True):
        ui.card_header("A card with a header, add an interactive graph here maybe")
        @render.plot
        def plot():
            import matplotlib.pyplot as plt
            return plt.scatter([1, 2, 3], [4, 5, 6])

    with ui.card():
        "Random information here perhaps."


    with ui.layout_columns(col_widths=[6, 6]):
        # visit: https://fontawesome.com/v4/icons/
        # for more icons
        with ui.value_box(showcase=icon("trophy")):
            "Total laps of data recorded"
            "300"
        with ui.value_box(showcase=icon("image")):
            "Total images used"
            "1000"

            #with ui.tooltip():
            #    icon("circle-info")
            #    "These images the points at the track where the driver either hits the throttle or the brakes."

with ui.nav_panel("Prediction"):
    "Add the saved cnn model or models here. Provide users with photos to choose from, maybe make it a game that asks the user to pick the image they think is the fastest and then the cnn makes it guess and then compare it with the real data."