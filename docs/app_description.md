# App Name: PyFactory

## Core Concept
This is a command-line Python application that functions as a fully autonomous, multi-agent AI codebase factory. The system's goal is to take a single user prompt (in the form of an `app_description.md` file) and turn it into a complete, zipped software project. It should require no human interaction after the initial command is run.

## Target Platform
This is a Python command-line application designed to run in a standard shell environment (like Bash or Zsh). It must be compatible with Python 3.10 and higher.

## Key Features & Workflow

1.  **Initialization:**
    *   The user will run the application from their terminal (e.g., `python main.py --description path/to/app_description.md`).
    *   The application must set up a dedicated project directory for the new software it's building, including initializing a Git repository and creating necessary sub-folders (`docs/`, `signals/`, `work_breakdown/`).

2.  **Configuration:**
    *   The system's logic must be highly configurable without changing the core Python code.
    *   **Agent Rules:** The behavior and persona for each AI agent must be defined in external Markdown files (e.g., `rules/rules-planner.md`).
    *   **LLM Configuration:** There must be a YAML file (`models.yaml`) to define LLM providers (e.g., OpenRouter, Google AI) and assign specific models to specific agent roles. This allows for flexibility and cost management.

3.  **Multi-Agent Orchestration:**
    *   The application will orchestrate a series of specialized AI agents in a specific sequence, controlled by a "Dispatcher" logic. The primary agents are:
        *   **Product Manager:** Reads the user's app description and generates a full suite of SDLC documents. Must be able to intelligently select a default tech stack (e.g., Next.js/Supabase for web, Flutter for mobile) if the user doesn't specify one.
        *   **Planner:** Reads the SDLC documents and creates a detailed, atomic, machine-readable implementation plan.
        *   **Developer:** Executes the plan. This agent's interaction must be tightly controlled by the main Python script, using the `aider-chat` library as a tool to apply code changes and make Git commits for each individual task.
        *   **User Simulator & Auditor:** Verifies the generated codebase against the documentation for logical and functional correctness. They should be able to trigger a "failure" state that loops back to the Planner for fixes.

4.  **Error Handling & Self-Correction:**
    *   The system must have a feedback loop. If the Auditor finds a discrepancy, it should generate a work item, and the Dispatcher should re-engage the Planner and Developer to fix the issue.

5.  **Final Output:**
    *   Upon successful completion of all phases and a passing audit, the application must clean up all temporary files and package the entire generated project directory into a single `.zip` file, named after the project.
    *   It should print a final success message to the console and exit gracefully.