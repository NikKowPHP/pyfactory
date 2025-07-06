# Engineering Work Plan: PyFactory Compliance

## High-Level Summary
This work plan translates the findings from the SpecCheck Audit Report into an actionable, prioritized set of tasks for an AI developer. The primary goal is to close the significant gap between the project's documentation and its current implementation. The plan focuses first on building the missing core application logic (P1), then addresses minor filesystem and code mismatches (P2), and finally resolves documentation gaps (P3). Completing this plan will bring the codebase into 100% compliance with its specifications.

---

### P1 - Implementation of Missing Features
*This tier focuses on creating the foundational files and logic for features that are documented but entirely missing from the codebase.*

- [ ] **[CREATE]**: Project directory structure setup function
    - **File**: `src/core/project_setup.py`
    - **Action**: Create a new file and implement a function `create_project_structure(base_path: Path)` that creates the `docs/`, `signals/`, and `work_breakdown/` subdirectories.
    - **Reason**: Audit finding: "[🟡 Partial] Project Initialization. The code to create the necessary sub-folders (...) as per FR 1.3 is missing."

- [ ] **[CREATE]**: Agent rule loader from Markdown files
    - **File**: `src/core/rule_manager.py`
    - **Action**: Create a new file and implement a function `load_agent_rules(agent_slug: str) -> str` that reads the content of the corresponding `rules/rules-{agent_slug}.md` file.
    - **Reason**: Audit finding: "[❌ Missing] Configurable Agent Rule Loading. No code exists to read, parse, or utilize these Markdown files."

- [ ] **[CREATE]**: Core Dispatcher engine for agent routing
    - **File**: `src/core/dispatcher.py`
    - **Action**: Create a `Dispatcher` class. Implement a method `get_next_agent()` that checks for signal files (e.g., `PROJECT_AUDIT_PASSED.md`, `IMPLEMENTATION_COMPLETE.md`, `PLANNING_COMPLETE.md`) in order of precedence to determine which agent's turn it is.
    - **Reason**: Audit finding: "[❌ Missing] Multi-Agent Orchestration. The 'Dispatcher Engine' responsible for reading signals and sequencing agents is entirely unimplemented."

- [ ] **[CREATE]**: Audit failure feedback loop logic in Dispatcher
    - **File**: `src/core/dispatcher.py`
    - **Action**: Extend the `Dispatcher` to check for the existence of files in a `work_items/` directory. If any exist, it should prioritize handing off to the 'planner' agent.
    - **Reason**: Audit finding: "[❌ Missing] Audit Feedback Loop. The workflow for a failed audit to generate a work item and re-engage the Planner is completely missing."

- [ ] **[CREATE]**: Main orchestration pipeline
    - **File**: `src/core/orchestrator.py`
    - **Action**: Implement a `run_pipeline()` function. This function should contain the main application loop that uses the `Dispatcher` to determine and execute the sequence of agents.
    - **Reason**: Audit finding: "The core function—generating a project—is missing." This orchestrator will serve as the main application controller.

- [ ] **[CREATE]**: Final project packaging utility
    - **File**: `src/core/output_generator.py`
    - **Action**: Implement a function `create_zip_archive(source_dir: Path, output_path: Path)` that packages a directory into a ZIP file, excluding temporary files and directories like `__pycache__/`.
    - **Reason**: Audit finding: "[❌ Missing] Final Output Generation. The functionality to package the generated project into a .zip archive is unimplemented."

- [ ] **[CREATE]**: Main application entry point to tie components together
    - **File**: `src/main.py`
    - **Action**: Create the main executable script. This script should call `cli.parser.parse_app_description()`, then initialize and run the `core.orchestrator.run_pipeline()`.
    - **Reason**: Audit finding: "[🟡 Partial] User Story: As a developer... The entry point exists, but the core function—generating a project—is missing."

- [ ] **[UPDATE]**: Implement success/failure exit codes in CLI
    - **File**: `src/main.py`
    - **Action**: Wrap the call to `run_pipeline()` in a try/except block. On success, exit with code 0. On any unhandled exception, print an error and exit with code 1.
    - **Reason**: Audit finding: "[🟡 Partial] CLI Interface. The application lacks status-based exit code handling as required by FR 5.3."

---

### P2 - Correcting Mismatches
*This tier focuses on fixing minor mismatches between the documentation and the file system or existing code.*

- [ ] **[FIX]**: Remove erroneous log file from documentation directory
    - **File**: `docs/READEME.md`
    - **Action**: Delete the file `docs/READEME.md`.
    - **Reason**: Audit finding: "[Anomaly] Filename Mismatch. This file appears to be an erroneously generated status log... and should be deleted to avoid confusion."

---

### P3 - Documentation Updates
*This tier focuses on updating the documentation to reflect implemented but undocumented features.*

- [ ] **[DOCS]**: Document the advanced error handling framework
    - **File**: `docs/System_Architecture.md`
    - **Action**: Add a new section under "Core Components" titled "5. Error Handling Framework". Describe the custom exception classes (`BaseError`, `ValidationError`), the structured error codes, and the `@retry` and `@error_handler` decorators.
    - **Reason**: Audit finding: "Undocumented Functionality: Advanced Error Handling Framework. This is a robust framework that... should be updated to describe this important component."

- [ ] **[DOCS]**: Document the CLI output formatting feature
    - **File**: `docs/Functional_Requirements.md`
    - **Action**: Add a new requirement, "5.4 The system must support selectable output formats (JSON, YAML) via a `--format` command-line argument."
    - **Reason**: Audit finding: "Undocumented Functionality: CLI Output Formatting. This user-facing feature should be added to `Functional_Requirements.md`."

- [ ] **[DOCS]**: Document the data serialization model
    - **File**: `docs/System_Architecture.md`
    - **Action**: In the "Core Components" section, add a note under "Agent System" or "Data Model" explaining that all data objects inherit from a `BaseModel` class in `src/core/repo.py` which provides `to_json` and `from_json` serialization methods.
    - **Reason**: Audit finding: "Undocumented Functionality: Data Serialization Model. This is a core architectural pattern... that should be documented in `System_Architecture.md`."