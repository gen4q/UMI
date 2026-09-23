from math import ceil
from dash import Input, Output, State
import plotly.graph_objects as go
from backend.data_service import FEATURES, SPECIES, load_iris_data, set_data, get_data, clear_data, filter_data


def make_figure(df=None):
    fig = go.Figure()
    if df is None:
        fig.add_annotation(text='Načítajte dáta pomocou tlačidla.', x=0.5, y=0.5,
                           xref='paper', yref='paper', showarrow=False)
    else:
        counts = df['species'].value_counts().reindex(SPECIES, fill_value=0)
        fig.add_bar(x=list(SPECIES), y=counts.tolist(), text=counts.tolist(), textposition='outside',
                    cliponaxis=False, marker_color=['#159895', '#5876ae', '#b48748'])
        fig.update_yaxes(range=[0, max(1, int(counts.max()) * 1.25)])
    fig.update_layout(title={'text': 'Počet vyfiltrovaných kvetov podľa druhu', 'font': {'size': 16}},
                      xaxis_title='Druh', yaxis_title='Počet kvetov', template='plotly_white',
                      margin={'l': 45, 'r': 20, 't': 50, 'b': 45}, font={'family': 'Arial'},
                      showlegend=False, bargap=0.5)
    fig.update_yaxes(dtick=10 if df is not None and len(df) > 30 else 1)
    return fig


def register_callbacks(app):
    slider_outputs = [Output(c, p) for c in FEATURES for p in ('min', 'max', 'value', 'disabled', 'marks')]

    @app.callback(Output('load-status', 'children'), *slider_outputs,
                  Input('load-button', 'n_clicks'), State('page-key', 'children'),
                  prevent_initial_call=True,
                  running=[(Output('load-button', 'disabled'), True, False)])
    def load_data(_clicks, page_key):
        try:
            df = load_iris_data()
            set_data(page_key, df)
        except Exception:
            clear_data(page_key)
            return ('Načítanie zlyhalo. Skontrolujte internet a skúste znova.',
                    *[v for _ in FEATURES for v in (0, 1, [0, 1], True, {})])
        values = []
        for column in FEATURES:
            low, high = float(df[column].min()), float(df[column].max())
            values.extend([low, high, [low, high], False, {f'{low:g}': str(low), f'{high:g}': str(high)}])
        return ('Dáta boli načítané.', *values)

    @app.callback(Output('total-count', 'children'), Output('filtered-count', 'children'),
                  Output('species-chart', 'figure'), Output('iris-table', 'data'),
                  Output('iris-table', 'page_current'), Output('result-message', 'children'),
                  *[Output(f'{c}-range', 'children') for c in FEATURES],
                  *[Input(c, 'value') for c in FEATURES], Input('load-status', 'children'),
                  State('page-key', 'children'))
    def update_results(*args):
        ranges, page_key = args[:4], args[-1]
        df = get_data(page_key)
        if df.empty:
            return ('0', '0', make_figure(), [], 0, 'Najskôr načítajte dataset.', *['—'] * 4)
        filtered = filter_data(df, ranges)
        message = ('Žiadny kvet nevyhovuje zvoleným rozsahom.' if filtered.empty
                   else f'Zobrazených {len(filtered)} z {len(df)} kvetov ({len(filtered) / len(df):.0%}).')
        return (str(len(df)), str(len(filtered)), make_figure(filtered),
                filtered.to_dict('records'), 0, message,
                *[f'{low:.1f} – {high:.1f} cm' for low, high in ranges])

    @app.callback(Output('page-info', 'children'), Input('iris-table', 'page_current'),
                  Input('iris-table', 'data'))
    def update_page(page, rows):
        pages = ceil(len(rows) / 10)
        return f'{min((page or 0) + 1, pages)} / {pages}' if pages else '0 / 0'
