# Simple Conversation UI Overview

The Python based application demonstrates a simple web application that interacts with the Watson conversation service. The application allows a user to interact with a conversation workspace using a basic chat user interface. The application also includes an integration to Watson Retrieve and Rank to gather/present a list of Solr results in cases where the conversation service dialog flow flags the application to integrate the results.

Application assumes you have an existing conversation service in Bluemix with a developed workspace

## Application Structure

- `server.py` : Main entry point to the application. Sets up server and endpoint handlers. Receives requests from UI, calls scripts to gather responses, which it then normalizes/formats.
- `orchestrator.py` : Handles orchestration of requests/responses between conversation and R&R.
-  `wdc_services.py` : Wrapper for conversation service and R&R service integration. Conversation service is called using the watson-developer-cloud python sdk, while R&R is called using REST APIs. The wrapper contains the service credential and instance id information needed to call the services.

## Run the app locally

1. Install Python
2. Download and extract this code 
3. cd into the app directory
4. Install dependencies using `pip`

    ```sh
    pip install -r requirements.txt
    ```
5. Modify the wdc_services.py file to include the appropriate service/instance information. At minimum, the CONVERSATION_USERNAME, CONVERSATION_PASSWORD and CONVERSATION_ID (same as workspace id) need to be updated.
6. Run `python server.py`
5. Access the running app in a browser at http://localhost:5000

