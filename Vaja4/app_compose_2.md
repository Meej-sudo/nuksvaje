# Združitev delov composa

Če želimo, da se naša aplikacija uspešno zažene z docker composom, moramo združiti in nadgraditi oba dela composa iz prejšnjega koraka.
Celoten compose bo sedaj izgledal sledeče.
```yaml
version: "3.9"

services:
 api:
    build:
      context: . # Za kontekst vzamemo trenuten direktorij
    container_name: fastapi_api # Container poimenujemo
    ports:
      - "8000:8000" # Izpostavimo port 8000
    depends_on:
      - db # Odvisnost od containerja db
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/mydb # Okoljska spremenljivka za dostop do postgres baze

    db:
    image: postgres:14 # Image za postavitev postgres baze
    container_name: fastapi_db # Ime containerja
    environment: # Podatki za dostop do postgres baze
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data # Medij za trajno shranjevanje podatkov
    ports:
      - "5432:5432" # Izpostavljen port

volumes:
  postgres_data:
```
V naš prvi servis fastapi_api smo dodali ```dependency```. Ta dependency poskrbi, da se mora prvo zagnati container fastapi_db in šele nato se zažene container fastapi_api. Tak vrstni red je pomemben saj naša aplikacija piše v podatkovno bazo. V kolikor se podatkovna baza ne postavi v containerju je nesmiselno, da bi se postavila naša aplikacija saj nima dostopa do baze. Vsi naši api endpointi komunicirajo z podatkovno bazo.
Poleg tega smo dodali tudi okoljso spremenljivko ```DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/mydb```, ki poveže aplikacijo z postgres bazo.
