# Vaja 5

Namen vaje je predstaviti osnove orkestracije containerjev. 

## Kaj je orkestracija vsebnikov?

Orkestracija vsebnikov se nanaša na avtomatizirano upravljanje:
- zagona in zaustavljanja vsebnikov
- razporejanja po strežnikih
- skaliranja aplikacij
- obnavljanja v primeru napak
- nadgradnje aplikacij brez prekinitve delovanja

Najbolj razširjeno orodje za orkestracijo je **Kubernetes**.

---

## Kaj je Kubernetes?

**Kubernetes** (K8s) je odprtokodni sistem za orkestracijo vsebnikov, ki omogoča:
- avtomatsko razporejanje in upravljanje vsebnikov v gruči strežnikov
- samoobnavljanje storitev
- horizontalno skaliranje
- nadgradnje brez izpadov (rolling updates)

---

## Ključne komponente v Kubernetesu

| Komponenta       | Opis |
|------------------|------|
| **Pod**          | Najmanjša enota v Kubernetesu, ki lahko vsebuje enega ali več vsebnikov. |
| **Deployment**   | Upravljalec za ustvarjanje in nadgradnjo podov. |
| **Service**      | Omogoča dostop do podov prek stalnega IP-naslova ali DNS imena. |
| **Node**         | Fizični ali virtualni strežnik v gruči. |
| **Cluster**      | Skupina node-ov, ki jih upravlja Kubernetes. |
| **Ingress**      | Usmerjanje zunanjega prometa do storitev znotraj gruče. |
| **ConfigMap & Secret** | Upravljanje konfiguracij in občutljivih podatkov. |
| **Volume**       | Shranjevanje podatkov, ki preživijo ponovno zagon poda. |

---

## Pomembne funkcionalnosti

- **Samozdravljenje**: če se pod sesuje, ga Kubernetes samodejno ponovno zažene.
- **Avtomatsko skaliranje**: prilagodi število replik glede na obremenitev (CPU, RAM).
- **Rolling updates**: nadgradi aplikacijo brez izpadov.
- **Load balancing**: razporeja promet med več replikami storitve.
- **Declarative config**: stanje sistema je opisano z YAML datotekami.

⬇️ [Minikube in kubectl](minikube.md)
