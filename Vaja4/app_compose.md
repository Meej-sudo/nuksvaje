# Docker Compose Aplikacije

Naša aplikacija ima trenutno samo en container, to je naš python app. Docker compose ima sledečo strukturo.
```yaml
version: "3.9"

services:
 api:
    build:
      context: .
    container_name: fastapi_api
    ports:
      - "8000:8000"
 ```
Ključna razlika v primerjavi z compose datoteke iz vaje 3, je to da image sedaj vzamemo iz DockerFile in ne neposredno iz interneta.  
Našemu projektu lahko dodamo podatkovno bazo kot container, ki se bo ustvaril ko zaženemo docker compose.
```yaml
db:
    image: postgres:14
    container_name: fastapi_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```
V drugem delu našega composa uporabimo image postres:14 da iz interneta naložimo image postgres baze.

⬇️ [Združitev compose segmentov](app_compose_2.md)
