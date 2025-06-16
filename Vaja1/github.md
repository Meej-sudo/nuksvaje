#  Uvod v Git in GitHub

##  Kaj je Git?

**Git** je porazdeljen sistem za nadzor različic (angl. *version control system*), ki omogoča:

- Sledenje spremembam v izvorni kodi ali dokumentih
- Shranjevanje zgodovine razvoja
- Delo v ekipah (več razvijalcev hkrati)
- Povrnitev starejših verzij datotek

Git deluje **lokalno**, kar pomeni, da vse spremembe najprej narediš na svojem računalniku.

---

##  Kaj je GitHub?

**GitHub** je spletna storitev, ki omogoča:

- Shranjevanje Git repozitorijev v oblaku
- Sodelovanje več oseb na istem projektu
- Upravljanje z različicami kode
- Sledenje napakam (issues), predlogom (pull requests), dokumentaciji itd.

👉 GitHub je zgrajen na podlagi Gita – Git je orodje, GitHub pa spletna platforma.

---

## ⚙️ Osnovni Git ukazi

```bash
git init               # Ustvari nov lokalni git repozitorij
git config --global user.email <email> # Dodamo email, ki ga bomo uporabili za push
git status             # Prikaže trenutno stanje (spremembe)
git add ime_datoteke   # Doda datoteko v "staging area"
git add .              # Doda vse elemente v trenutnem dirketorji v "staging area""
git commit -m "Opis"   # Shrani spremembe z opisom
git log                # Prikaže zgodovino commitov
```
---
## ⚙️ Povezava z Githubom
```bash
git remote add origin https://github.com/your-username/your-repo.git # Push preko protokola https
git remote set-url origin git@github.com:your-username/your-repo.git # Push preko protokola ssh
git push -u origin main # Posredovanje sprememb na repozitorij na Github platformi
git pull # Prevzem spremebn iz repozitorija na Githubu
```
