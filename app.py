from flask import Flask, request, jsonify, render_template
import os
import dialogflow_v2
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, send_from_directory
import google 
from flask_cors import CORS,cross_origin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'##json credentials
DIALOGFLOW_PROJECT_ID = '<DIALOGFLOW_PROJECT_ID>'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'


app = Flask(__name__, static_folder='react-chatbot-dialogflow/build')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'] , echo=True)
Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy(app)
#to avoid cors problems
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'



#Log Table
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_text = db.Column(db.Text())
    is_bot = db.Column(db.Integer())
    created_at = db.Column(db.Integer(), server_default="(strftime('%s','now')")

#Truck Table
class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100))
    truck_number = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "⛟ : "+self.manufacturer+", "+self.model+", "+self.color+", N° "+self.truck_number 


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# webhook triggered after dialogflow variables are filled and received a confirmation of the query from user
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    query_object=data['queryResult']['outputContexts'][1]['parameters']
    res=[]
    #since the color variable is not required in dialogflow so it will be used in the query only if it's filled
    if query_object['color'] == '':
        res=Truck.query.filter_by(manufacturer=query_object['manufacturer'], model=query_object['model']).all()
    else:
        res=Truck.query.filter_by(manufacturer=query_object['manufacturer'], model=query_object['model'], color=query_object['color']).all()

    message="There are no trucks with the provided specs"
    #To render the Truck object we call str function
    #which returns the string representation defined earlier in __repr__
    if len(res)>0:
        message="Found trucks:"+';'.join(map(str, res))   
    reply = {
            "fulfillmentText": message,
        }
    return jsonify(reply)

#Query dialogflow API to get response
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow_v2.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow_v2.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

#Log messages in db
def log_message(message, is_bot):
    log= Log(message_text = message, is_bot=is_bot)
    session.add(log)
    session.commit()

#Endpoint receiving and responding to chat messages from the user
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.get_json(silent=True)['message']
    log_message(message, 0)
    fulfillment_text = detect_intent_texts(DIALOGFLOW_PROJECT_ID, "unique", message, 'en')
    log_message(fulfillment_text, 1)
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run( debug=True, host='0.0.0.0')
