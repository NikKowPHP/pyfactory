# Functional Requirements

## 1. Core Functionality
1.1 The system must parse app_description.md to determine project requirements  
1.2 The system must initialize a Git repository in the project directory  
1.3 The system must create directory structure: docs/, signals/, work_breakdown/

## 2. Configuration Management
2.1 The system must read agent personas from Markdown files in rules/ directory  
2.2 The system must load LLM configurations from models.yaml file  
2.3 The system must allow model assignments per agent role (e.g., Planner=GPT-4, Developer=Claude-3)

## 3. Agent Orchestration
3.1 The system must execute agents in sequence: Product Manager → Planner → Developer → Auditor  
3.2 The Dispatcher must track agent handoffs using signal files  
3.3 Failed audits must generate work_items/ entries for reprocessing

## 4. Error Handling
4.1 The system must retry failed agent operations up to 3 times  
4.2 Critical errors must create signals/NEEDS_ASSISTANCE.md for manual intervention  
4.3 Audit discrepancies must trigger Planner re-engagement within 5 seconds

## 5. Output Requirements
5.1 The system must package completed projects as ZIP files  
5.2 ZIP archives must exclude temporary working files  
5.3 The CLI must display success/failure status with exit codes (0=success, 1=error)
5.4 The system must support selectable output formats (JSON, YAML) via a --format command-line argument