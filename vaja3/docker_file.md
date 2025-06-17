# Dockerfile

`Dockerfile` je besedilna datoteka, ki vsebuje niz ukazov in navodil, ki jih Docker uporablja za sestavo slike (*image*). Slika je osnova za zagon vsebnika (*container*).

## Osnovna struktura Dockerfile:
Dockerfile običajno vključuje naslednje ukaze:
- `FROM` – določa osnovno sliko, npr. `python:3.11`
- `COPY` – kopira datoteke iz lokalnega sistema v sliko
- `RUN` – izvaja ukaze med gradnjo slike (npr. nameščanje odvisnosti)
- `CMD` ali `ENTRYPOINT` – določa ukaz, ki se izvede ob zagonu vsebnika

# Primer
V direktorji ustvarimo datoteko in jo poimenujemo **Dockerfile**. V to datoteko bomo zapisali minimalno število ukazov, ki jih potrebujemo za zagon containerja.
```dockerfile
#Dockerfile
FROM alpine # Osnova
CMD ["echo", "Hello from my custom Docker image!"] # Izveden ukaz
```
Container moramo nato ustvariti z ```bash docker build -t <ime>``` ter ga zaženemo z ```bash docker run <ime>```.

Do containerja lahko dostop tudi z ukazom ```docker exec -it <ime> /bin/bash```
