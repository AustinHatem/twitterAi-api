import openai
from fastapi import FastAPI, Path
import os

app = FastAPI()

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = os.environ.get('OPENAIKEY')
FINE_TUNED_MODEL = 'davinci:ft-personal-2022-12-15-22-49-18'
TEMP = 0.7

def gpt3_completion(prompt, engine='text-davinci-003', temp=TEMP, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['END']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        model=FINE_TUNED_MODEL,
        # engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text




@app.get('/')
def home():
    return {"Data" : "Testing"}

@app.get("/about")
def about():
    return {"Data" : "About"}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The Id of the item you'd  like to view", gt=0, lt=2)):
    return {"data" : item_id}

@app.get("/get-tweet")
def get_item(topic: str):
    # user_input = input('Write A Tweet about: ')
    prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', topic)
    response = gpt3_completion(prompt)
    return {"data" : response}