import os, requests, json, string, datetime, csv
import wdc_services

INTERCEPT_FLAG_NAME = 'callRetrieveAndRank'

WDC_get_conversation_response = wdc_services.WDC_get_conversation_response
WDC_get_conversation_first_response = wdc_services.WDC_get_conversation_start_response
WDC_get_retrieve_and_rank_response = wdc_services.WDC_get_retrieve_and_rank_response

def get_enrichment_data(response, question):
    print('Inside get_enrichment_data')
    rnr_resp = WDC_get_retrieve_and_rank_response(question)
    application_response = response
    if (rnr_resp != None):
        print("Number of documents to process from retrieve and rank %d" % len(rnr_resp))
        if(len(rnr_resp) > 0):
            #Remove the default conversation response
            application_response['output']['text'].pop()
        for docs in rnr_resp['response']['docs']:
            docOut = '<b>Title: </b>' + docs['title'] + '<br>'+ docs['body'][:75] +'....... <a href="' + docs['sourceUrl'] +'">Visit Answer</a><br>'
            application_response['output']['text'].append(docOut)

    return application_response

def intercept_requested(response):
    global INTERCEPT_FLAG_NAME
    print('Inside intercept_requested')
    cont = response['context']
    if(cont.has_key(INTERCEPT_FLAG_NAME)):
        if (response['context'][INTERCEPT_FLAG_NAME]):
            return True
    return False

def enrich_application_response(response, question):
    print('Inside enrich_application_response')
    application_response = response
    if (intercept_requested(response)):
        application_response = get_enrichment_data(application_response, question)
        application_response['context'][INTERCEPT_FLAG_NAME] = False
    return application_response

def get_application_response(context, question):
    print('Inside get_application_response')
    response = WDC_get_conversation_response(context, question)
    application_response = enrich_application_response(response, question)
    return application_response

def get_application_start_response():
    print('Inside get_application_start_response')
    response = WDC_get_conversation_first_response()
    return response
