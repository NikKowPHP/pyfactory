# PyFactory

## Overview
An autonomous AI-powered codebase factory that transforms app descriptions into complete software projects through multi-agent collaboration.

## Key Features
- CLI-driven project initialization
- Configurable AI agent personas
- Model-agnostic LLM integration
- Self-correcting implementation workflow
- Audit-powered quality assurance
- Production-grade security sandboxing:
  * Restricted file write locations
  * Path traversal prevention
  * Dangerous file extension blocking

## Prerequisites
- Python 3.10+
- pip package manager

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/pyfactory.git
cd pyfactory

# Install dependencies
pip install -r requirements.txt
```

## Getting Started
```bash
python main.py --description path/to/app_description.md
```

## Configuration
1. Agent rules: `rules/rules-*.md`
2. LLM models: `models.yaml`
3. Project structure: `docs/`, `signals/`, `work_breakdown/`

## Contribution
```mermaid
graph LR
    A[Product Manager] --> B[Specs]
    B --> C[Planner]
    C --> D[Developer]
    D --> E[Auditor]
    E -->|Valid| F[Output]
    E -->|Issues| C