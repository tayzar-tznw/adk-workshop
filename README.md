# Sample Agents

This folder contains agent samples for workshop.

## Getting Started

1.  **Prerequisites:**

    *   "Ensure you have installed and configured the Agent Development Kit (ADK). See the [ADK Quickstart Guide](https://google.github.io/adk-docs/get-started/quickstart/)."
    *   "Python 3.9+ and [Poetry](https://python-poetry.org/docs/#installation) installed."
    *   "Access to Google Cloud (Vertex AI) and/or a Gemini API Key (depending on the agent - see individual agent READMEs)."

2.  **Running a Sample Agent:**
    *   "Navigate to the specific agent's directory (e.g., `cd agents/weather-agent`)."
    *   "Copy the `.env.example` file to `.env` and fill in the required environment variables (API keys, project IDs, etc.). See the agent's specific README for details on required variables."
    *   "Install dependencies using Poetry: `poetry install`"
    *   "Follow the instructions in the agent's `README.md` to run it (e.g., using `adk run .` or `adk web`)."


## Workshop Catergories

Check out the agent samples below, organized by category:

| Feature | Data Science Agent                                                                                                           | Movie Script Agent                                                                                                                                                                                               | Travel Concierge                                                                                                                                                                                                                                   | Weather Agent                                                                                         |
| :------------------- |:-----------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------|
| Primary Goal | Perform sophisticated data analysis.                                                                                         | Develop a comprehensive movie pitch document.                                                                                                                                                                    | Act as a digital travel assistant for planning and booking.                                                                                                                                                                                        | Provide weather information and demonstrate basic ADK concepts.                                       |
| Key Concepts Taught | - Multi-agent systems<br>- Function tool (Python)<br>- Agent tool<br>- NL2SQL<br>- Structured data<br>- Database interaction | - Multi-agent systems (Sequential, Loop, Parallel)<br>- Workflow agents<br>- Tool creation & usage (append_to_state, exit_loop)<br>- Iterative refinement<br>- State management <br>- Add Integration Connectors | - Multi-agent systems<br>- Function tool (Python)<br>- Custom tool creation<br>- Agent tool<br>- Input/output schema<br>- Updatable context<br>- Dynamic instructions <br>- MCP (Airbnb) <br>- OpenAPI Tool <br>- Potential A2A with weather agent | - Multi-agent systems<br>- Function tool (Python)<br>- Basic ADK concepts <br>- Add OpenAPI Tools     |
| Differences/Scenario | Focuses on querying and analyzing structured data using multiple specialized agents.                                         | Simulates a creative workflow involving research, writing, critique, and reporting, managed by different types of workflow agents.                                                                               | Emulates a concierge service, handling user requests for travel, requiring dynamic instruction handling and context updates.                                                                                                                       | A straightforward agent to fetch and present weather data, illustrating fundamental ADK features.     |
| Difficulty | Advanced                                                                                                                     | Intermediate                                                                                                                                                                                                     | Intermediate                                                                                                                                                                                                                                       | Easy                                                                                                  |
| Interaction Type | Workflow                                                                                                                     | Workflow                                                                                                                                                                                                         | Conversational                                                                                                                                                                                                                                     | Conversational                                                                                        |



## Using the Agents in this Repository

This section provides general guidance on how to run, test, evaluate, and potentially deploy the agent samples found in this repository. While the core steps are similar, **each agent has its own specific requirements and detailed instructions within its dedicated `README.md` file.**

**Always consult the `README.md` inside the specific agent's directory (e.g., `agents/weather-agent/README.md`) for the most accurate and detailed steps.**

Here's a general workflow you can expect:

1.  **Choose an Agent:** Select an agent from the table above that aligns with your interests or use case.
2.  **Navigate to the Agent Directory:** Open your terminal and change into the agent's main directory:
    ```bash
    cd agents/<agent-name> 
    # Example: cd agents/weather-agent
    ```
3.  **Review the Agent's README:** **This is the most crucial step.** Open the `README.md` file within this directory. It will contain:
    *   A detailed overview of the agent's purpose and architecture.
    *   Specific prerequisites (e.g., API keys, cloud services, database setup).
    *   Step-by-step setup and installation instructions.
    *   Commands for running the agent locally.
    *   Instructions for running evaluations (if applicable).
    *   Instructions for running tests (if applicable).
    *   Steps for deployment (if applicable).

4.  **Setup and Configuration:**
    *   **Prerequisites:** Ensure you've met the general prerequisites listed in the main "Getting Started" section *and* any specific prerequisites mentioned in the agent's README.
    *   **Dependencies:** Install the agent's specific Python dependencies using Poetry (this command is usually run from the agent's main directory):
        ```bash
        poetry install
        ```
    *   **Environment Variables:** Most agents require configuration via environment variables. Copy the `.env.example` file to `.env` within the agent's directory and populate it with your specific values (API keys, project IDs, etc.). Consult the agent's README for details on required variables. You may need to load these variables into your shell environment (e.g., using `source .env` or `set -o allexport; . .env; set +o allexport` in bash).

5.  **Running the Agent Locally:**
    *   Agents can typically be run locally for testing and interaction using the ADK CLI or ADK Dev UI. The specific command might vary slightly (e.g., the exact directory to run from), so check the agent's README.
    *   **CLI:** Often involves running `adk run .` from within the agent's *core code* directory (e.g., `agents/weather-agent/weather-agent/`).
        ```bash
        # Example (check agent's README for exact path)
        cd agents/weather-agent/weather-agent/ 
        adk run . 
        ```
    *   **ADK Dev UI:** Often involves running `adk web .` from the agent's *main* directory (e.g., `agents/weather-agent/`).
        ```bash
        # Example (check agent's README for exact path)
        cd agents/weather-agent/
        adk web
        ```
        Then, open the provided URL in your browser and select the agent from the dropdown menu.

6.  **Evaluating the Agent:**
    *   Many agents include an `eval/` directory containing scripts and data to assess performance.
    *   The agent's README will explain how to run these evaluations (e.g., `python eval/test_eval.py`). This helps verify the agent's effectiveness on specific tasks.

7.  **Testing the Agent Components:**
    *   A `tests/` directory often contains unit or integration tests (e.g., for custom tools).
    *   These ensure the individual code components function correctly.
    *   The agent's README may provide instructions on how to run these tests, often using a framework like `pytest`.

8.  **Deploying the Agent:**
    *   Some agents are designed for deployment, typically to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview).
    *   The `deployment/` directory contains the necessary scripts (like `deploy.py`) and configuration files.
    *   Deployment usually requires specific Google Cloud setup (Project ID, enabled APIs, permissions). The agent's README and the scripts within the `deployment/` folder provide detailed instructions, similar to the example shown in the `weather-agent` agent's documentation.

By following the specific instructions in each agent's `README.md`, you can effectively set up, run, evaluate, test, and potentially deploy these diverse examples.

## Directory Structure of Agents
Each agent displayed here is organized as follows:

```bash
├── agent-name
│   ├── agent_name/
│   │   ├── shared_libraries/               # Folder contains helper functions for tools
│   │   ├── sub_agents/                     # Folder for each sub agent
│   │   │   │   ├── tools/                  # tools folder for the subagent
│   │   │   │   ├── agent.py                # core logic of the sub agent
│   │   │   │   └── prompt.py               # prompt of the subagent
│   │   │   └── ...                         # More sub-agents    
│   │   ├── __init__.py                     # Initializes the agent
│   │   ├── tools/                          # Contains the code for tools used by the router agent
│   │   ├── agent.py                        # Contains the core logic of the agent
│   │   ├── prompt.py                       # Contains the prompts for the agent
│   ├── deployment/                         # Deployment to Agent Engine
│   ├── eval/                               # Folder containing the evaluation method
│   ├── tests/                              # Folder containing unit tests for tools
│   ├── agent_pattern.png                   # Diagram of the agent pattern
│   ├── .env.example                        # Store agent specific env variables
│   ├── pyproject.toml                      # Project configuration
│   └── README.md                           # Provides an overview of the agent
```
### General Structure

#### Directory Breakdown

1.  **`agent_name/` (Core Agent Code)**: 
    *   This directory contains the core logic of the agent.
    *   **`shared_libraries/`**: (Optional) Contains code that is shared among multiple sub-agents.
    *   **`sub_agents/`**: Contains the definitions and logic for sub-agents.
        *   Each sub-agent has its own directory (e.g., `planning/`, `booking/` in `travel-conceirge`).
        *   **`tools/`**: Contains any custom tools specific to the sub-agent.
        *   **`agent.py`**: Defines the sub-agent's behavior, including its model, tools, and instructions.
        *   **`prompt.py`**: Contains the prompts used to guide the sub-agent's behavior.
    *   **`__init__.py`**: An initialization file that imports the `agent.py` from the folder for marking the `agent_name` directory as a Python package.
    *   **`tools/`**: Contains any custom tools used by the main agent.
    *   **`agent.py`**: Defines the main agent's behavior, including its sub-agents, model, tools, and instructions.
    *   **`prompt.py`**: Contains the prompts used to guide the main agent's behavior.
    
    Note that the initial folder name is with "-" between words whereas the core logic is stored in the folder with the same agent name but with "_" between words (e.g., `llm_auditor`). This is due to the project structure imposed by poetry.

2.  **`deployment/`**

    *   Contains scripts and files necessary for deploying the agent to a platform like Vertex AI Agent Engine.
    *   The `deploy.py` script is often found here, handling the deployment process.

3.  **`eval/`**

    *   Contains data and scripts for evaluating the agent's performance.
    *   Test data (e.g., `.test.json` files) and evaluation scripts (e.g., `test_eval.py`) are typically located here.

4.  **`tests/`**

    *   Contains unit and integration tests for the agent.
    *   Test files (e.g., `test_agents.py`) are used to verify the agent's functionality.

5.  **`agent_pattern.png`**

    *   A visual diagram illustrating the agent's architecture, including its sub-agents and their interactions.

6.  **`.env.example`**

    *   An example file showing the environment variables required to run the agent.
    *   Users should copy this file to `.env` and fill in their specific values.

7.  **`pyproject.toml`**

    *   Contains project metadata, dependencies, and build system configuration.
    *   Managed by Poetry for dependency management.

8.  **`README.md`**

    *   Provides detailed documentation specific to the agent, including its purpose, setup instructions, usage examples, and customization options.
