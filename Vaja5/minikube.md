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
