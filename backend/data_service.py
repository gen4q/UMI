"""Načítanie, kontrola a filtrovanie dát; žiadne sťahovanie pri importe."""
from io import BytesIO
import ssl
import certifi
from time import monotonic
from threading import RLock
from urllib.request import urlopen

import pandas as pd

IRIS_URL = 'https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv'
FEATURES = ('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
COLUMNS = (*FEATURES, 'species')
SPECIES = ('setosa', 'versicolor', 'virginica')
# Každé otvorenie stránky má vlastný kľúč. DataFrame zostáva iba na serveri.
_frames = {}
_lock = RLock()
TTL = 24 * 60 * 60


def load_iris_data(url=IRIS_URL):
    with urlopen(url, timeout=20, context=ssl.create_default_context(cafile=certifi.where())) as response:
        df = pd.read_csv(BytesIO(response.read()))
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError('Chýbajú stĺpce: ' + ', '.join(sorted(missing)))
    df = df.loc[:, list(COLUMNS)].copy()
    if df.empty:
        raise ValueError('Dataset je prázdny.')
    for column in FEATURES:
        df[column] = pd.to_numeric(df[column], errors='raise')
        if not df[column].map(lambda x: pd.notna(x) and float('-inf') < x < float('inf')).all():
            raise ValueError(f'Stĺpec {column} obsahuje neplatné hodnoty.')
    if not df['species'].isin(SPECIES).all():
        raise ValueError('Dataset obsahuje neznámy alebo chýbajúci druh.')
    return df


def set_data(page_key, df):
    with _lock:
        now = monotonic()
        for key, (_, stamp) in list(_frames.items()):
            if now - stamp > TTL:
                del _frames[key]
        _frames[page_key] = (df.copy(), now)


def get_data(page_key):
    with _lock:
        entry = _frames.get(page_key)
        return entry[0].copy() if entry else pd.DataFrame(columns=COLUMNS)


def clear_data(page_key):
    with _lock:
        _frames.pop(page_key, None)


def filter_data(df, ranges):
    mask = pd.Series(True, index=df.index)
    for column, (low, high) in zip(FEATURES, ranges, strict=True):
        mask &= df[column].between(low, high, inclusive='both')
    return df.loc[mask].copy()
