# Data Model

## 1. Project
- **Fields:**  
  - id: UUID  
  - name: String (from app_description.md)  
  - created_at: DateTime  
  - status: Enum (initializing, planning, developing, auditing, completed)  
  - output_path: String (path to ZIP archive)  

## 2. Agent Configuration
- **Fields:**  
  - role: String (product_manager, planner, developer, auditor)  
  - rules_md: Path (to Markdown persona file)  
  - llm_model: String (from models.yaml)  
  - max_retries: Integer  

## 3. Work Item
- **Fields:**  
  - task_id: UUID  
  - description: String  
  - status: Enum (pending, in_progress, completed, failed)  
  - retry_count: Integer  
  - error_log: Text  

## 4. Audit Result
- **Fields:**  
  - audit_id: UUID  
  - passed: Boolean  
  - discrepancies: JSON (structured error report)  
  - timestamp: DateTime