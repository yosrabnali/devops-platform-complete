# DevOps Platform Complete

A production-grade DevOps platform combining CI/CD, GitOps, Kubernetes orchestration, autoscaling, and full observability.

---

## Architecture
Developer → git push → GitHub Actions (4 jobs) → Docker Hub

│

ArgoCD detects change

│

Kubernetes cluster

├── Flask API x3 pods

├── Redis cache

├── HPA autoscaling

└── Prometheus + Grafana

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + Flask | REST API with Prometheus metrics |
| Docker | Containerization |
| Kubernetes (Kind) | Container orchestration |
| ArgoCD | GitOps continuous deployment |
| GitHub Actions | CI/CD pipeline (4 jobs) |
| Trivy | Security vulnerability scanning |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| HPA | Horizontal pod autoscaling |
| Helm | Kubernetes package manager |
| Redis | In-memory cache |

---

## Project Structure
devops-platform-complete/

├── app/

│   └── main.py                    # Flask API + Prometheus metrics

├── tests/

│   └── test_main.py               # 4 automated tests

├── k8s/

│   ├── deployment.yml             # 3 replicas + probes + resources

│   ├── service.yml                # ClusterIP service

│   ├── redis-deployment.yml       # Redis cache

│   ├── hpa.yml                    # Autoscaling 2-10 pods

│   └── servicemonitor.yml        # Prometheus scraping config

├── argocd/

│   └── application.yml            # GitOps configuration

├── monitoring/

│   └── prometheus-values.yaml     # Prometheus Helm values

├── .github/

│   └── workflows/

│       └── ci-cd.yml              # 4-job CI/CD pipeline

├── Dockerfile

└── requirements.txt

---

## CI/CD Pipeline — 4 Jobs
git push

│

├── Job 1: test      → pytest 4 tests

├── Job 2: security  → Trivy vulnerability scan

├── Job 3: build     → docker build + push to Docker Hub

└── Job 4: deploy    → update image tag in k8s/deployment.yml

│

ArgoCD detects change

│

Auto-sync to Kubernetes

---

## API Endpoints

| Endpoint | Method | Response |
|----------|--------|----------|
| `/` | GET | App status + visits + pod/node info |
| `/health` | GET | Health check (used by K8s probes) |
| `/metrics` | GET | Prometheus metrics |
| `/api/users` | GET | Sample users list |

---

## Kubernetes Features

**Auto-healing** — if a pod crashes, Kubernetes recreates it automatically in under 1 second.

**Zero Downtime** — 3 replicas ensure the app stays available during updates or pod restarts.

**HPA Autoscaling** — automatically scales from 2 to 10 pods based on CPU usage (threshold: 70%).

**Liveness + Readiness Probes** — Kubernetes continuously checks `/health` to ensure pods are alive and ready.

**Resource Limits** — each pod is limited to 128Mi RAM and 200m CPU to prevent resource exhaustion.

---

## GitOps with ArgoCD

ArgoCD watches the `k8s/` directory in this repository. Any change pushed to GitHub is automatically synced to the Kubernetes cluster — no manual `kubectl apply` needed.

**Self-healing**: if someone manually modifies the cluster, ArgoCD reverts it back to match the Git state.

---

## Observability

**Prometheus** scrapes `/metrics` from Flask every 15 seconds, collecting:
- `flask_requests_total` — total HTTP requests by endpoint, method, status
- `flask_request_latency_seconds` — request latency histogram

**Grafana** visualizes these metrics in real-time dashboards.

---

## Getting Started

### Prerequisites
- Docker Desktop
- Kind
- kubectl
- Helm

### Setup

```bash
# Create cluster
kind create cluster --name devops-cluster

# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy application
kubectl apply -f k8s/

# Install monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f monitoring/prometheus-values.yaml

# Deploy ArgoCD app
kubectl apply -f argocd/application.yml
```

### Access

```bash
# App
kubectl port-forward service/flask-service 9090:80

# ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8443:443

# Grafana
kubectl port-forward service/monitoring-grafana 3000:80 -n monitoring

# Prometheus
kubectl port-forward service/monitoring-kube-prometheus-prometheus 9091:9090 -n monitoring
```

---

## What I Learned

- Building a complete GitOps workflow with ArgoCD
- Implementing security scanning (DevSecOps) with Trivy
- Configuring Kubernetes probes, resource limits, and HPA
- Exposing custom Prometheus metrics from a Flask application
- Writing PromQL queries for monitoring
- Managing multi-service deployments with Helm

---

## Author

**Yosra Benali**
Cloud & DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-yosrabnali-black)](https://github.com/yosrabnali)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-yosrabenali-blue)](https://hub.docker.com/r/yosrabenali)