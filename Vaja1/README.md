
# Vaja1
Namen vaje je priprava razvojnega okolja, spoznavanje z osnovami Git-a ter priprava osnonve strukture web aplikacije, ki jo bomo razvijali tekom vaj.
- Pyenv
- Requirements.txt
- Github
- Ogrodje Items aplikacije

# Pyenv

`pyenv` je orodje, ki ti pomaga **upravljati več verzij Pythona** na tvojem računalniku.
##  Zakaj uporabljati `pyenv`?

### 1. **Delo z različnimi projekti**
Različni projekti pogosto zahtevajo različne verzije Pythona. Eden morda uporablja Python 3.8, drug pa 3.12. S `pyenv` lahko vsakemu projektu določiš svojo verzijo.

### 2. **Testiranje na različnih verzijah**
Če razvijaš knjižnico ali orodje, lahko preveriš, kako deluje na različnih verzijah Pythona.

### 3. **Izogibanje sistemskemu Pythonu**
Na Linux/macOS sistemih imaš že nameščen "sistemski" Python, ki ga uporablja tudi operacijski sistem. Spreminjanje te verzije je tvegano — `pyenv` ti omogoča, da namestiš in uporabljaš druge verzije brez vpliva na sistem.

## 🛠️ Osnovni ukazi
```bash
pyenv install <verzija>         # Namesti Python 3.11.4
pyenv global <verzija>          # Uporabi to verzijo globalno
pyenv local <verzija>           # Uporabi to verzijo v trenutnem projektu (ustvari .python-version datoteko)
pyenv -m venv venv              # Ustvarimo virtualno okolje v direktoriju
pyenv source venv/bin/activate  # Zaženemo virtualno python okolje
pyenc deactivate                # Izključimo virtualno python okolje
```

# Requirements.txt
requirements.txt je tekstovna datoteka, ki v Python projektih seznamuje vse potrebne knjižnice (pakete), ki jih projekt potrebuje za pravilno delovanje. Namesto ročne inštalacije vsakega paketa posebej, lahko vse pakete inštaliramo v enem koraku z uporabo requirements.txt datoteke. Na ta način lahko tudi drugi razvijalci reproducirajo vaš projekt brez napak zaradi manjkajočih odvisnosti.
## Primer requirements.txt
``` txt
flask==2.3.2
requests>=2.31.0
pandas~=2.2
numpy
```
## Inštalacija projektov iz requirements.txt
``` bash
pip install -r requirements.txx # Namestitev vseh knjižnic znotraj datoteke
```


