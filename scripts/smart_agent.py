import requests
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

def create_classifier(dataset_file):
  with open(dataset_file, 'r') as fp:
    cl = NaiveBayesClassifier(fp, format='csv')
  return cl

def first_sentence(text):
  blob = TextBlob(text)
  return str(blob.sentences[0])

def bing_search(query):
  url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
  payload = {'q': query}
  headers = {'Ocp-Apim-Subscription-Key': '7e4b37dd090b4ca084fb1526a381b78d'}
  r = requests.get(url, params=payload, headers=headers)
  answer = r.json().get('webPages').get('value')[0].get('snippet')
  return first_sentence(answer)

def initialize_classifiers():
  rasp_cl = create_classifier('minor_project_dataset.csv')
  automat_cl = create_classifier('minor_project_dataset3.csv')
  return rasp_cl, automat_cl

action_cl, automat_cl = initialize_classifiers()

def raspberry_pi_extract_action(query):
  on_stat = 'on'
  select_stat = 'lights'
  if "off" in query:
    on_stat = 'off'
  if "fan" in query:
    select_stat = 'fan'
  return select_stat + ' ' + on_stat

def automat_take_dec(query):
  action = automat_cl.classify(query)
  print("Sending to Raspberry pi. . " + action)
  label_map = {'fan_inc': "increase fan",
               'fan_dec': "decrease fan",
               'light_inc': "brighten lights",
               'light_dec': "dim lights"}
  return label_map[action]

def smart_agent_answer(query):
  act = action_cl.classify(query)
  if act == 'hard_action':
    return raspberry_pi_extract_action(query)
  elif act == 'soft_action':
    return automat_take_dec(query)
  elif act == 'terminate':
    return "Goodbye!"
  else:
    return bing_search(query)

if __name__ == "__main__":
  while True:
    quest = input("UserQuery> ")
    ans = smart_agent_answer(quest)
    print("A> " + ans)
