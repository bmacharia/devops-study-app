# DevOps Study App: Technical Documentation

This repository provides a reference implementation of a full-stack Python application, architected to demonstrate advanced DevOps practices. The project integrates automated CI/CD pipelines (GitHub Actions), containerization, and Kubernetes-based deployment, with a focus on reproducibility, automation, and production-readiness.

## Table of Contents

- [DevOps Study App: Technical Documentation](#devops-study-app-technical-documentation)
  - [Table of Contents](#table-of-contents)
  - [System Overview](#system-overview)
  - [Technology Stack](#technology-stack)
  - [Environment Setup](#environment-setup)
  - [Development Workflow](#development-workflow)
  - [Directory Structure](#directory-structure)
  - [CI/CD Pipeline and Kubernetes Integration](#cicd-pipeline-and-kubernetes-integration)

## System Overview

The system consists of two primary Python services (backend and frontend), each containerized and orchestrated via Kubernetes. The repository is structured to support:

- Local development and integration testing using Docker Compose
- Automated code quality enforcement and testing
- Multi-stage container builds for production parity
- Kubernetes deployment with kustomize overlays for environment-specific configuration
- GitOps workflows and automated release management
- End-to-end CI/CD pipeline using GitHub Actions

## Technology Stack

- Python 3.13 (application logic)
- Docker & Docker Compose (containerization, local orchestration)
- Kubernetes (K3d for local clusters, kustomize for overlays)
- GitHub Actions (CI/CD automation)
- Mise (toolchain/environment management)

## Environment Setup

Required tools:

- Docker & Docker Compose
- Python 3.13
- Mise CLI (`pip install mise`)

1. Install all prerequisites listed above.
2. Clone this repository.
3. Run `mise install` to provision the required toolchain and Python environment.
4. For local development, use `docker-compose up` to start all services.

## Development Workflow

- Application code is located in `src/` (backend and frontend)
- Unit and integration tests are in `src/backend/tests`
- Use scripts in `scripts/` and `kubernetes/` for cluster setup, deployment, and automation

## Directory Structure

```text
.
├── src/
│   ├── backend/      # Backend service: API, business logic, tests, Dockerfile
│   └── frontend/     # Frontend service: Jinja2 templates, Dockerfile
├── kubernetes/       # Kubernetes manifests, kustomize overlays, cluster setup scripts
├── scripts/          # Automation and utility scripts
├── dev-keys/         # SSH keys for GitOps/CI deployment
├── docker-compose.yaml
├── mise.toml
├── README.md
└── release-please-config.json
```

## CI/CD Pipeline and Kubernetes Integration

The repository implements a comprehensive CI/CD pipeline using **GitHub Actions**. Key stages include:

- Linting, formatting, and automated testing on every commit and pull request
- Multi-stage Docker image build and registry publish
- Automated release and publishing of Docker images to a container registry
- End-to-end application testing on a real Kubernetes cluster provisioned with **K3d** (in-pipeline)
- Kubernetes deployment using manifests and kustomize overlays
- Automated release management and GitOps support

Kubernetes manifests and overlays are provided for both local and remote cluster deployments. The pipeline leverages K3d to provision a lightweight Kubernetes cluster for integration and E2E testing, ensuring production parity and deployment reliability. Docker images are automatically built and released to the configured registry as part of the release workflow.
