from uuid import uuid4
from dash import register_page, html, dcc, dash_table
import dash_bootstrap_components as dbc
from backend.data_service import FEATURES, COLUMNS
from callbacks.iris_callbacks import make_figure

register_page(__name__, path='/')
LABELS = ('Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width')


def layout():
    filters = []
    for column, label in zip(FEATURES, LABELS):
        filters.append(dbc.Col([
            html.Div([html.Label(label, htmlFor=column),
                      html.Span('—', id=f'{column}-range', className='range-value')], className='filter-label'),
            dcc.RangeSlider(id=column, min=0, max=1, value=[0, 1], step=0.1,
                            disabled=True, marks={}, allowCross=False, updatemode='drag',
                            tooltip={'placement': 'bottom', 'always_visible': False}),
        ], md=6, className='mb-3'))
    return dbc.Container([
        html.Div(str(uuid4()), id='page-key', hidden=True),
        html.Header([html.P('UMELÁ INTELIGENCIA / LABORATÓRNA ÚLOHA 01', className='eyebrow'),
                     html.H1('Iris Data Explorer Dashboard'),
                     html.P('Preskúmajte rozmery kvetov a porovnajte tri druhy kosatcov.', className='text-muted')]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H2('Prehľad dát'),
                html.Div([html.Span('Všetky záznamy'), html.Strong('0', id='total-count')], className='stat'),
                html.Div([html.Span('Vyfiltrované'), html.Strong('0', id='filtered-count')], className='stat'),
                html.Div([html.Span('Zobrazená strana'), html.Strong('0 / 0', id='page-info')], className='stat'),
                html.P('Stlačte „Načítať dáta“.', id='load-status', role='status', className='status'),
                dbc.Button('Načítať dáta', id='load-button', n_clicks=0, color='primary', className='w-100'),
            ])), md=4),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='species-chart', figure=make_figure(),
                config={'displayModeBar': False}, style={'height': '300px'}))), md=8),
        ], className='g-3 mb-3'),
        dbc.Card(dbc.CardBody([html.H2('Filtrovanie rozsahov'),
            html.P('Rozmery v cm. Všetky štyri podmienky platia súčasne (AND).', className='text-muted small'),
            dbc.Row(filters),
        ]), className='mb-3'),
        dbc.Card(dbc.CardBody([
            html.Div([html.H2('Vyfiltrované dáta'), html.Span('10 záznamov na strane', className='text-muted small')], className='table-heading'),
            html.P('Najskôr načítajte dataset.', id='result-message', role='status', className='small text-muted'),
            dash_table.DataTable(id='iris-table', columns=[{'name': c, 'id': c} for c in COLUMNS],
                data=[], page_size=10, page_current=0, page_action='native', sort_action='native',
                style_table={'overflowX': 'auto'},
                style_cell={'fontFamily': 'system-ui', 'fontSize': 13, 'padding': '7px 12px', 'textAlign': 'left'},
                style_header={'backgroundColor': '#edf3f5', 'fontWeight': '600'},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f8fafb'}]),
        ])),
        html.Footer('Tabuľka, počty aj graf zobrazujú výsledok rovnakého filtra. • Iris / 3 druhy / 4 vlastnosti'),
    ], className='py-4', style={'maxWidth': '1120px'})
