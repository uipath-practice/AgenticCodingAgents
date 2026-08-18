<!-- Harvested from https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-human-validation
     Images: staging/images/7-configure-human-validation/ (13 found)
     <<IMG:n>> marks where image n appeared in the original page. -->

# Add an Action App for human validation

## Involving humans only when necessary

Key steps in this lesson

1. Add validation Action App to our project.
2. Configure process flow for humans to review the documents submitted by the applicant and the decisions made by the agents
3. Based on App Action direct flow further.

## 1. Humans in the loop

In many cases where Agent can not determine exact course of action, or when double checking is ncesessary, Human involvement is required. Humans process task in Action Center using the conveniently summarized inputs from Robots/Agents:

- all inputs required to make a decision should be presented on one screen: ideally we don't want business users to open applications or go back and review execution flow.
- agent's and robot's job is to prepare all inputs in the right format, so that when time comes to ask user inputs, it's ready.
- once a decision is made - our Process execution continues to next steps.

Let's plan the Action's structure:

<<IMG:1>>

In short, we need a nice frontend for the user, where the agent decisions along with necessary information is presented to make a decision.

Do you think this kind of form will be helpful for a business user to speed up processing time? Any opportunity to improve it?

<<IMG:2>>

Let's build it!!! Well.. it will take a lot of time, so .. maybe let's just take a look at the already built app and discuss it.

## 2. Review the Action App

<<IMG:3>>

<<IMG:4>>

## 3. Adding Human validation task

Let's open Agentic Process again and configure the validation task as **Action App Task**:

<<IMG:5>>

<<IMG:6>>

- Make sure to **customize your Task Title,** so that it's easier to identify our tasks in Action Center later.
- In the Assignment section, **assign the task to yourself**. Otherwise you will need to locate the task in a pool of all unassigned tasks.

<<IMG:7>>

Let's pass the following inputs to the action app:

- Summary - Justification (from Eligibility Determination Agent)
- EligibilityStatus - Conclusion (from Eligibility Determination Agent)
- Calculation - Calculation (from Eligibility Determination Agent)
- FraudResidencyRisk - ResidencyValidationDecision (from Residency Verification Agent)
- FraudResidencyExplanation - rationale (from Residency Verification Agent)
- FraudIncomeRisk - decision (from Income Verification Agent)
- FraudIncomeExplanation - rationale (from Income Verification Agent)
- ApplicationFilePath - in_Application (from the input arguments)
- PaystubFilePath - in_ExamplePaystub (from the input arguments)

## 4. Configure Exclusive Gateway decision

One last step in this lesson - let's configure the downstream flow based on validation decision:

<<IMG:8>>

<<IMG:9>>

Let's **set " No " as default path** (noting that real business process might have different approach).

Then in Expression Editor pick "Action" output, which as per App settings can be "Approve" or "Reject".

Here is what we want:

<<IMG:10>>

Testing time! Now click on Debug button and monitor the execution.

<<IMG:11>>

Processing stopped until decision is made. Click "**Open app task**" link or find task in **Action Center**:

<<IMG:12>>

As soon as task is processed, Maestro continues the execution, in this case the outcome was "Deny":

<<IMG:13>>
