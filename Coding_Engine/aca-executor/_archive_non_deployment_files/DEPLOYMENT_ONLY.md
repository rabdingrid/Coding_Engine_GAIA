# 📦 Deployment Files Only

This directory contains ONLY the essential files for FastAPI deployment.

## Files in this directory:

```
Coding_Engine/aca-executor/
│
├── 📄 executor-service-fastapi.py
├── 🐳 Dockerfile.fastapi
├── 📋 requirements-fastapi.txt
│
└── 📁 terraform/
    ├── main.tf
    ├── variables.tf
    ├── postgresql.tf
    └── postgresql-variables.tf
```

## To see all files (including stashed):
```bash
git stash list
git stash show -p stash@{0}  # View stashed files
```

## To restore stashed files:
```bash
git stash pop
```

