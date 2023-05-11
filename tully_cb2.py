import openai
import csv
import json
import datetime
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RealEstateChatbot:
    def __init__(self):
        data_file='/Users/amarahmed/Desktop/reelTour_/response_status_active_filter_tcb_res.json'
        with open(data_file) as file:
            data = []
            for line in file:
                data.append(json.loads(line))
        # self.df = pd.json_normalize(data, 'value')
        self.df = pd.json_normalize(data)
        self.df['MajorChangeTimestamp'] = pd.to_datetime(self.df['MajorChangeTimestamp']).astype(int) / 10**9  # replace 'date_column' with the name of your date column
        #self.df['ListAgentDirectPhone'] = pd.to_datetime(self.df['ListAgentDirectPhone']).astype(int) / 10**9  # replace 'date_column' with the name of your date column
        self.df = self.df.drop(columns=['ListAgentDirectPhone'])  # replace 'phone_number_column' with the name of your phone number column
        self.df = self.df.drop(columns=['ListAgentEmail'])  # replace 'phone_number_column' with the name of your phone number column
        self.df = self.df.drop(columns=['ListAgentFullName'])  # replace 'phone_number_column' with the name of your phone number column

        self.df1 = self.df.iloc[:,:58]
        self.df1 = self.df1.fillna(0)
        self.df_new = self.df1.iloc[:,1:]
        openai.api_key = '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'

    def start_chat(self):
        response = openai.Completion.create(engine="text-davinci-003", prompt="As a person talking natrually asking to help find a home ask about what they are looking for in less than 10 words", max_tokens=60)
        print(self.df_new.shape) 
        print("Chatbot: " + response.choices[0].text.strip())
        data_file='/Users/amarahmed/Desktop/reelTour_/response_status_active_filter_tcb_res.json'
        
        #using csv
        #self.df = pd.read_csv(data_file, encoding='utf-8')

        #using json
        with open(data_file) as file:
            data = []
            for line in file:
                data.append(json.loads(line))
        # self.df = pd.json_normalize(data, 'value')
        self.df = pd.json_normalize(data)

        while True:
            user_input = input().lower()
            self.handle_user_input(user_input)


    def handle_user_input(self, input):
        keywords = input.split()
        #matches = [record for record in self.df if any(keyword in record['ACT_AddressInternet'].lower() for keyword in keywords)]
        matches = [record for record in self.df.to_dict('records') if any(keyword in (record.get('ACT_AddressInternet') or '').lower() for keyword in keywords)]
        if matches:
            response = openai.Completion.create(engine="text-davinci-003", prompt="As a friendly chatbot respond to user after finding something for them", max_tokens=60)
            print("Chatbot: " + response.choices[0].text.strip())
            for match in matches[:2]:
                formatted_match = json.dumps({
                    'ACT_AddressInternet': match['ACT_AddressInternet'],
                    'ListPrice': match['ListPrice'],
                    'BedroomsTotal': match['BedroomsTotal'],
                    'BathroomsFull': match['BathroomsFull']
                }, indent=4)
                print(formatted_match)
                
            # Adding the cosine similarity logic here
            user_inputs = [int(keyword) for keyword in keywords if keyword.isdigit()]
            user_interactions = np.array(user_inputs)
            similarity_scores = cosine_similarity(user_interactions.reshape(1, -1), self.df_new)
            recommended_items = np.argsort(similarity_scores)[0][::-1]  # reverse sort order
            for item in recommended_items:
                similarity_percent = similarity_scores[0][item] * 100
                if(similarity_percent >= 70):
                    print(f'{self.df1.iloc[item,0]},  ({similarity_percent:.2f}%)')
                    
        else:
            response = openai.Completion.create(engine="text-davinci-003", prompt="I'm sorry, I couldn't find any properties that match your criteria. Could you provide more details or try different keywords?", max_tokens=60)
            print("Chatbot: " + response.choices[0].text.strip())
        self.continue_chat()

    def continue_chat(self):
        response = openai.Completion.create(engine="text-davinci-003", prompt="Is there anything else you'd like to search for?", max_tokens=60)
        print("Chatbot: " + response.choices[0].text.strip())
        user_input = input().lower()
        if 'no' in user_input:
            current_hour = datetime.datetime.now().hour
            if current_hour < 12:
                response = openai.Completion.create(engine="text-davinci-003", prompt="Alright, have a great morning! Looking forward to hearing from you.", max_tokens=60)
                print("Chatbot: " + response.choices[0].text.strip())
            elif 12 <= current_hour < 18:
                response = openai.Completion.create(engine="text-davinci-003", prompt="Alright, have a great afternoon! Looking forward to hearing from you.", max_tokens=60)
                print("Chatbot: " + response.choices[0].text.strip())
            else:
                response = openai.Completion.create(engine="text-davinci-003", prompt="Alright, have a great evening! Looking forward to hearing from you.", max_tokens=60)
                print("Chatbot: " + response.choices[0].text.strip())
        else:
            self.handle_user_input(user_input)


if __name__ == "__main__":
    #bot = RealEstateChatbot('/Users/amarahmed/Desktop/reelTour_/response_status_active_filter_tcb.json')
    bot = RealEstateChatbot()
    bot.start_chat()
    
