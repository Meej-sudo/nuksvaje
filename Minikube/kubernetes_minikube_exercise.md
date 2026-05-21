# Kubernetes Basics with Minikube and kubectl

## Exercise: Deploy, Expose, Scale, and Self-Heal a Web Application

This exercise introduces the basics of Kubernetes and container orchestration using **Minikube** and **kubectl**.

You will run a local Kubernetes cluster, deploy a simple nginx web server, expose it through a Service, inspect Pod and Service networking, scale the application, delete a Pod, and observe Kubernetes self-healing.

---

## Learning Goals

By the end of this exercise, you should be able to:

- Explain what Kubernetes is used for.
- Start a local Kubernetes cluster with Minikube.
- Use `kubectl` to interact with a Kubernetes cluster.
- Create a Deployment.
- Expose an application using a Service.
- View Pod IPs and Service endpoints.
- Understand the difference between Pod IPs and Service access.
- Scale an application.
- Demonstrate Kubernetes self-healing by deleting a Pod.

---

## Theory Summary

A **container** packages an application together with everything it needs to run.

A **container orchestrator** manages containers automatically. It can start containers, restart failed containers, scale applications, distribute traffic, and manage updates.

**Kubernetes** is a container orchestration platform.

Instead of manually starting containers, you describe the desired state of your application. Kubernetes then works to make the actual state match that desired state.

Example:

```text
I want 3 copies of my web application running.
I want them exposed through a stable network address.
If one copy fails, I want it replaced automatically.
```

Kubernetes handles this for you.

---

## Important Kubernetes Concepts

### Cluster

A **cluster** is the complete Kubernetes environment.

In this exercise, Minikube creates a small local Kubernetes cluster.

---

### Node

A **Node** is a machine that runs workloads.

In Minikube, you usually have one local node called `minikube`.

---

### Pod

A **Pod** is the smallest deployable unit in Kubernetes.

A Pod usually contains one container.

Important:

```text
Kubernetes does not run containers directly.
Kubernetes runs Pods.
Pods contain containers.
```

---

### Deployment

A **Deployment** manages Pods.

It makes sure the desired number of Pod replicas are running.

For example, if a Deployment should have 3 replicas and one Pod is deleted, Kubernetes creates a replacement Pod.

---

### Service

A **Service** gives stable network access to Pods.

Pods are temporary. They can be deleted, recreated, and assigned new IP addresses.

A Service provides a stable way to reach them.

```text
Pods are replaceable.
Services provide stable access.
```

---

### kubectl

`kubectl` is the command-line tool used to communicate with Kubernetes.

You use it to create, inspect, update, and delete Kubernetes resources.

---

### Minikube

Minikube runs a local Kubernetes cluster on your computer or virtual machine.

It is useful for learning, testing, and local development.

---

## Architecture Diagram

```text
Your VM or Host
    |
    | curl http://192.168.49.2:<node-port>
    v
Minikube Node
    |
    | NodePort Service
    v
nginx Service
    |
    +--> Pod 1: 10.x.x.x:80
    +--> Pod 2: 10.x.x.x:80
    +--> Pod 3: 10.x.x.x:80
```

Important:

```text
From outside the cluster, you usually access the Service.
Inside the cluster, Pods communicate using internal Pod IPs or Service names.
```

---

# Part 1: Install Required Tools

You need:

- Docker
- Minikube
- kubectl

---

## 1.1 Install Docker

Minikube needs a container or VM driver. For this exercise, use Docker.

Check if Docker is installed:

```bash
docker version
```

If Docker is not installed, install Docker Desktop or Docker Engine for your operating system.

After installation, make sure Docker is running.

On Linux, your user may need permission to access Docker without `sudo`.

Run:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in, or run:

```bash
newgrp docker
```

Test Docker access:

```bash
docker ps
```

If this works without `sudo`, you are ready.

---

## 1.2 Install Minikube

### macOS

Using Homebrew:

```bash
brew install minikube
```

### Windows

Using winget:

```powershell
winget install Kubernetes.minikube
```

Using Chocolatey:

```powershell
choco install minikube
```

### Linux

For x86-64 Linux:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb
```

Verify Minikube:

```bash
minikube version
```

---

## 1.3 Install kubectl

### macOS

Using Homebrew:

```bash
brew install kubectl
```

or:

```bash
brew install kubernetes-cli
```

### Windows

Using winget:

```powershell
winget install -e --id Kubernetes.kubectl
```

Using Chocolatey:

```powershell
choco install kubernetes-cli
```

### Linux

Using Snap:

```bash
sudo snap install kubectl --classic
```

Verify kubectl:

```bash
kubectl version --client
```

---

# Part 2: Start the Kubernetes Cluster

Start Minikube with the Docker driver:

```bash
minikube start --driver=docker
```

Check Minikube status:

```bash
minikube status
```

Check the Kubernetes nodes:

```bash
kubectl get nodes
```

Expected output:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

Explanation:

```text
You now have a local Kubernetes cluster.
The cluster has one node called minikube.
```

---

# Part 3: Deploy nginx

Create a Deployment using the nginx image:

```bash
kubectl create deployment nginx-demo --image=nginx
```

Check the Deployment:

```bash
kubectl get deployments
```

Check the Pods:

```bash
kubectl get pods
```

Expected output:

```text
NAME                          READY   STATUS    RESTARTS   AGE
nginx-demo-xxxxxxxxxx-xxxxx    1/1     Running   0          ...
```

Explanation:

```text
The Deployment created a Pod.
The Pod is running the nginx container.
```

---

# Part 4: Inspect the Pod

Show more information about the Pod:

```bash
kubectl get pods -o wide
```

Example output:

```text
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE
nginx-demo-xxxxxxxxxx-abcde    1/1     Running   0          1m    10.244.0.5   minikube
```

The `IP` column shows the internal Pod IP.

Describe the Pod:

```bash
kubectl describe pod <pod-name>
```

Example:

```bash
kubectl describe pod nginx-demo-xxxxxxxxxx-abcde
```

View logs:

```bash
kubectl logs <pod-name>
```

For nginx, logs may be empty until the application receives traffic.

---

# Part 5: Expose nginx with a Service

The Pod is running, but it is not yet easily reachable from outside the cluster.

Expose the Deployment as a NodePort Service:

```bash
kubectl expose deployment nginx-demo --type=NodePort --port=80
```

Check Services:

```bash
kubectl get services
```

or:

```bash
kubectl get svc
```

Example output:

```text
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        ...
nginx-demo   NodePort    10.104.25.132   <none>        80:30847/TCP   ...
```

Explanation:

```text
The Service gives stable access to the nginx Pods.
The NodePort exposes the Service through the Minikube node.
```

Get the Minikube Service URL:

```bash
minikube service nginx-demo --url
```

Example output:

```text
http://192.168.49.2:30847
```

Open the URL in a browser or use `curl`:

```bash
curl http://192.168.49.2:30847
```

You should see the nginx welcome page HTML.

---

# Part 6: Understand Pod IPs vs Service Access

Check Pod IPs:

```bash
kubectl get pods -o wide
```

You may see Pod IPs like:

```text
10.244.0.5
10.244.0.6
10.244.0.7
```

These are internal Kubernetes Pod IPs.

From your VM or host shell, the Service URL may work:

```bash
curl http://192.168.49.2:30847
```

But direct Pod IP access may not work:

```bash
curl http://10.244.0.5
```

This is expected with Minikube and the Docker driver.

Explanation:

```text
192.168.49.2 is the Minikube node IP.
30847 is the NodePort exposed by the Service.

10.x.x.x addresses are internal Pod network addresses.
They are usually reachable from inside the cluster, not necessarily from the outer VM or host shell.
```

---

## 6.1 Curl Pods from inside Minikube

Enter the Minikube node:

```bash
minikube ssh
```

Then curl a Pod IP:

```bash
curl http://<pod-ip>
```

Example:

```bash
curl http://10.244.0.5
```

Exit Minikube:

```bash
exit
```

Explanation:

```text
Inside the Minikube node, the internal Pod network is reachable.
Outside the cluster, we normally access the application through the Service.
```

---

# Part 7: Scale the Application

Scale the Deployment to 3 replicas:

```bash
kubectl scale deployment nginx-demo --replicas=3
```

Check the Pods:

```bash
kubectl get pods -o wide
```

Expected result:

```text
There should now be 3 nginx Pods.
```

Check the Deployment:

```bash
kubectl get deployment nginx-demo
```

Explanation:

```text
We changed the desired state from 1 replica to 3 replicas.
Kubernetes created additional Pods to match the desired state.
```

---

# Part 8: View Service Endpoints

A Service forwards traffic to Pods.

Show the Service details:

```bash
kubectl describe svc nginx-demo
```

Look for the `Endpoints` field:

```text
Endpoints: 10.244.0.5:80,10.244.0.6:80,10.244.0.7:80
```

You can also run:

```bash
kubectl get endpoints nginx-demo
```

or:

```bash
kubectl get ep nginx-demo
```

Explanation:

```text
The Service has one stable access point.
The Endpoints are the current Pod IPs behind that Service.
```

Important:

```text
Service address stays stable.
Pod IPs can change.
```

---

# Part 9: Demonstrate Self-Healing

Open two terminals.

---

## Terminal 1: Continuously Call the Service

Get the Service URL:

```bash
minikube service nginx-demo --url
```

Example:

```text
http://192.168.49.2:30847
```

Run a loop:

```bash
while true; do curl -s http://192.168.49.2:30847 | head -n 5; echo; sleep 2; done
```

This continuously checks whether the Service is working.

---

## Terminal 2: Delete a Pod

List Pods:

```bash
kubectl get pods
```

Delete one Pod:

```bash
kubectl delete pod <pod-name>
```

Example:

```bash
kubectl delete pod nginx-demo-xxxxxxxxxx-abcde
```

Watch the Pods:

```bash
kubectl get pods -w
```

You should see one Pod terminating and a new one being created:

```text
nginx-demo-xxxxxxxxxx-abcde   Terminating
nginx-demo-yyyyyyyyyy-fghij   ContainerCreating
nginx-demo-yyyyyyyyyy-fghij   Running
```

Meanwhile, Terminal 1 should continue receiving responses from the Service.

Explanation:

```text
The Service keeps working because it sends traffic to the remaining healthy Pods.
The Deployment notices that one Pod disappeared.
Because the desired state is 3 replicas, Kubernetes creates a replacement Pod.
```

---

# Part 10: Optional Better Demo - Show Which Pod Answers

The nginx page looks the same from every Pod.

To clearly show that different Pods answer behind one Service, use a demo image that returns the Pod hostname.

Create the Deployment:

```bash
kubectl create deployment hostname-demo \
  --image=registry.k8s.io/e2e-test-images/agnhost:2.39 \
  -- /agnhost netexec --http-port=8080
```

Scale it:

```bash
kubectl scale deployment hostname-demo --replicas=3
```

Expose it:

```bash
kubectl expose deployment hostname-demo --type=NodePort --port=8080
```

Get the Service URL:

```bash
minikube service hostname-demo --url
```

Call the `/hostname` endpoint repeatedly:

```bash
for i in {1..10}; do curl -s $(minikube service hostname-demo --url)/hostname; echo; done
```

Example output:

```text
hostname-demo-xxxxxxxxxx-abcde
hostname-demo-xxxxxxxxxx-fghij
hostname-demo-xxxxxxxxxx-klmno
hostname-demo-xxxxxxxxxx-abcde
```

Explanation:

```text
The Service forwards requests to different Pods.
Each Pod answers with its own hostname.
```

Delete one hostname-demo Pod:

```bash
kubectl delete pod <hostname-demo-pod-name>
```

Run the curl loop again:

```bash
for i in {1..10}; do curl -s $(minikube service hostname-demo --url)/hostname; echo; done
```

You should see the deleted Pod disappear from the responses, and a new Pod eventually appear.

---

# Part 11: Optional YAML Version

Kubernetes resources are commonly managed using YAML files.

Create a file called:

```bash
nginx-demo.yaml
```

Add:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-yaml-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-yaml-demo
  template:
    metadata:
      labels:
        app: nginx-yaml-demo
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-yaml-demo
spec:
  type: NodePort
  selector:
    app: nginx-yaml-demo
  ports:
  - port: 80
    targetPort: 80
```

Apply it:

```bash
kubectl apply -f nginx-demo.yaml
```

Check resources:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Open it:

```bash
minikube service nginx-yaml-demo
```

Delete it:

```bash
kubectl delete -f nginx-demo.yaml
```

Explanation:

```text
This is the declarative approach.
We describe the desired state in a YAML file.
Kubernetes applies that desired state.
```

---

# Part 12: Clean Up

Delete the nginx Service and Deployment:

```bash
kubectl delete service nginx-demo
kubectl delete deployment nginx-demo
```

Delete the optional hostname demo if you created it:

```bash
kubectl delete service hostname-demo
kubectl delete deployment hostname-demo
```

Stop Minikube:

```bash
minikube stop
```

Optional: delete the local Minikube cluster completely:

```bash
minikube delete
```

Explanation:

```text
minikube stop pauses the local cluster.
minikube delete removes the local cluster.
```

---

# Troubleshooting

## Docker permission error on Linux

Error example:

```text
denied while trying to connect to the docker API
```

Fix:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in, or run:

```bash
newgrp docker
```

Test:

```bash
docker ps
```

Then start Minikube without `sudo`:

```bash
minikube start --driver=docker
```

Do not run:

```bash
sudo minikube start --driver=docker
```

The Docker driver should not be used with root privileges.

---

## Pod IPs are not reachable from my VM or host

This can happen with Minikube using the Docker driver.

Use the Service URL instead:

```bash
minikube service nginx-demo --url
```

Then:

```bash
curl http://<service-url>
```

To test Pod IPs directly, enter the Minikube node:

```bash
minikube ssh
```

Then:

```bash
curl http://<pod-ip>
```

---

## Service works, but Pod IPs do not

This is normal.

Explanation:

```text
The Service is exposed through the Minikube node IP and NodePort.
The Pod IPs belong to the internal Kubernetes network.
```

---

# Student Questions

Answer the following:

1. What is the difference between a Pod and a Deployment?
2. Why do we need a Service?
3. What happens when a Pod is deleted?
4. Why are Pod IPs not a stable way to access an application?
5. What is the difference between a Pod IP and a NodePort Service URL?
6. What does Kubernetes mean by desired state?
7. Why is this considered orchestration?

---

# Key Takeaways

```text
Minikube runs Kubernetes locally.
kubectl controls Kubernetes.
A Deployment manages Pods.
A Service exposes Pods.
Pod IPs can change.
Services provide stable access.
Kubernetes can self-heal by replacing deleted or failed Pods.
```
