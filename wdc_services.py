import os, requests, json, string, datetime, csv
from watson_developer_cloud import ConversationV1

SOLR_CLUSTER_ID = 'XXXXX'
RANKER_ID = 'XXXXX'
RETRIEVE_AND_RANK_USERNAME = 'XXXXX'
RETRIEVE_AND_RANK_PASSWORD = 'XXXXX'
COLLECTION_NAME = 'XXXXX'
SOLR_RETURN_FIELDS = 'XXXXX'
SOLR_RETURN_ROWS = 'XXXXX'
CONVERSATION_ID = 'XXXXX'
CONVERSATION_USERNAME = 'XXXXX'
CONVERSATION_PASSWORD = 'XXXXX'

if 'SOLR_CLUSTER_ID' in os.environ:
    SOLR_CLUSTER_ID = os.environ['SOLR_CLUSTER_ID']
if 'RANKER_ID' in os.environ:
    RANKER_ID = os.environ['RANKER_ID']
if 'VCAP_SERVICES' in os.environ:
    retrieve_and_rank = json.loads(os.environ['VCAP_SERVICES'])['retrieve_and_rank'][0]
    RETRIEVE_AND_RANK_USERNAME = retrieve_and_rank["credentials"]["username"]
    RETRIEVE_AND_RANK_PASSWORD = retrieve_and_rank["credentials"]["password"]

if 'CONVERSATION_ID' in os.environ:
    CONVERSATION_ID = os.environ['CONVERSATION_ID']
if 'VCAP_SERVICES' in os.environ:
    conversation = json.loads(os.environ['VCAP_SERVICES'])['conversation'][0]
    CONVERSATION_USERNAME = conversation["credentials"]["username"]
    CONVERSATION_PASSWORD = conversation["credentials"]["password"]

conversation = ConversationV1(
  username=CONVERSATION_USERNAME,
  password=CONVERSATION_PASSWORD,
  version='2016-07-11'
)

def WDC_get_retrieve_and_rank_response(args_string):
    global SOLR_CLUSTER_ID, RANKER_ID, RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD
    print('Inside wdc_get_retrieve_and_rank_response')
    POST_SUCCESS = 200
    url = 'https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/' + SOLR_CLUSTER_ID + '/solr/'+ COLLECTION_NAME + '/select?q=' + args_string + '&rows='+SOLR_RETURN_ROWS+'&wt=json&fl=' + SOLR_RETURN_FIELDS
    response = requests.get(url, auth=(RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD), headers={'content-type': 'application/json'})
    print('Response from wdc_get_retrieve_and_rank_response')
    print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    if response.status_code == POST_SUCCESS:
        return response.json()
    return None

def WDC_get_conversation_response(context, input):
    global CONVERSATION_ID, CONVERSATION_USERNAME, CONVERSATION_PASSWORD
    print('Inside wdc_get_conversation_response')
    POST_SUCCESS = 200
    response = ''
    context = context
    response = conversation.message(
        workspace_id=CONVERSATION_ID,
        message_input={'text': input},
        context=context
    )
    print('Response from wdc_get_conversation_response')
    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
    return response

def WDC_get_conversation_start_response():
    global CONVERSATION_ID, CONVERSATION_USERNAME, CONVERSATION_PASSWORD
    print('Inside wdc_get_conversation_start_response')
    context = {}
    response = conversation.message(
        workspace_id=CONVERSATION_ID,
        message_input={'text': ''},
        context=context
    )
    print('Response from wdc_get_conversation_start_response')
    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
    return response
