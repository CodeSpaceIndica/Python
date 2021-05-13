from flask import Flask, request
from flask.wrappers import Response
import requests 
import json
import re
import datetime
app = Flask(__name__)

token = '<BOT_ID>'

# https://api.telegram.org/bot<BOT_ID>/getMe
# https://api.telegram.org/bot<BOT_ID>/setWebhook?url=https://5540d4801e1f.ngrok.io/

def write_json(data, filename='resp.json'):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def parse_mesg(message):
    chat_id = ''
    text = ''

    if 'message' in message.keys():
        chat_id = message['message']['chat']['id']
        text = message['message']['text']
    else:
        chat_id = message['edited_message']['chat']['id']
        text = message['edited_message']['text']
            
    pattern = r'^/\d{6}$'
    matches = re.findall(pattern, text)

    pincode=''
    if matches:
        pincode = matches[0][1:]
    
    return chat_id, pincode

def send_message(chat_id, msg):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id':chat_id, 'text':msg}
    requests.post(url, json=payload)
    
def get_slots(pincode, dt):
    slots = []
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?'
    q = f'pincode={pincode}&date={dt}'

    resp = requests.get(url+q, headers=
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'})

    print(resp.status_code)

    if resp.ok:
        data = json.loads(resp.text)

        for slot in data['sessions']:
            cname = slot['name']
            cap = slot['available_capacity']
            age = slot['min_age_limit']
            vax = slot['vaccine']
            slots.append([cname, cap, age, vax])
    else:
        print("trouble")
        
    return slots

@app.route('/', methods=['POST'])
def hello_world():

    if request.method == "POST":
        # TODO 
        mesg = request.get_json()
        
        chat_id, pin = parse_mesg(mesg)

        if pin == '':
            msg = "Incorrect command format. Send /<6 digit pincode>"
            send_message(chat_id, msg)            
            # wrong command format
            
        else:
            #hit cowin api  
            title = "Date   " + "Center Name  " + "Availability  " + "Age limit " + "Vaccine"
            send_message(chat_id, title)
            for i in range(5):
                today = datetime.date.today()+datetime.timedelta(days=i)
                today = today.strftime('%d-%m-%Y') 
                print(pin, today)
                slots = get_slots(pin, today)

                if len(slots) == 0:
                    send_message(chat_id, 'No slots found')
                else:
                    for slot in slots:
                        slotinfo = " | ".join(map(str, slot)) 
                        send_message(chat_id, today+ " " + slotinfo)
                        

        return Response('ok', status=200)
