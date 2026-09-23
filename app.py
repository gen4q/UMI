from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
from callbacks.iris_callbacks import register_callbacks

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY],
           title='Iris Data Explorer', suppress_callback_exceptions=True)
app.layout = html.Div(page_container)
register_callbacks(app)
server = app.server

if __name__ == '__main__':
    app.run(debug=False)
