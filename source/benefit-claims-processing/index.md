<!-- Harvested from https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing
     Images: staging/images/_exercise-index/ (0 found)
     <<IMG:n>> marks where image n appeared in the original page. -->

# Benefit Claims Processing

Agentic orchestration, implemented in Maestro, empowers enterprise customers to coordinate their long-running enterprise processes between humans, robots, and AI agents, working seamlessly across different systems of records and systems of engagement. With agentic orchestration, customers are able to design, implement, monitor, operate, and optimize their long-running processes and operate them at scale.

During this exercise, we are going to implement a Benefit Claims use case, from the government sector. This is typically a structured procedure used by citizens to request financial or service-based assistance (eg. pensions, social assistance, unemployment benefits etc.)

Here is the plan:

1. [Create BPMN diagram](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/create-bpmn-process) for our end-to-end process
2. [Setting up the agentic automation solution](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/setting-up-the-solution) to implement the process.
3. [Add an RPA Automation](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-a-robot) which uses IXP, to retrieve information from the benefits application PDF document.
4. [Build an Agent that checks the declared applicant residency](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/residency-verification-agent) against known records.
5. [Build an Agent that checks the declared applicant income](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/income-verification-agent) against known records.
6. [Build an Agent that decides if the applicant is eligible for benefits](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/eligibility-determination-agent), using internal guidelines.
7. [Create a human validation step](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-human-validation), to present the agents conclusions, for the human to decide whether to approve the benefits claim or not
8. [Notify the applicant in case of benefits approval](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-api-integration-benefit-approval)
9. [Notify the applicant in case of benefits rejection](https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-api-integration-benefit-rejection)
