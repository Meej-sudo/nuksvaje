# Vaja 2

V drugi vajo bomo dopolnili preostale CRUD metode iz prve vaje, dodali bomo verzioniranje API klicev ter iplementirali preprost Frontend za vizualizacijo podatkov.

- Verzioniranje API klicev
- Implementacija CRUD
- Implementacija FrontEnd-a

---

#  Zakaj verzionirati API klice?

Verzioniranje API-jev pomeni, da določimo različico (npr. `v1`, `v2`, ...) našega API-ja. To je ključnega pomena pri razvoju, vzdrževanju in nadgradnji aplikacij, ki uporabljajo naš API.
To hkrati tudi pomeni, da se spremeni pot do določenega vira. Če smo v prvi vaji uporabljali pot /items/ bomo sedaj uporabljaji pot /verzija/items

---

## ✅ Prednosti verzioniranja API-jev

### 1. 🔒 Stabilnost za obstoječe uporabnike
Ko naredimo spremembe (npr. odstranimo ali preimenujemo polja), lahko obstoječe aplikacije še vedno uporabljajo staro različico API-ja brez prekinitev.

### 2. 🛠️ Lažje vzdrževanje in migracije
Z verzijami lahko postopoma preusmerjamo uporabnike z `v1` na `v2`, brez potrebe po takojšnjih spremembah v vseh aplikacijah.

### 3. 🚀 Hitrejši razvoj novih funkcionalnosti
Razvijalci lahko eksperimentirajo z novimi funkcijami v `v2`, medtem ko `v1` ostane nespremenjen in stabilen za produkcijo.

### 4. 🔍 Jasna dokumentacija
Vsaka verzija API-ja ima svojo dokumentacijo, kar zmanjšuje zmedo in izboljša uporabniško izkušnjo.

---

## Kako verzionirami z FastAPI knjižnico

Če želimo verzionirati z knjižnico FastAPI moramo bodisi ročno bodisi preko requirements.txt inštalirati python knjižnico **fastapi-versioning**.
```bash
pip install fastapi-versioning
```
Verzioniranje implementiramo tako, da poleg api rout-a navedemo tudi verzijo.
```python
@app.post("/items/", response_model=ItemRead)
@version(1)
```
Na koncu moramo zamenjat način kako inicializiramo svojo aplikacijo. 
```python
app = FastAPI() # Spremenimo v
app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
```
Torej bodo naši API rout-i sedaj /v1/items/


