# FrontEnd

Trenutno lahko vse API klice testiramo z uporabo orodja Postman ali pa z orodjem **curl**. Če gradimo aplikacija, katere namen je samo vračanje podatkov, potem ne potrebujemo grafičnega vmesnika.
Ker implementiramo metode za dodajanje podatkov, je za uporabnika veliko bolj primerno da te podatke vnaša preko spletnega obrazca.
Če želimo implementirati grafični vmesnik, moramo v aplikacijo dodati sledeče elemente.
- Middleware
- "Mounting" statičnega index.html
- -Javascript za pobiranje uporabniških podatkov

---

# Zakaj potrebujemo Middleware v spletni aplikaciji?

Middleware je **vmesna programska plast**, ki se izvaja med prejemom HTTP zahtevka in pošiljanjem odgovora. Omogoča, da v aplikacijo vstavimo dodatno logiko, ki ni neposredno povezana z obdelavo posameznih endpointov.

---

### 🎯 Namen Middleware

- **Obdelava in spreminjanje zahtev in odgovorov** (npr. preverjanje avtorizacije, beleženje, obvladovanje napak)
- **Dodajanje varnostnih politik**, kot so CORS (Cross-Origin Resource Sharing)
- **Optimizacija ali transformacija podatkov**
- **Centralizirano upravljanje funkcionalnosti**, ki jih uporablja več endpointov

---

### 🛡️ Primer Middleware: CORSMiddleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
---

# Mounting index.html

V projektu bomo dodali **index.html**, ki bo vesboval obrazec za dodajanje Item ter pregled nad vsemi Itemi, ki so v podatkovni bazi.
NA konec main.py dodamo sledečo kodo.
```python
app.mount("/", StaticFiles(directory=".", html=True), name="static")
```
## Index.html

V html datoteki bomo s pomočjo Javascripta prebrali vnosna polja ter klicala ustrezen API klic glede na uporabnikovo akcijo.
Na začetku definiramo korenski API klic.
```javascript
const API_BASE = "http://localhost:8000/v1";
```

Nato za vsako API kočno točko definiramo svojo Javascript funkcijo, ki bo klicala pravilno API končno točko. Spodaj je primer za pridobivanje vseh Item, ki so v podatkovni bazi.
```javascript
  async function fetchItems() {
      const res = await fetch(`${API_BASE}/items`); # Kombiniramo korenjski API z pravilnio API končno točko
      const items = await res.json(); # Počakamo na rezultat
      const list = document.getElementById("item-list");
      list.innerHTML = "";
      items.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${item.name}</strong>: ${item.description} 
          <button onclick="deleteItem(${item.id})">Delete</button>
          <button onclick="editItem(${item.id}, '${item.name}', '${item.description}')">Edit</button>
        `;
        list.appendChild(li);
      });
    }
```


