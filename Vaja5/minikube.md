# Minikube
Na vajah bomo uporabljali "Kubernetes", ki je namenjen lokalnemu razvoju in testiranju. Različica, ki jo bomo uporabljali se imenuje Minikube. Ta različica ni primerna za produkcijsko uporabo vendar je primerna za demonstracijo konceptov orkestracije. Minikube deluje samo na enemu nodu.

## Kaj je Minikube?

**Minikube** je orodje, ki omogoča zagon enovoziščne Kubernetes gruče (cluster) **lokalno** na tvojem računalniku. Namenjen je predvsem učenju, testiranju in razvoju Kubernetes aplikacij.

Deluje v virtualnem okolju (npr. VirtualBox, Docker, Hyper-V) in ustvari en **Node**, ki vključuje vse glavne komponente Kubernetes strežnika.

---

## Glavne značilnosti Minikube:

- Zagon Kubernetes gruče lokalno (brez potrebe po oblačni infrastrukturi)
- Hiter preizkus YAML konfiguracij in Helm chartov
- Podpora za **ingress**, **dashboard**, **addons** ipd.
- Podpira več **virtualizacijskih gonilnikov** (VM, Docker)

---

## Namestitev Minikube

```bash
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/$(uname | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```
# Kubectl

Minikube prestavlja kubernetes strežnik, za dostop do strežnika pa potrebujemo dodatno orodje. Uradno orodje za delo z kubernetesom se imenuje **kubectl*. 
## Kaj je kubectl?

**kubectl** je uradno orodje ukazne vrstice za komunikacijo z **Kubernetes API strežnikom**. Omogoča upravljanje Kubernetes virov, kot so podi, storitve, deploymenti, konfiguracije in drugo.

Z kubectl lahko:
- ustvarjaš, bereš, posodabljaš in brišeš objekte v gruči (CRUD operacije),
- spremljaš stanje sistema,
- izvajaš diagnostiko,
- nadziraš dnevniške zapise (*logs*),
- vstopaš v vsebnike (*exec*),
- in še veliko več.

---

## Kako kubectl deluje?

kubectl komunicira s **Kubernetes API strežnikom** v tvoji gruči preko datoteke `kubeconfig` (privzeto: `~/.kube/config`), kjer so shranjeni podatki o gruči in uporabniku.

---

## Osnovna sintaksa

```bash
kubectl [ukaz] [vrsta-objekta] [ime-objekta] [dodatne-možnosti]
```
---

## Kubectl ukazi
```bash
	
kubectl get pods	# Prikaže seznam vseh podov
kubectl get services	# Prikaže seznam storitev
kubectl describe pod <ime>	# Podrobnosti o posameznem podu
kubectl logs <ime-poda>	# Prikaže dnevnik vsebnika
kubectl exec -it <ime-poda> -- bash	# Dostop do terminala v podu
kubectl apply -f file.yaml	# Ustvari ali posodobi objekte iz YAML datoteke
kubectl delete -f file.yaml	# Izbriše objekte iz YAML datoteke
kubectl create deployment <ime> --image=<slika>	# Ustvari deployment prek ukazne vrstice
kubectl scale deployment <ime> --replicas=3	# Skalira deployment na 3 ponovitve
```
⬇️ [Deploy podov](deploy.md)
