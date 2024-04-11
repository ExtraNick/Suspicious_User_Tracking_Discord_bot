from random import choice, randint #this is used for flair 
import json 

Bot_channel = 1226380484020404304

with open("data.json", "r" ) as openfile: #opens the JSON file where the user IDs are storeds
    #print(json.load(openfile))
    sus_users = json.load(openfile) #loads the contents of the JSON file into the sus_users list

def get_response(user_input: str, channel: str) -> str:
    lowered: str = user_input.lower() #Python is case senstitive so this ensures all messages receives are lower case and no conflicts happen

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    # elif 'hello' in lowered:
    #     return 'Hello there!'
    # elif 'how are you' in lowered:
    #     return 'See you!'
    # elif 'roll dice' in lowered:
    #     return f'You rolled: {randint(1, 6)}'
    if 'add suspicious user 'in lowered and channel == Bot_channel:
        sent_user_id = user_input[20:] #This checks if the input matches the Discord User ID syntax (18 characters of length)
        if len(sent_user_id) != 18:
            return 'User ID specified doesnt match the 18 characters standard length'
        elif sent_user_id in sus_users: #This check if the provided User ID already exists in the sus_users list
            return 'User ID already exists in the suspicious users list'
        else:
            sus_users.append(sent_user_id) #adds the User ID to the sus_users list
            print(sus_users) #this print is used to feedback here in the console
            with open("data.json", "w") as outfile: #opens the JSON file
                outfile.write(json.dumps(sus_users)) #Saves the new sus_sers list into the JSON file to be read later
            return 'user added to suspicious list'
        
    if 'remove suspicious user ' in lowered and channel == Bot_channel:
        sent_user_id = user_input[23:] #This checks if the input matches the Discord User ID syntax (18 characters of length)
        if len(sent_user_id) != 18: 
            return 'User ID specified doesnt match the 18 characters standard length'
        elif sent_user_id not in sus_users: #This check if the provided User ID is present in the current sus_users list
            return 'User ID does not exist in the suspicious users list'
        else:
            sus_users.remove(sent_user_id) #removes the User ID from the list
            print(sus_users) #prints the action to the console
            with open("data.json", "w") as outfile: #opens the JSON file
                outfile.write(json.dumps(sus_users)) #Saves the new sus_users list into the JSON file to be read later
            return 'user removed from suspicious list'
    # else:
    #     return choice(['I do not understand...',
    #                    'What are you talking about',
    #                    'Do you mind rephrasing that?'])
def send_response(name: str, message: str) -> str:
    name = message.author
    message = message.content
    return "Message by suspicious user " + str(message.author) + " detected. Message:", message.content
    
