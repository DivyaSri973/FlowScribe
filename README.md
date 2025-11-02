# FlowScribe

FlowScribe is an agent-driven automation and documentation system. The project runs two cooperating agents:

- The Requesting Agent (Agent A): asks questions about a task and requests the next action.
- The Instruction Agent (Agent B): replies with a step-by-step workflow, including images/visuals for each step and instructions the automation should execute.

This repository uses LangGraph to orchestrate the agent flow and Selenium for web scraping and browser automation. The main goal is to produce reproducible, illustrated workflows that can be executed automatically and captured as documentation.

Table of contents
- Project overview
- Architecture and agent interaction
- Features
- Requirements
- Setup and installation
- Configuration
- How it works (example flow)
- Adding images for steps
- Extending workflows and agents
- Testing & debugging
- Contributing
- License

Project overview
----------------
FlowScribe coordinates a conversation between two agents to convert high-level user requests into concrete, executable automation steps with visual aids.

Typical use cases:
- Convert a manual web task into an automated Selenium script with step images.
- Generate a reproducible onboarding checklist with screenshots for each step.
- Produce documented scraping flows that show what was scraped and how.

Architecture and agent interaction
----------------------------------
- LangGraph orchestrates the flow: it defines nodes representing Agent A and Agent B and the message routes between them.
- Agent A (Requesting Agent)
  - Receives the user's high-level request (for example: "Log into example.com and export the reports for October").
  - Breaks down the request into sub-questions or context and asks Agent B for the next action.
- Agent B (Instruction Agent)
  - Receives a prompt from Agent A and returns:
    - A short actionable instruction for the automation engine (Selenium-friendly).
    - A descriptive, human-friendly step explanation suited for documentation.
    - An image (or instructions to capture an image) showing the step's UI state.
  - May also return error handling and verification steps.
- Execution loop:
  1. Agent A asks Agent B "What is the next step?"
  2. Agent B responds with the step, text description, and image metadata (or a base64 image).
  3. The automation layer (Selenium) executes the step and captures a screenshot (if requested).
  4. The result (success/failure and screenshot) is fed back to Agent A and the next iteration begins until the task completes.

Features
--------
- Orchestrated agent conversation using LangGraph.
- Selenium-based automation and web scraping.
- Automatic screenshot capture and attachment to step documentation.
- Human-readable documentation generated from each step's description and images.
- Extensible node-based flow (add new agent behaviors / flow nodes easily).

Requirements
------------
- Python 3.9+ (or another language runtime if you implement agents separately)
- Selenium (e.g., selenium==4.x)
- WebDriver for your target browser (ChromeDriver, geckodriver, etc.)
- LangGraph (install per LangGraph docs; pip/JS client depending on language)
- Optional: Pillow or image libs for processing screenshots
- Internet access for web scraping targets and any external LLM or agent services

Setup and installation
----------------------
1. Clone the repo
   git clone https://github.com/DivyaSri973/FlowScribe.git
   cd FlowScribe

2. Create & activate a virtual environment (Python example)
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows

3. Install dependencies (example Python requirements)
   pip install -r requirements.txt

   Example requirements.txt entries:
   - selenium>=4.0.0
   - langgraph-client   # replace with the actual LangGraph client package if published
   - pillow

4. Install WebDriver
   - Chrome: download chromedriver and add to PATH
   - Firefox: download geckodriver and add to PATH

Configuration
-------------
- LangGraph: create a flow definition that includes two nodes (RequestingAgent, InstructionAgent) and the channels between them.
- Agents: configure agent prompts, model endpoints, or local models as needed.
- Selenium: configure browser options, headless mode, and screenshot size.
- Add environment variables for credentials, API keys, and endpoints:
  - LANGGRAPH_API_KEY
  - LLM_API_KEY (if using a separate LLM provider)
  - SELENIUM_DRIVER_PATH

How it works (example flow)
---------------------------
Below is a high-level sequence for an example "Export report" request:

1. User provides a high-level goal to Agent A:
   - "Log into https://example.com, navigate to Reports → Monthly, select October, and export CSV."

2. Agent A normalizes the request and asks Agent B:
   - "Given the goal, what is the first step to perform in the browser? Provide an actionable step, a human description, and whether a screenshot is needed."

3. Agent B responds with a structured message:
   - step_action: "Go to https://example.com/login and enter credentials (username, password) and click 'Sign in'."
   - doc_text: "Open the login page, enter credentials in the top-right form, and sign in."
   - screenshot: true
   - image_instructions: "Capture full-page screenshot after login button click."

4. The Selenium executor runs the step_action, captures the screenshot as instructed, and returns success + image path to Agent A.

5. Agent A passes the result context to Agent B and asks for the next step until the full task completes.

Message contract (example JSON)
-------------------------------
Agent B should return a JSON-like payload for each step. Example:
{
  "step_id": 1,
  "step_action": "click|css=#reports-nav; wait|css=.monthly-report",
  "doc_text": "Open Reports menu and select 'Monthly' report.",
  "screenshot": true,
  "image_filename": "step-01-reports-open.png",
  "verification": "selector:.monthly-report-table exists"
}

Adding images for steps
-----------------------
- Images can be:
  - Captured by Selenium during execution (recommended).
  - Provided by Agent B as base64-encoded images when describing UI (less common).
- Recommended naming: step-<zero-padded-step-number>-short-desc.png (e.g., step-01-login.png).
- Store images in a /docs/images or /artifacts/<run-id>/images directory so multiple runs don't overwrite each other.

Extending workflows and agents
------------------------------
- Add nodes to the LangGraph flow to implement:
  - Error handling agent (provides retries and fallbacks).
  - Screenshot annotator (draws boxes or highlights on screenshots).
  - Result summarizer (creates a final human-friendly report).
- To add new capabilities in Agent B, update its prompt template to include:
  - Required output schema (step_action, doc_text, screenshot, verification).
  - Allowed action primitives for the automation layer (click, fill, wait, goto, scroll, screenshot).
- If you need richer visuals: integrate a small image-generation or markup agent that annotates screenshots with step labels.

Testing & debugging
-------------------
- Unit-test the action parser that converts Agent B's step_action into Selenium commands.
- Use a "dry-run" mode where actions are validated but not executed (Selenium runs in a fake/stubbed environment).
- Log each agent message and the Selenium command stream; persist logs per-run.
- When a step fails, include the failure details and the last screenshot in the feedback to Agent B so it can suggest recovery steps.

Example local run (pseudo-commands)
----------------------------------
1. Start LangGraph flow (refer to langgraph/flow definition file)
2. Start the executor (connects LangGraph -> Selenium)
   python run_executor.py --flow=flows/login_export.flow --run-id=2025-11-02-01
3. Watch logs in artifacts/2025-11-02-01/ and images in artifacts/2025-11-02-01/images/

Security and privacy
--------------------
- Never store plaintext credentials in source control. Use secret managers or environment variables.
- Be careful scraping sites: honor robots.txt and the site's terms of service.
- If you capture personal data in screenshots, redact or store securely.

Roadmap / Next steps
--------------------
- Provide example LangGraph flow definitions for common tasks (login & export, scrape table, create account).
- Add a small demo that runs end-to-end on a test site (with test accounts).
- Add a visual report generator that combines steps + images into a PDF or markdown runbook.
- Add support for video capture of flows in addition to screenshots.

Contributing
------------
Contributions are welcome! Please:
1. Open an issue describing the feature or bug.
2. Fork the repo, create a feature branch, and open a PR with tests and documentation.

License
-------
Specify a license (e.g., MIT). If you want to keep things permissive, add an MIT LICENSE file.

Acknowledgements
----------------
- LangGraph — for flow orchestration.
- Selenium — for browser automation and screenshot capture.

Contact
-------
Maintainer: DivyaSri973
Repository: https://github.com/DivyaSri973/FlowScribe

Notes
-----
- This README outlines the intended design and integration points: LangGraph for the agent flow, two cooperating agents (requesting and instruction), and Selenium for execution and image capture. Implementations (prompt design, JSON schema, LangGraph flow definitions, and Selenium executor) should be added to the repository as code, configuration, and example assets.
