


# 🚀 DevOps Study App: Cloud-Native CI/CD & Kubernetes Platform

A fully automated CI/CD pipeline and Kubernetes deployment platform designed to simulate **real-world production infrastructure**. This project demonstrates **end-to-end DevOps best practices**, including GitOps workflows, automated testing, container security, infrastructure automation, and AI-ready deployment patterns.

> **Purpose:** Build a production-grade platform that enables developers to ship applications faster, safer, and with zero manual intervention.

---

## 🔥 Tech Stack

<!-- Neon Dark Mode badges (for-the-badge style) -->
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=FF9900)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![K3s](https://img.shields.io/badge/K3s-FFC61C?style=for-the-badge&logo=rancher&logoColor=white)
![K3d](https://img.shields.io/badge/K3d-FF6A00?style=for-the-badge&logo=docker&logoColor=white)
![FluxCD](https://img.shields.io/badge/FluxCD-2C3E50?style=for-the-badge&logo=flux&logoColor=white)
![Kustomize](https://img.shields.io/badge/Kustomize-7B42BC?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=for-the-badge&logo=trivy&logoColor=white)
![Semantic Release](https://img.shields.io/badge/Release%20Please-8A2BE2?style=for-the-badge&logo=semanticrelease&logoColor=white)
![DevContainers](https://img.shields.io/badge/DevContainers-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

---

## 🔧 Key Features & Capabilities

| Capability | Description | Impact |
|-----------|-------------|--------|
| **GitHub Actions CI/CD** | Automated linting, testing, security scans, and release pipelines | 🚀 Reduce deployment effort by ~90% |
| **Kubernetes Deployment (K3d / Kustomize)** | Environment-specific overlays with GitOps compatibility | ✅ Zero-drift deployments |
| **Container Security (Trivy)** | Automated image scanning during pipeline | 🔒 Shift-left security |
| **Semantic Releases (Release Please)** | Versioning & changelog automation | 📦 Production-ready cadence |
| **Fully Containerized Dev Environments** | DevContainers for consistent onboarding | 🧪 No more “works on my machine” |
| **AI/LLM Infrastructure Ready** | Architecture supports GPU scheduling & inference workloads | 🤖 Future-proof infra |

---

## 🏗 Architecture Overview

```mermaid
flowchart LR
    Dev(Developer Commit) --> CI[GitHub Actions CI Pipeline]
    CI --> Build[Docker Build & Trivy Scan]
    Build --> Test[PyTest Integration Tests]
    Test --> Release[Semantic Release Publish]
    Release --> Deploy[FluxCD / K8s Apply]
    Deploy --> K3d[K3d Local Cluster / K3s Remote]
````

---

## 🧠 Technology Stack

* **Languages & Frameworks:** Python 3.13, Jinja2
* **Containerization:** Docker, Docker Compose
* **Orchestration:** Kubernetes (K3d), Kustomize, GitOps-ready with FluxCD
* **CI/CD:** GitHub Actions, Trivy, PyTest, Release Please, DevContainers
* **Tooling:** Mise (environment automation), K3d (lightweight k8s)
* **Future Ready:** GPU scheduling + AI model deployment support (LLM inference through containers)

---

## 📁 Repository Structure

```text
.
├── src/                # Application code for backend & frontend
│   ├── backend/        # API/service, logic, tests
│   └── frontend/       # Jinja2 templates, Dockerfile
├── kubernetes/         # Kustomize overlays, deployment scripts
├── scripts/            # Automation scripts
├── dev-keys/           # Example SSH keys for GitOps (do not use in prod)
├── docker-compose.yaml # Local orchestration
├── mise.toml           # Managed dev environment
└── release-please-config.json  # Automated release pipeline config
```

---

## ⚙️ CI/CD Pipeline Flow

### 🔄 On Every Commit / PR

* ✅ **Lint & Format:** Ruff, pre-commit
* ✅ **Unit Tests:** PyTest with coverage
* ✅ **Security Scan:** Trivy image scanning
* ✅ **Build & Push Docker Image**
* ✅ **Semantic Release:** Tags, changelogs & GitHub releases
* ✅ **K8s Integration Testing:** Deploy to K3d for full E2E validation
* ✅ **GitOps-Ready:** Integrate FluxCD for continuous reconciliation

---

## 🚀 Deployment Options

| Environment | Platform  | Deployment Mechanism            |
| ----------- | --------- | ------------------------------- |
| **Local**   | K3d       | Kustomize + GitHub Actions      |
| **Remote**  | K3s / EKS | GitOps (FluxCD) or direct apply |

---



## 🌟 Outcomes & Learning Value

✔ Demonstrates **real DevOps maturity** – from code to production
✔ Teaches **platform engineering fundamentals** (GitOps, IaC, observability)
✔ Validates **AI infrastructure readiness** via Kubernetes-native patterns
✔ Enables **scalable, reproducible deployments** for any cloud-native app

---

## 📌 Future Enhancements (Roadmap)

* 🔄 FluxCD GitOps automation (in progress)
* 🤖 AI/LLM inference workload integration
* 🔐 SOPS + Sealed Secrets for key management
* 🔎 Distributed tracing & advanced observability (OpenTelemetry)

---


## 📫 Contact & Collaboration

If you’re interested in DevOps, Kubernetes, Cloud Native development, or AI infrastructure — let’s connect!

**📧 Email:** [babu.macharia@protonmail.com](mailto:babu.macharia@protonmail.com)
**🔗 LinkedIn:** [https://linkedin.com/in/babu-macharia](https://linkedin.com/in/babu-macharia)
**🌐 Blog:** [https://babumacharia.com](https://babumacharia.com)



