import openai
import os
import re


# Replace with your OpenAI API key
openai.api_key = "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"

PROMPT_START = '''You are an engaging and helpful chatbot that guides users to find the right home in Austin, Texas. If they are interested, you direct them to contact real estate agent Daniel Tully at 512-767-2761. Ask the following questions to gather information:
- What type of home are you looking for?
- How many bedrooms do you need?
- What is your budget?
- Are you looking for a specific neighborhood?
- What are some must-have features in your new home?'''

def generate_response(prompt):
    #return "affirmative"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.5,  # Lower temperature for more focused responses
        #top_p=1,  # Use top_p to focus on more probable answers
    )
    return response.choices[0].text.strip()



def get_yes_no_response(question):
    while True:
        print(question)
        user_input = input("You: ").lower()
        if user_input in ["yes", "no"]:
            return user_input == "yes"
        else:
            prompt = f"The user responded with '{user_input}'. Determine if the user's response is affirmative or negative in the context of the question '{question}'."
            chatbot_response = generate_response(prompt)
            if chatbot_response:
                chatbot_response = chatbot_response.lower()
                if "affirmative" in chatbot_response:
                    print("Chatbot: yes")
                    return True
                elif "negative" in chatbot_response:
                    print("Chatbot: no")
                    return False
                else:
                    print("Chatbot: I didn't understand your response. Please answer with 'yes' or 'no'.")
            else:
                print("Chatbot: I didn't understand your response. Please answer with 'yes' or 'no'.")

def confirm_exit():
    print("Chatbot: Before we end the conversation, do you have any more questions or concerns? (yes/no)")
    while True:
        confirm = input("You: ").lower()
        if confirm in ["yes", "no"]:
            return confirm == "yes"

def book_tour():
    print("Chatbot: Would you like to book a tour for the property? (yes/no)")
    while True:
        confirm = input("You: ").lower()
        if confirm in ["yes", "no"]:
            return confirm == "yes"
        
def book_appointment():
    print("Chatbot: Would you like to book an appointment with me ? (yes/no)")
    while True:
        confirm = input("You: ").lower()
        if confirm in ["yes", "no"]:
            return confirm == "yes"


def main():
    
    #wip later
    print("Hey! I'm Daniel Tully and I'm here to help you find the perfect home in Austin, Texas.")
    response = get_yes_no_response("Would you like to start? (yes/no)")
    print("Response:", response)

    
    # print("Hey! I'm Daniel Tully and I'm here to help you find the perfect home in Austin, Texas.")
    # print("Would you like to start ? (yes/no)")

    #chat_history = PROMPT_START

    #user_input = input("You: ").lower()

    if response == False:
        print("Chatbot: No problem! If you have any questions or need assistance in the future, feel free to ask. Have a great day!")
        return
    if response==True:
        
        print("Ok lets get started ! Lets first get your contact information and then ask a few questions")

        print("What is your name ?")
        name = input("You: ").lower()

        print("And what is a valid phone number [no special characters or letters] or email so we can stay in touch after this")

        chat_history = PROMPT_START
        required_info = ["type", "bedrooms", "budget", "neighborhood", "features", "other"]
        gathered_info = []


        while True:

            user_input = input("You: ").lower()
            exit_phrases = ["quit", "exit", "bye"]
            interested_phrases = ["interested", "book a tour", "schedule a tour", "book appointment"]

            
            while not (re.match("^\d{10}$", user_input)) or (re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_input)):
                print ("I did not get that, can you try that again")
                user_input = input("You: ").lower()
                #contact_info = user_input

            contact_info = user_input
            print(f"Ok {name} lets begin !")

            missing_info = set(required_info) - set(gathered_info)
            if missing_info:
                follow_up_questions = {
                    "type": "What type of home are you looking for?",
                    "bedrooms": "How many bedrooms do you need?",
                    "budget": "What is your budget?",
                    "neighborhood": "What part(s) of town are you interested in ?",
                    "features": "What are some must-have features in your new home?",
                    "other":"Anything else I should note for your ideal home ?",
                }
                for info in required_info:
                    print(f"Chatbot: {follow_up_questions[info]}")
                    user_input = input("You: ").lower()
                    gathered_info.append(info)
                    if any(phrase in user_input for phrase in exit_phrases):
                        break
        

            # If all required information is gathered, prompt for booking/appt a tour
            if set(gathered_info) == set(required_info):
                # if book_tour():
                #     print("Chatbot: Great! Please provide your availability for the tour.")
                #     availability = input("You: ")
                #     print(f"Chatbot: Thank you! I've noted your availability as '{availability}'. Daniel Tully will follow up with you to confirm the tour details. If you have any more questions or concerns, please feel free to contact Daniel Tully at 512-767-2761. Have a great day!")
                #     break

                if book_appointment():
                    print("Chatbot: Great! Please provide your availability for an call with me.")
                    availability = input("You: ")
                    print(f"Chatbot: Thank you {name}! I've noted your availability as {availability}. I will follow up with you at {contact_info} as soon as I can. If you have any more questions or concerns, please feel free to contact me at 512-767-2761. Have a great day!")
                    break

            if any(phrase in user_input for phrase in exit_phrases):
                if confirm_exit():
                    print("Chatbot: Thank you for letting me know. I'll make a note of your concerns, and I will get back to you shortly. If you have any more questions or concerns, feel free to contact me at 512-767-2761. Goodbye!")
                    break
                else:
                    print("Chatbot: Great!")

            if any(phrase in user_input for phrase in interested_phrases):
                #note below for hypos
                if book_tour():
                    print("Chatbot: Great! Please provide your availability for the tour.")
                    availability = input("You: ")
                    print(f"Chatbot: Thank you {name}! I've noted your availability as {availability}. I will follow up and contacting you at {contact_info} with you to confirm the tour details. If you have any more questions or concerns, please feel free to contact Daniel Tully at 512-767-2761. Have a great day!")
                    break
                if book_appointment():
                    print("Chatbot: Great! Please provide your availability for a call.")
                    availability = input("You: ")
                    print(f"Chatbot: Thank you {name}! I've noted your availability as {availability}. I will follow up and contacting you at {contact_info} with you to confirm the call. If you have any more questions or concerns, please feel free to contact me at 512-767-2761. Have a great day!")
                    break
                else:
                    print("Chatbot: No problem! If you change your mind or have more questions, feel free to ask.")
                    continue

if __name__ == "__main__":
    main()