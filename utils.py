from gnewsclient import gnewsclient
client = gnewsclient.NewsClient(max_results=5)

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client.json'

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = 'newsbot-usgg'

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return 'get_news', dict(response.parameters)
    return 'small_talk', response.fulfillment_text

def fetch_news(params):
    print(params)
    if params.get('language') != '':
        client.language = params.get('language')
    if params.get('geo-country') != '':
        client.location = params.get('geo-country')
    if params.get('topic') != '':
        client.topic = params.get('topic')[0]

    print(client.get_config())
    return client.get_news()

topics_keyboard = [
    ['Top Stories', 'World', 'Nation'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science', 'Health']
]
    

if __name__ == '__main__':
    response = detect_intent_from_text('fetch me some national news', 12345)
    print(response.intent.display_name)
    print(dict(response.parameters))