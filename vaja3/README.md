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
```bash
sudo apt-get update

sudo apt-get -y install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common

sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" |  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable docker
```

## Namestitev Docker-Composa

