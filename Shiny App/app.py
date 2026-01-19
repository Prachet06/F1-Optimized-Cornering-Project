# TODO: Make an app that uses your CNN and perhaps other regression models etc.
from shiny import reactive, req
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title="F1", fillable=True)
ui.include_css("../Shiny App/styles.css")

with ui.sidebar():
    "Sidebar (input)"

"Main content (output)"