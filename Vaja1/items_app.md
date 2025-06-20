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


# Web routi

Za postavite spletnega strežnika bomo uporabili knjižnico **FastAPI**. Posamezno CRUD metodo bomo implementerali kot ločen API klic z ustrezno HTTP metodo.
Vsak API klic je sestavljen iz http metode, poti, odgovora. Nov API klic definiramo z dekoratorjem **@**.



## Primer API klica
```python
@app.post("/items/", response_model=ItemRead) # Celotna pot se torej glasi http://127.0.0.1/items
@app.get("/items/{item_id}", response_model=ItemRead) # Celotna pot se glasi http://127.0.0.1/items/<Item, ki se nahaj v db>
```

Vsak API klic mora biti prav tako opremljen z funkcijo, ki se kliče ko uporabnik obišče API pot.



## Implementacija CRUD metod

CRUD je kratica za implementacijo osnovnih funkcij ustvarjanja (Create), branja (Read), posodabljanja (Update) ter brisanja (Delete) spletnih virov. 
```python
@app.post("/items/", response_model=ItemRead) # Http metoda POST
@app.get("/items/", response_model=List[ItemRead]) # Http metoda GET
@app.put("/items/{item_id}", response_model=ItemRead) # Http metoda UPDATE
@app.delete("/items/{item_id}") # Http metoda DELETE
```
V praksi lahko večino CRUD funkcijo implementiramo samo z funkcijo POST, saj POST omogoča pošiljanje podatkov proti spletnemu strežniku kar omogoča posodabljanje, ustvarjanje ter brisanje virov. Po standardu se mora HTTP metoda ujemati z akcijo, ki jo želimo izvesti nad virom.

---
# Podatkovna baza
Podatkovna baza se bo dinamično ustvarilo s pomočjo knjižnice sqlalchemy. Sqlaclchemy je ORM (Objec Relational Mapper) kar pomeni, da lahko ustvari več tipov podatkovnih baz. V našem primeru bomo uporabljali SQLite.
```python
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
```
---
# Shema podatkovne baze

V shemi definiramo strukturo naše podatkovne baze (tabele, polja, povezave). V našem primeru bomo imeli eno tabelo z imenom **Items**
```python
class Item(Base):
    __tablename__ = "items" ## Ime tabele

    id = Column(Integer, primary_key=True, index=True) # ID, ki služi kot unikatna vrednost za vsak zapis
    name = Column(String, nullable=False) #Ime 
    description = Column(String) # Opis
```

 ⬇️ [Github](github.md)
