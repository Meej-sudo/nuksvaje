# Osnovni Docker ukazi

Uspešno nameščeno docker okolje lahko preverimo z ukazom ```bash docker --version ``` ali pa ```bash docker info```. Vsi docker ukazi zahtevajo višji privilegih tako, da uporabljajte ukaz **sudo** pred vsakim docker ukazom.

## Prvi Docker container
Prvi docker container lahko poženemo z ukazom docker run hello-world. To je testni docker image, ki nam bo vrnil "Hello World" ter opisal korake, ki jihj e izvedel za zagon tega docker containerja.
```bash
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
Stanje docker container lahko preverimo z ukazom ```bash docker container list``` ali pa ```bash docker container list -a```, ki prikaže containerje z vsemi statusi.
```bash
CONTAINER ID   IMAGE                                 COMMAND                  CREATED         STATUS                     PORTS     NAMES
8dab64c5a1c9   hello-world                           "/hello"                 2 minutes ago   Exited (0) 2 minutes ago             relaxed_hermann
```
Vsak docker container je sestavljen iz ID, imena imaga, ukaza ki se je izvedel ko se je container postavil, čas stvarjenja, status, odprti porti ter ime (privzeto se generirajo naključna imena).
Z ukazom ```bash docker inspect <ime containerja>``` si lahko ogledamo detajle container. Z ```bash docker inspect image <id imaga>``` pa si lahko ogledamo detajle imaga.

⬇️ [Namestitev Docker Imaga](docker_image.md)
