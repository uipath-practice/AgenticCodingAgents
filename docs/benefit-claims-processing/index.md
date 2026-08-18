# Benefit Claims Processing

**Build an end-to-end agentic Benefit Claims process — BPMN modelling, IXP document extraction, three AI agents, human validation, and email notification.**

## Overview

Agentic orchestration, implemented in **Maestro**, lets you coordinate long-running enterprise
processes between humans, robots, and AI agents working across different systems of record and
systems of engagement. You design, implement, monitor, operate, and optimize those processes, then
run them at scale.

In this exercise you'll implement a **Benefit Claims** use case from the government sector — the
structured procedure citizens use to request financial or service-based assistance, such as
pensions, social assistance, or unemployment benefits.

<!-- Rows become links as each lesson is authored. An unbuilt link fails `mkdocs build --strict`. -->

| Step | Focus |
| ---: | :--- |
| [**Create BPMN process**](1-create-bpmn-process.md) | Model the end-to-end process on the BPMN canvas |
| [**Setting up the Solution**](2-setting-up-the-solution.md) | Create the agentic automation solution that implements the process |
| [**Configure a Robot**](3-configure-a-robot.md) | Add an RPA automation that uses IXP to read the application PDF |
| [**Residency Verification Agent**](4-residency-verification-agent.md) | Build an agent that checks the declared residency against known records |
| **Income Verification Agent** *(coming next)* | Build an agent that checks the declared income against known records |
| **Eligibility Determination Agent** *(coming next)* | Build an agent that decides eligibility using internal guidelines |
| **Configure human validation** *(coming next)* | Present the agents' conclusions for a case worker to approve or deny |
| **Configure API integration — Benefit Approval** *(coming next)* | Notify the applicant when the claim is approved |
| **Configure API integration — Benefit Rejection** *(coming next)* | Notify the applicant when the claim is rejected |

!!! tip "Training Environment"
    Log in at **[cloud.uipath.com/tpenlabs](https://cloud.uipath.com/tpenlabs)** and remember using tenant **AgenticWorkshop** for this exercise.
