# Iris dashboard

Aplikácia v Plotly Dash na prezeranie datasetu Iris. Po kliknutí na tlačidlo načíta dáta z internetu a umožní ich filtrovať podľa štyroch rozmerov kvetov. Počty, graf aj tabuľka zobrazujú rovnaký výsledok.

## Inštalácia a spustenie

Potrebujete Python 3.10 alebo novší a internet na inštaláciu balíkov, načítanie CSV a Bootstrap témy. V termináli otvorte priečinok projektu a spustite:

```bash
python -m pip install -r requirements.txt
python app.py
```

Vo Windows môžete balíky nainštalovať aj dvojklikom na `install_requirements.bat`. Skript používa prednostne `py -3`, inak `python`. Ak máte viac verzií Pythonu, aplikáciu spustite rovnakým príkazom ako pri inštalácii, napríklad `py -3 app.py`. Skript inštaluje iba balíky, samotný Python musí byť už nainštalovaný.

Otvorte http://127.0.0.1:8050 a kliknite na **Načítať dáta**. Pri ďalšom spustení stačí `python app.py`. Server zastavíte cez Ctrl+C.

## Používanie

Pred načítaním sú výsledky prázdne a filtre zablokované. Po načítaní sa rozsahy nastavia podľa dát. Štyrmi posuvníkmi meníte dĺžku a šírku kališného a korunného lístka v centimetroch.

Všetky rozsahy platia naraz (AND), vrátane krajných hodnôt. Výsledky sa menia už počas posúvania. Graf ukazuje počty troch druhov a tabuľka všetkých päť stĺpcov, po 10 riadkov na strane. Stĺpce sa dajú triediť; zmena filtra vráti tabuľku na prvú stranu.

Na vyskúšanie nastavte **Petal Length** od 1.0 do 2.0 cm: zostane 50 kvetov setosa. Ak nevyhovuje žiadny kvet, zobrazí sa nula a prázdna tabuľka. Ďalšie kliknutie na **Načítať dáta** znovu stiahne CSV a obnoví rozsahy. Po obnovení stránky treba dáta načítať znova.

## Súbory projektu

- `app.py` vytvára aplikáciu, zapína Dash Pages a pripája Bootstrap tému FLATLY.
- `pages/home.py` obsahuje panel, tlačidlo, filtre, graf a tabuľku.
- `backend/data_service.py` načítava, kontroluje, uchováva a filtruje dáta.
- `callbacks/iris_callbacks.py` obsahuje callbacky a tvorbu grafu.
- `assets/styles.css` dopĺňa vzhľad stránky.
- `requirements.txt` uvádza potrebné balíky; `install_requirements.bat` ich nainštaluje vo Windows.

## Ako to funguje

`load_data` reaguje na tlačidlo, načíta CSV a nastaví filtre. Pri štarte sa nespúšťa (`prevent_initial_call=True`); počas sťahovania blokuje tlačidlo cez `running`. Pri chybe zobrazí správu a umožní nový pokus.

`update_results` reaguje na štyri filtre a stav načítania. Dáta vyfiltruje raz a z rovnakého výsledku aktualizuje počty, graf, tabuľku aj textové rozsahy.

`update_page` pri zmene strany alebo dát tabuľky aktualizuje údaj o stránkovaní, napríklad 1 / 15.

DataFrame zostáva v pamäti servera pod identifikátorom otvorenej stránky. Skrytý prvok `page-key` obsahuje iba tento identifikátor; `dcc.Store` sa nepoužíva. Aplikácia je určená na lokálne spustenie s jedným serverovým procesom.

Zdroj dát: [Iris CSV](https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv).
