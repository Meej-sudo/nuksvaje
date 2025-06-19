# Priprava deployment datotke

V prvem koraku moramo zagnati Minikube storitev z ukazom ```minkube start```. Kubernetes deluje na principu deployment datotek iz katerih jemlje informacije o zgradbi deploymenta, ki ga želimo izvesti. Deployment je .yaml datoteka. Za vajo bomo vzeli nginx strežnike in jih postavili kot cluster.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2 # Naredimo dve replike containerja
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine # Vzamemo nginx image
        ports:
        - containerPort: 80 # Storitev bo tekla na portu 80
```
