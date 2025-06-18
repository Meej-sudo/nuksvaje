# Docker Compose
Docker Compose je posebna oblika datoteke, ki je namenjena zaganjanju več containerjev naenkrat. V direktorji ustvarimo datoteko z imenom ``` docker-compose.yaml```(lahko tudi .yml) in v njo zapišemo vse informacije o containerjih, ki jih želimo zagnati.

## Primer 
```yaml
version: '3'
services:
 web:
  image: nginx
  ports:
   - "8080:80" 
```
V tem primeru je compose datoteke ne potrebna saj zaganjamo samo en container. Compose je namenjen zaganjanu več containerjev naenkrat kjer imajo containerji lahko neko obliko soodvisnosti.
```yaml
version: '3'
services:
 web:
  image: nginx
  ports:
   - "8080:80" 
 demo:
  image: alpine
```
Zaženemo dva containerja. Prvi kot osnovo uporabi image **nginx** drugi pa **alpine**
Datoteko zaženemo z ukazom ``` docker-compose up -d```. Če želimo image najprej zgraditi potem uporabimo opcijo ``` docker-compose up --build```..
Containerje nato ugasnemo z ukazom ```docker-compose down```.
