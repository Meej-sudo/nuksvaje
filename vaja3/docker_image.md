# Docker Image

Vse docker image lahko najdemo na platformi DockerHub. Vedno sortiramo containerje po številu prenosov saj so te najbolj zaupanja vredni. DockerHub je dostopen na  https://hub.docker.com/.

## Nalaganja Docker imagov

Privzeto vaš sistem nima lokalnih docker imagov kar pomeni, da moramo poljuben image prenesti na sistem. Image lahko iščemo z ukazom ```bash docker search <ime>``` ali pa neposredno na DockerHubu. Željeni docker image nator naložimo z ukazom ```bash docker pull <ime> ```.


### Primer
```bash
docker  search nginx # Poiščemo nginx image
docker pull nginx # Naložimo nginx image lokalno
docker images # Prikažemo image
```

## Zagon containerja iz docker imaga

Ko zaženemo container z pljubnim imagom moramo povedati ime containerja ter image, ki ga bomo uporabili. Poljubno lahko potem še izpostavimo določene porte, da bo apliakcija dosegljiva na ven.
```bash
docker run -d -p 8080:80 --name webserver nginx
http://localhost:8080
```
Ustvarili smo docker image z imenom webserver, ki uporablja nginx image in je dosegljiv na portu 8080.
```bash
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                     NAMES
d2ec03d7cbb9   nginx     "/docker-entrypoint.…"   30 seconds ago   Up 29 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   webserver
```
## Nadzor containerja

Containerje lahko nato nadziramo z ukazi ```bash docker ps``` ```bash docker logs```. Pogosto želimo log datoteke tudi prekopirati v lokalno datoteko na napravi. To lahko naredimo z ukazom ```bash docker logs > ime.txt```
Conatiner lahko ustavimo, zaženemo ali ponovno zaženemo z ukazom ```bash docker stop/start/restart <ime>```

⬇️ [Dockerfile](docker_file.md)
