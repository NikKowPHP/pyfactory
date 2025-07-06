# System Architecture

## Core Components

1. **CLI Interface**  
   - Entry point for user interaction  
   - Handles argument parsing and initial setup  
   - Manages project directory creation and ZIP output  

2. **Dispatcher Engine**  
   - Orchestrates agent workflow sequence (Product Manager → Planner → Developer → Auditor)  
   - Monitors signal files for phase transitions  
   - Implements error recovery workflows  

3. **Agent System**  
   - Product Manager: Generates SDLC docs from app_description.md  
   - Planner: Creates atomic implementation plans  
   - Developer: Executes code changes via aider-chat integration  
   - Auditor: Validates output against requirements  

4. **Configuration Manager**
   - Loads agent rules from Markdown files
   - Maintains LLM model assignments from models.yaml
   - Tracks runtime parameters through environment variables

5. **Error Handling Framework**
   - Custom exception classes (BaseError, ValidationError)
   - Structured error codes with machine-readable formats
   - Decorators for retry logic (@retry) and consistent formatting (@error_handler)
   - Implemented in src/core/error_handler.py

6. **Data Serialization Model**
    - All data objects inherit from BaseModel in src/core/repo.py
    - Provides standardized to_json() and from_json() methods
    - Supports consistent serialization across all components

7. **Security Sandboxing**
    - All file writes are restricted to './generated_project/' directory
    - Path validation prevents:
      * Parent directory traversal (../)
      * System directory access (/etc, /bin, etc.)
      * Dangerous file extensions (.sh, .exe, etc.)
    - Implemented in src/core/agents/developer_agent.py
    - Critical for production safety when using AI-generated code

## Interaction Flow
```mermaid
graph TD
    A[CLI Start] --> B[Dispatcher]
    B --> C[Product Manager]
    C --> D[Planner]
    D --> E[Developer]
    E --> F[Auditor]
    F -->|Success| G[ZIP Generation]
    F -->|Failure| H[Work Item Creation]
    H --> D