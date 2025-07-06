
# Engineering Work Plan: Achieving Core Functionality

## High-Level Summary
This work plan addresses the primary finding of the latest audit: the application's core orchestration logic is a non-functional placeholder. The tasks are prioritized to first fix the central orchestrator loop (P0), then build out the missing agent and data model implementations required to make that loop functional (P1), and finally clean up extraneous artifacts (P2). Completing this plan will transition the project from a static skeleton to a dynamic, executable system that can run its documented workflow from start to finish.

---

### P0 - Critical Code Fixes
*This tier focuses on replacing the non-functional placeholder logic that is blocking the entire application from working.*

- [ ] **[FIX]**: Replace placeholder logic in Orchestrator with actual agent execution
    - **File**: `src/core/orchestrator.py`
    - **Action**: Rewrite the `run_pipeline` function's loop. Instead of `print(f"Switching to agent: {next_agent}")`, it must instantiate the appropriate agent class (e.g., `PlannerAgent`, `DeveloperAgent`), pass it necessary context, and call a standard method like `execute()`.
    - **Reason**: Audit finding: "[🟡 Partial] Multi-Agent Orchestration. The `run_pipeline` function contains a placeholder loop that only prints the name of the next agent. It does not instantiate or execute any agent logic."

---

### P1 - Implementation of Missing Features
*This tier focuses on creating the necessary classes and structures to support the P0 fix and enable a complete, functional workflow.*

- [ ] **[CREATE]**: Implement concrete data model classes
    - **File**: `src/core/models.py`
    - **Action**: Create a new file to house the data models. Implement Python classes for `Project`, `AgentConfiguration`, `WorkItem`, and `AuditResult` as defined in `docs/Data_Model.md`. These classes should inherit from the existing `BaseModel` in `src/core/repo.py`.
    - **Reason**: Audit finding: "[🟡 Partial] Data Models. The specific data models described in the documentation are not implemented as distinct classes."

- [ ] **[CREATE]**: Create an abstract base class for all agents
    - **File**: `src/core/agents/base_agent.py`
    - **Action**: Create a new directory and file. Define an abstract class `BaseAgent` with an `__init__` method that accepts context (e.g., rules, config) and an abstract `execute()` method that all concrete agents will implement.
    - **Reason**: To provide a consistent interface for the Orchestrator to run any agent, resolving the core non-functional state of the application.

- [ ] **[CREATE]**: Implement a concrete PlannerAgent class
    - **File**: `src/core/agents/planner_agent.py`
    - **Action**: Create a `PlannerAgent` class that inherits from `BaseAgent`. Its `execute()` method should perform the documented planner role: consuming an input signal (like `SPECIFICATION_COMPLETE.md`) and creating the output signal (`PLANNING_COMPLETE.md`).
    - **Reason**: To provide the first concrete, executable implementation for the Orchestrator, making the workflow functional.

- [ ] **[CREATE]**: Implement a concrete DeveloperAgent class
    - **File**: `src/core/agents/developer_agent.py`
    - **Action**: Create a `DeveloperAgent` class inheriting from `BaseAgent`. Its `execute()` method should consume the `PLANNING_COMPLETE.md` signal and, upon completion, create the `IMPLEMENTATION_COMPLETE.md` signal.
    - **Reason**: To provide the next concrete agent in the chain, enabling the Orchestrator to run a multi-step workflow.

- [ ] **[CREATE]**: Implement a concrete AuditorAgent class
    - **File**: `src/core/agents/auditor_agent.py`
    - **Action**: Create an `AuditorAgent` class inheriting from `BaseAgent`. Its `execute()` method should consume the `IMPLEMENTATION_COMPLETE.md` signal and create the `PROJECT_AUDIT_PASSED.md` signal.
    - **Reason**: To provide the final concrete agent in the primary success path, allowing the Orchestrator to run the full application lifecycle.

---

### P2 - Correcting Mismatches
*This tier focuses on cleaning up extraneous files and artifacts identified in the audit.*

- [ ] **[FIX]**: Remove extraneous development artifact
    - **File**: `work_breakdown/tasks/a.md`
    - **Action**: Delete the file `work_breakdown/tasks/a.md`.
    - **Reason**: Audit finding: "[Anomaly] Extraneous File. The file is a development artifact and not part of the defined application structure."