<!-- Harvested from https://sites.google.com/uipath.com/agentic-automation/benefit-claims-processing/configure-api-integration-benefit-rejection
     Images: staging/images/9-configure-api-integration-benefit-rejection/ (9 found)
     <<IMG:n>> marks where image n appeared in the original page. -->

# Update external systems using API - Benefit Rejection Case

## Integration Service

Key steps in this lesson:

- **Generate benefits rejection email using Gen AI**

- **Send the email to the benefits applicant**. We are going to use an Integration Service GMail connector.

Let's configure the tasks in the workflow accordingly.

## 1. Integration Service with Gen AI Connector

**UiPath** [Integration Service](https://docs.uipath.com/integration-service/automation-cloud/latest/user-guide/introduction) is the fastest and most convenient way to automate API enabled applications. It takes care about authorization and authentication, helping you centralize management of API connections and also allowing faster integration into SaaS platforms.

Let's see what we have prepared:

<<IMG:1>>

There are 3 connections available:

- **Gmail Connection** that we can use to send emails
- **Data Fabric Connection** where we can store any type of data (tables, files, etc.)
- **GenAI Connection** which we will use to generate emails using LLMs.

Good part: we don't need to worry about credentials or permissions today - platform administrators have prepared these for our automation, and they are also taking care about securing and restricting access to these.

Note: make sure you are using the right tenant, or contact your trainer if there are issues with connections.

Let's configure the **Generate Rejection Email** task in Maestro, for this, we are going to use the [UiPath GenAI Activities](https://docs.uipath.com/activities/other/latest/integration-service/uipath-uipath-airdk-about). Specifically the [Generate Email](https://docs.uipath.com/activities/other/latest/integration-service/uipath-airdk-airdk-generate-email) activity.

- Action will be "**Execute Connector Activity**"
- Pick the UiPath GenAI Activities connector and configure the **GenAI Connection**
- Select the **Generate Email** activity

<<IMG:2>>

<<IMG:3>>

Next, let's configure the following input properties:

- Include salutation - **true**
- Salutation - **Greetings**
- Include sign-off: **true**
- Sign-off: **Regards**
- Sign-off name: **Benefits Claims Department**
- Email content (**JS Expression**): **"Generate an email notifying the recipient that their application for benefits has been denied, for the following reason: "+vars.denialReason**
- Model: **gpt-5 . 1**
- Saluation name: **Applicant**
- Style: **Concise**
- Output format: **HTML**

Once we have the generated email, we can send it to the applicant using the GMail connector. Let's configure the **Send Rejection Email** task.

- Action will "**Execute Connector Activity**"
- Pick the **Gmail Connector** and select the [uipathlabs@gmail.com](mailto:uipathlabs@gmail.com) connection
- Pick the **Send Email** activity

<<IMG:4>>

<<IMG:5>>

Let's configure the activity properites:

- To**:** we are going to use the **in_EmailAddress** argument from the start event
- Subject: **Benefits Application Rejected**
- Body: the **emailContent** output variable from the **Generate Rejection Email** task

<<IMG:6>>

<<IMG:7>>

Time to test the rejection scenario! Configure the debug values of the BPMN process as in the picture below, in the **Case Worker Review** action center task, **reject** the benefits application.

In the debug panel, pass the following argument values:

- in_emailAddress - **your own email adddress**
- in_ExamplePaystub - **Sample pay stub.png**
- in_Application - **Sample application.pdf**

<<IMG:8>>

Once the execution of the process is completed, you should recieve the benefits rejection email:

<<IMG:9>>
