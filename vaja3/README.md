# Vaja 3

Na vaji bomo predelali osnove dockerja in mikrostoritev. 

## Mikrostoritve

Mikrostoritve so arhitekturni vzorec, kjer je aplikacija razdeljena na manjše, neodvisne storitve. Vsaka storitev je odgovorna za točno določeno funkcionalnost in komunicira z drugimi prek API-jev, najpogosteje REST ali gRPC.

### Ključne prednosti:
- **Neodvisnost**: Mikrostoritve lahko razvijamo, nameščamo in skaliramo ločeno.
- **Boljša razširljivost**: Sistem je lažje prilagoditi rastočim potrebam.
- **Tehnološka raznolikost**: Vsaka storitev je lahko napisana v drugem programskem jeziku ali uporablja drugo bazo podatkov.

### Izzivi:
- **Kompleksnost**: Upravljanje porazdeljenega sistema zahteva ustrezno infrastrukturo.
- **Komunikacija**: Potrebna je skrbna zasnova vmesnikov in mehanizmov za obravnavo napak.

### Tehnologije
- **Docker**
- **Linux Container**

---

# Docker
Docker je odprtokodna platforma, ki omogoča avtomatizirano ustvarjanje, razmestitev in zagon aplikacij v vsebnikih (*containers*). Vsebnik je lahek, prenosljiv paket, ki vsebuje vse, kar aplikacija potrebuje za delovanje – kodo, knjižnice, odvisnosti in konfiguracije.

### Prednosti Dockerja:
- **Prenosljivost**: Aplikacije delujejo enako v vseh okoljih (razvoj, test, produkcija).
- **Izolacija**: Vsak vsebnik deluje ločeno, kar zmanjšuje konflikte med komponentami.
- **Hitrost**: Vsebniško okolje se zažene bistveno hitreje kot tradicionalni virtualni strežniki.
- **Skalabilnost**: Docker se odlično integrira z orodji za orkestracijo, kot je Kubernetes.

## Namestitev Dockerja

Docker lahko namestimo na poljubno platformo (Windows, Linux, Mac). Navodila za namestitev dockerja so v **docker** datoteki na githubu.


## Namestitev Docker-Composa

