# TODO: Make an app that uses your CNN and perhaps other regression models etc.
# TODO: Add a lot of images to the app to enhance its appearance
# TODO: Add a gif at the start or at the top of a page to again, improve its appearance
from shiny import reactive, req
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title="F1", fillable=True)
ui.include_css("../Shiny App/styles.css")

with ui.sidebar():
    "Sidebar (input)"

"Main content (output)"