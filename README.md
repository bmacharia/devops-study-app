
# DevOps Study App

A Python-based application designed to showcase end-to-end DevOps best practices, from local development to production-ready CI/CD and container orchestration.

## Table of Contents

- [About The Project](#about-the-project)  
- [Built With](#built-with)  
- [Prerequisites](#prerequisites)  
- [Getting Started](#getting-started)  
- [Usage](#usage)  
- [Folder Structure](#folder-structure)  
- [CI/CD Workflows](#ci-cd-workflows)  
- [Development](#development)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)  

## About The Project

This repo demonstrates a full DevOps workflow around a Python application, covering:

- **Remote-container development** with VS Code DevContainers 
- **Dependency & packaging** via `mise.toml` (Mise CLI)   
- **Code quality** enforced by pre-commit hooks (`.pre-commit-config.yaml`)  
- **Containerization** using Docker and Docker Compose (`docker-compose.yaml`)   
- **Continuous Integration** pipelines in GitHub Actions (`.github/workflows`)  
- **Application source** in Python under `src/` :contentReference[oaicite:5]{index=5}  

## Built With

- **Python** 
- **Docker** & **K3d** 
- **GitHub Actions** (CI/CD pipelines)
- **DevContainers** (`.devcontainer/`)
- **pre-commit** (`.pre-commit-config.yaml`) 
- **Mise CLI** (`mise.toml`) 

## Prerequisites

- **Docker** & **Docker Compose**  
- **Python 3.13**  
- **Mise CLI** (install via `pip install mise`)  


## Folder Structure

```
.
├── .devcontainer/                 # VS Code remote-container config
├── .github/
│   └── workflows/                # CI/CD pipeline definitions
├── scripts/                      # Helper scripts (build, deploy, etc.)
├── src/                          # Python application code
├── .pre-commit-config.yaml       # Linting & formatting hooks
├── docker-compose.yaml           # Multi-container dev/testing setup
├── mise.toml                     # Dependency & packaging config
└── ReadMe.md                     # This file
```


## CI/CD Workflows

Under `.github/workflows/` you’ll find automated pipelines for:

* **Linting & Formatting**
* **Unit & Integration Testing**
* **Docker Image Build & Publish**
* **Release Automation**

