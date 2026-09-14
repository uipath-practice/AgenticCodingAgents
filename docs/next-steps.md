# Next Steps

!!! tip "Congratulations!"
    You've completed the Agentic Automation Workshop — from your first CLI command to a live,
    running Benefit Claims process built with **Maestro**, **IXP**, three AI agents, and a coding
    agent.

## What you built

Across this workshop you set up your coding agent environment, practiced driving the platform from
the terminal, and used both hands-on clicking and a coding agent to build an end-to-end **Benefit
Claims Processing** solution — an agentic process that verifies a citizen's benefits application
and routes it to a human for the final call.

| Component | Role |
| :--- | :--- |
| **UiPath CLI** and skills | The interface and instruction packs that let a coding agent build on UiPath |
| **Agentic Process** (Maestro) | Orchestrates the end-to-end claims process across robots, agents, and humans |
| **RPA robot with IXP** | Extracts structured data from the benefits application PDF |
| **Residency Verification Agent** | Checks the declared residency against known records |
| **Income Verification Agent** | Checks the declared income against known records — built either with a coding agent or by hand in Studio Web |
| **Eligibility Determination Agent** | Decides eligibility using internal guidelines |
| **Action App** | Presents the agents' conclusions for a case worker to approve or deny |
| **API integrations** | Notify the applicant by email once the claim is approved or rejected |

## Next steps

### 1. Keep building with a coding agent

If you built the Income Verification Agent manually, go back and try the coding agent path — or
pick another agent in the process and rebuild it the other way. The fastest way to get comfortable
is to keep switching between describing outcomes to your coding agent and configuring things by
hand, until reaching for the CLI feels as natural as clicking through Studio Web.

### 2. Extend the process

Nothing about this process is final. Add a guardrail to one of the agents, tighten a prompt after
watching it misfire on an edge case, or add a fourth verification check of your own. Small,
incremental changes are the fastest way to build intuition for how these agents actually behave.

## Keep iterating

**Ask for outcomes, not commands**

- Describe what you want the agent to do and let it choose the `uip` commands. It gets easier the more you do it.

**Evaluate before you trust**

- Before relying on any agent's decision in production, build out its evaluation set. A few good test cases catch more regressions than hours of manual testing.

**Trust the model**

- Don't over-optimize for tokens early. A stronger model often costs less overall because it makes fewer mistakes.

## Learn more

| Resource | Description |
| :--- | :--- |
| [IXP documentation](https://docs.uipath.com/ixp/automation-cloud/latest/user-guide/introduction) | Intelligent document extraction used by the RPA robot |
| [Agent tools](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-tools) | How agents call RPA workflows, APIs, and other agents |
| [Agent evaluations](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-evaluations) | Building evaluation sets and evaluators |
| [Context Grounding](https://docs.uipath.com/automation-cloud/automation-cloud/latest/admin-guide/about-context-grounding) | Anchoring an agent's answers to your own data |
| [Using UiPath CLI with Coding Agents](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/coding-agents) | Per-agent setup walkthroughs |
| [uip skills reference](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/uip-skills) | Full command and flag reference |
| [UiPath/skills (GitHub)](https://github.com/uipath/skills) | The source of the UiPath skills |
