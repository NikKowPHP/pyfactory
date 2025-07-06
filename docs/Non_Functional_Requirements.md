# Non-Functional Requirements

## 1. Performance
1.1 Agent handoff latency must be ≤500ms between phases  
1.2 ZIP generation for projects ≤100MB must complete in <30 seconds  
1.3 CLI must respond to --help command within 200ms  

## 2. Reliability
2.1 System must maintain operation through 3 consecutive agent failures  
2.2 Audit discrepancies must be detected with 99.9% accuracy  
2.3 Configuration changes must take effect without system restart  

## 3. Maintainability
3.1 Agent rules must be modifiable via Markdown files only  
3.2 LLM model assignments must be configurable via YAML  
3.3 All signal files must self-delete after being processed