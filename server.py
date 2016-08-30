import os, requests, json, string, datetime
from flask import Flask, request, jsonify, render_template
import wdc_services, orchestrator

app = Flask(__name__)

#try:
#    load_dotenv(find_dotenv())
#except Exception:
#    print ('warning: no .env file loaded')

# Externalized customizations --------------------
BOT_NAME = 'Watson'
WATSON_IMAGE = 'watson.jpg'
WATSON_STYLE = 'chat-watson'
HUMAN_STYLE = 'chat-human'
CHAT_TEMPLATE = 'IBM-style-dialog.html'
QUESTION_INPUT = 'response-input'
PERSONA_NAME = 'User'
PERSONA_IMAGE = 'watson.jpg'
# Reset conversation -----------------------------
POSTS = []
CONVERSATION_CONTEXT = ''
CONVERSATION_PAYLOAD = ''

class Post:
    def __init__(self, style, icon, text, datetime, name):
        self.style = style
        self.icon = icon
        self.text = text
        self.datetime = datetime
        self.name = name

def post_watson_response(response):
    global WATSON_IMAGE, POSTS, HUMAN_STYLE, WATSON_STYLE
    print('Inside post_watson_response')
    now = datetime.datetime.now()
    post = Post(WATSON_STYLE, WATSON_IMAGE, response, now.strftime('%Y-%m-%d %H:%M'), BOT_NAME)
    POSTS.append(post)
    return post

def post_user_input(input):
    global POSTS, HUMAN_STYLE, WATSON_STYLE, PERSONA_IMAGE, PERSONA
    print('Inside post_user_input')
    now = datetime.datetime.now()
    post = Post(HUMAN_STYLE, PERSONA_IMAGE, input, now.strftime('%Y-%m-%d %H:%M'), PERSONA_NAME)
    POSTS.append(post)
    return post

def format_application_response_as_string(response_strings):
    print('Inside format_conversation_response_as_string')
    response = ''
    if response_strings:
        for response_string in response_strings:
            if str(response_string) != '':
                if len(response) > 0:
                    response = response + '<BR>' + response_string
                else:
                    response = response_string
    return response


# Functions in external modules ------------------
get_application_response = orchestrator.get_application_response
get_application_start_response = orchestrator.get_application_start_response

@app.route('/')
def Index():
    global POSTS, CONVERSATION_CONTEXT, CONVERSATION_PAYLOAD, CHAT_TEMPLATE
    print('Inside GET')
    POSTS = []
    CONVERSATION_CONTEXT = ''
    CONVERSATION_PAYLOAD = ''
    final_response = ''
    response = get_application_start_response()
    if response != None:
        CONVERSATION_CONTEXT = response['context']
        CONVERSATION_PAYLOAD = response
        final_response = format_application_response_as_string(response['output']['text'])
    post_watson_response(final_response)
    return render_template(CHAT_TEMPLATE, posts=POSTS)

@app.route('/', methods=['POST'])
def Index_Post():
    global POSTS, CONVERSATION_CONTEXT, CONVERSATION_PAYLOAD, CHAT_TEMPLATE, QUESTION_INPUT
    print('Inside POST')
    question = request.form[QUESTION_INPUT]
    post_user_input(question)
    final_response = ''
    application_response = get_application_response(CONVERSATION_CONTEXT, question)
    if application_response != None:
        CONVERSATION_CONTEXT = application_response['context']
        CONVERSATION_PAYLOAD = application_response
        final_response = format_application_response_as_string(application_response['output']['text'])
    post_watson_response(final_response)
    return render_template(CHAT_TEMPLATE, posts=POSTS)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(port))
