# Ideja Aplikacije

Name vaj je izdelati preprosto Items spletno aplikacije preko katere bomo spoznali koncepte, ki jih boste kasneje implementirali v lastne projekte
Na prvi laboratorijski vaji bomo postavili ogrodje te aplikacije in se spoznali z naslednjimi elementi.
- Osnove pythona
- Struktura Web aplikacije
- Web "Routi"
- Implementacija CRUD metod

Vsa koda za projekt je v ločenih .py mapah.

# Struktura aplikacije

Aplikacija bo narejena iz treh ločenih .py datotek
- main.py # Vsebuje programsko logiko
- database.py # Inicializira podatkovno bazo
- models.py # Opisuje strukturo podatkovne baze

---
# Web routi

Za postavite spletnega strežnika bomo uporabili knjižnico **FastAPI**. Posamezno CRUD metodo bomo implementerali kot ločen API klic z ustrezno HTTP metodo.
Vsak API klic je sestavljen iz http metode, poti, odgovora. Nov API klic definiramo z dekoratorjem **@**.
---

## Primer API klica
```python
@app.post("/items/", response_model=ItemRead) # Celotna pot se torej glasi http://127.0.0.1/items
@app.get("/items/{item_id}", response_model=ItemRead) # Celotna pot se glasi http://127.0.0.1/items/<Item, ki se nahaj v db>
```

Vsak API klic mora biti pravtako opremljen z funkcijo, ki se kliče ko uporabnik obišče API pot.
---

## Implementacija CRUD metod

CRUD je kratica za implementacijo osnovnih funkcij ustvarjanja (Create), branja (Read), posodabljanja (Update) ter brisanja (Delete) spletnih virov. 
