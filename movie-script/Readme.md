## Build multi-agent systems with ADK

*   **schedule** 1 hour 30 minutes

### Overview

### Objective

### Setup and requirements

### Multi-Agent Systems

### The Hierarchical Agent Tree

Tree structure showing hierarchical agents

### Task 1. Install ADK and set up your environment

> **Note:** Using an Incognito browser window is recommended for most Qwiklabs to avoid confusion between your Qwiklabs student account and other accounts logged into Google Cloud. If you are using Chrome, the easiest way to accomplish this is to close any Incognito windows, then right click on the **Open Google Cloud console** button at the top of this lab and select **Open link in Incognito window**.

#### Enable Vertex AI recommended APIs

In the Google Cloud console, navigate to Vertex AI by searching for it at the top of the console.

Click **Enable all recommended APIs**.

#### Prepare a Cloud Shell Editor tab

Open Cloud Shell by pressing G and then S on your keyboard.

Click **Continue**.

When prompted to authorize Cloud Shell, click **Authorize**.

In the upper right of the Cloud Shell pane, click the **Open in new window** button (Open in new window button).

Click **Authorize** again.

Click the **Open Editor** pencil icon (Open Editor pencil icon) at the top of the pane to view files.

At the top of the left-hand navigation menu, click the **Explorer** icon Explorer icon to open your file explorer.

Click the **Open Folder** button.

In the Open Folder dialog that opens, click **OK** to select your Qwiklab student account's home folder.

#### Download and install the ADK and code samples for this lab

Install ADK by running the following command in the Cloud Shell Terminal.

> **Note:** You will specify the version to ensure that the version of ADK that you install corresponds to the version used in this lab:

```bash
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk==0.4.0
```

Install additional lab requirements with:

```bash
python3 -m pip install -r adk_multiagent_systems/requirements.txt
```

#### If needed, restore your Cloud Shell application-default authorization

> **Note:** You don't need to do the steps in this section now. They are provided as a convenience in case you encounter a TypeError error as you work on the lab, typically only after a long time, that ends like this:
>
> ```
> File "/home/student_03_d3d531d03b6c/.local/lib/python3.12/site-packages/google/auth/compute_engine/credentials.py", line 103, in _retrieve_info
> self._service_account_email = info["email"]
>                                 ~~~~^^^^^^^^^
> TypeError: string indices must be integers, not 'str'
> ```

The resolution is to refresh your application default credentials. Begin with this command, then follow the steps as you are prompted:

```bash
gcloud auth application-default login
```

You will then want to re-establish your project as your quota project with:

```bash
gcloud auth application-default set-quota-project YOUR_GCP_PROJECT_ID
```

### Workflow Agents

Parent to sub-agent transfers are ideal when you have multiple specialist sub-agents, and you want the user to interact with each of them.

However, if you would like agents to act one-after-another without waiting for a turn from the user, you can use workflow agents. Some examples of when you might use workflow agents include:
- ParallelAgent
Throughout the rest of this lab, you will build a multi-agent system that uses multiple LLM agents, workflow agents, and tools to help control the flow of the agent.

Specifically, you will build an agent that will develop a pitch document for a new hit movie: a biographical film based on the life of a historical character. Your sub-agents will handle the research, an iterative writing loop with a screenwriter and a critic, and finally some additional sub-agents will help brainstorm casting ideas and use historical box office data to make some predictions about box office results.

In the end, your multi-agent system will look like this (you can click on the image to see it larger):

Diagram of a film_concept_team multi-agent system


But you will begin with a simpler version.

Task 4. Begin building a multi-agent system with a SequentialAgent
A screenwriter to turn the research into a plot outline.
A file_writer to title the resulting movie and write the results of the sequence to a file.
```
Click on the `agent.py` file in the `workflow_agents` directory.

Read through this agent definition file. Because sub-agents must be defined before they can be assigned to a parent, to read the file in the order of the conversational flow, you can read the agents from the bottom of the file to the top.

```
You also have a function tool append_to_state. This function allows agents with the tool the ability to add content to a dictionary value in state. It is particularly useful for agents that might call a tool multiple times or act in multiple passes of a LoopAgent, so that each time they act their output is stored.

Try out the current version of the agent by launching the web interface from the Cloud Shell Terminal with:
adk web

```
To view the web interface in a new tab, click the http://0.0.0.0:8000 link in the Terminal output.

A new browser tab will open with the ADK Dev UI.

From the **Select an agent** dropdown on the left, select **workflow_agents**.

Start the conversation with: hello. It may take a few moments for the agent to respond, but it should request you enter a historical figure to start your film plot generation.


In the ADK Web UI, click on one of the agent icons (agent_icon) representing a turn of conversation to bring up the event view.

The event view provides a visual representation of the tree of agents and tools used in this session. You may need to scroll in the event panel to see the full plot.

adk web graph

In addition to the graph view, you can click on the **Request** tab of the event to see the information this agent received as part of its request, including the conversation history.

You can also click on the **Response** tab of the event to see what the agent returned.

When you are finished inspecting the events, close the browser tab and stop the server by highlighting the Terminal pane and pressing CTRL+C.

Task 5. Add a LoopAgent for iterative work
The LoopAgent is designed for tight iterative processes between agents. It repeatedly executes its sub-agents in the defined sequence until a termination condition is met.


Film_concept_team multi-agent system step 2


Your revised agent will flow like this:

The greeter will the same.
When the loop terminates, it will escalate control of the conversation back to the film_concept_team SequentialAgent, which will then pass control to the next agent in its sequence: the file_writer that will remain as before to give the movie a title and write the results of the sequence to a file.
To make these changes:

In the `adk_multiagent_systems/workflow_agents/agent.py` file, paste the following new agents into the `agent.py` file under the `# Agents` section header:

critic = Agent(
    name="critic",
    """,
    tools=[append_to_state],
)

Create a new LoopAgent called writers_room that creates the iterative loop of the researcher, screenwriter, and critic. Each pass through the loop will end with a critical review of the work so far, which will prompt improvements for the next round. Paste the following above the existing film_concept_team SequentialAgent.

writers_room = LoopAgent(
    ],
    max_iterations=3,
)

Note that the LoopAgent creation includes a parameter for max_iterations. This defines how many times the loop will run before it ends. Even if you plan to interrupt the loop via another method, it is a good idea to include a cap on the total number of iterations.

Update the film_concept_team SequentialAgent to remove the researcher and screenwriter and replace them with the writers_room LoopAgent. Now the film_concept_team creation should look like this:
        file_writer
    ],
)

Launch the web interface from the Terminal with:

adk web

A new browser tab will open with the ADK Dev UI.

From the **Select an agent** dropdown on the left, select **workflow_agents**.

Begin a new conversation with: hello


Using the Editor, review the file generated, which should be saved in the adk_multiagent_systems/movie_pitches directory. (Once again, you may need to use the Editor's menu to enable View > Word Wrap to see the full text without lots of horizontal scrolling.)

### Task 6. Add a termination condition for the LoopAgent
Currently, your loop runs the number of times specified by the max_iterations parameter of your LoopAgent. But if the movie pitch is good after the first or second iteration, you may want to stop the loop early. In this task, you will update the loop to be able to exit early.

LoopAgent loops can end in a few ways:
A callback function sets tool_context.actions.escalate = True or callback_context.actions.escalate = True (depending on the kind of callback function).
To use the exit_loop tool:

Add the following to your imports at the top of the `adk_multiagent_systems/workflow_agents/agent.py`:

from google.adk.tools import exit_loop

Provide the tool to the critic agent by updating its tools parameter to include this tool:

    tools=[append_to_state, exit_loop],

Add the following to the critic's instruction parameter, after its bulleted list of questions:

    If the PLOT_OUTLINE does a good job with these questions, exit the writing loop with your 'exit_loop' tool.

Give the loop a little more time, if needed, to be exited by changing the max_iterations value to 5 in the writers_room LoopAgent.


In the Terminal, stop the server with CTRL+C.


Tool cards indicating a call to exit_loop

### Task 7. Use a "fan out and gather" pattern for report generation with a ParallelAgent
The ParallelAgent enables concurrent execution of its sub-agents. Each sub-agent operates in its own branch, and by default, they do not share conversation history or state directly with each other during parallel execution.


This is valuable for tasks that can be divided into independent sub-tasks that can be processed simultaneously. Using a ParallelAgent can significantly reduce the overall execution time for such tasks.

In this lab, you will add some supplemental reports -- some research on potential box office performance and some initial ideas on casting -- to enhance the pitch for your new film.
While much of this example demonstrates creative work that would be done by human teams, this workflow represents how a complex chain of tasks can be broken across several sub-agents to produce drafts of complex documents which human team members can then edit and improve upon.

Paste the following new agents and ParallelAgent into your workflow_agents/agent.py file under the # Agents header:
```
box_office_researcher = Agent(
    name="box_office_researcher",
    model=model_name,
        casting_agent
    ]
)
```
Update the film_concept_team agent's sub_agents list to include the preproduction_team between the writers_room and file_writer:

film_concept_team = SequentialAgent(
        file_writer
    ],
)

Update the file_writer's instruction to:

    INSTRUCTIONS:

    CASTING_REPORT:
    {{ casting_report? }}

Save the file.

In the Terminal, stop the server with CTRL+C and then run it again with adk web.

Note: While this system can produce interesting results, it is not intended to imply that instructions can be so brief or adding examples can be skipped. The system's reliability would benefit greatly from the additional layer of adding more rigorous instructions and examples for each agent.

### Custom workflow agents
When the pre-defined workflow agents of SequentialAgent, LoopAgent, and ParallelAgent are insufficient for your needs, CustomAgent provides the flexibility to implement new workflow logic. You can define patterns for flow control, conditional execution, or state management between sub-agents. This is useful for complex workflows, stateful orchestrations, or integrating custom business logic into the framework's orchestration layer.

Creation of a CustomAgent is out of the scope of this lab, but it is good to know that it exists if you need it!

### Congratulations!
In this lab, you’ve learned to:
- Create multiple agents and relate them to one another with parent to sub-agent relationships
- Add to the session state and read it in agent instructions
- Use workflow agents to pass the conversation between agents directly
