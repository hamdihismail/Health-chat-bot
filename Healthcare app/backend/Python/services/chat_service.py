import openai   
import requests
# from backend.Python.models import db_conn
# import location_service
req = requests

openai.api_key = "sk-proj-SdMnSPiKizNSEVQ3esXdT3BlbkFJdURcN7I8kyePpoZBA4De"

INSTRUCTIONS = """You are a healthcare assistant providing accurate and up-to-date health information and tips based on North American standards, with a preference for using sources from the Mayo Clinic."""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

def chat_response(instructions, conversation_history, latest_question):
    messages = [
        {"role": "system", "content": instructions},
    ]

    for question, answer in conversation_history[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    
    messages.append({ "role": "user", "content": latest_question })

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return response.choices[0].message.content

def main():
    print("Say hello to your new assistant!")
    conversation_history = []
    while True:
        latest_question = input()
        if any(ele in latest_question for ele in ["quit","bye","exit","goodbye"]):
            break
        
        response = chat_response(INSTRUCTIONS, conversation_history, latest_question)

        conversation_history.append((latest_question, response))

        print("\n" + response + "\n")
        print(str(conversation_history))
        print(str(conversation_history).strip('[]').replace("'","").replace("\"",""))
    # Data = str(conversation_history).strip('[]').replace("'","").replace("\"","")
    # r1 = req.post('http://localhost:8000/chat/add', json={"conversation":Data})
    # res1 = r1.json()
    # chatId = res1['id']
    # r2 = req.post('http://localhost:8000/session/add', json={"chatId":chatId,"userId":1})

# def main(latest_question: str, userId: int, sessionId:int):
#     print("Say hello to your new assistant!")

#     sessionId_str = str(sessionId)

#     conversation_history = []
#     if sessionId:
#         try:
#             r0 = req.get('http://localhost:8000/session/'+sessionId_str)
#             res0 = r0.json()
#             print(res0)
#             print(res0[0]['chatId'])
#             chat_id = res0[0]['chatId']
#             chat_id_str = str(chat_id)
#             rChat = req.get('http://localhost:8000/chat/'+chat_id_str)
#             rChatRes = rChat.json()
#             # print(rChatRes['conversation'])
#             rChatHistory = rChatRes['conversation']
#             print(rChatHistory)
#             conversation_history.append(rChatHistory)
#             print(conversation_history)
#         except req.RequestException as e:
#             print(f"Request failed: {e}")
#             return "An error occurred"
#     response = chat_response(INSTRUCTIONS, conversation_history, latest_question)

#     # conversation_history.append((latest_question, response))
#     # Data = str(conversation_history).strip('[]').replace("'","").replace("\"","")
#     # if not sessionId:
#     #     r1 = req.post('http://localhost:8000/chat/add', json={"conversation":Data})
#     #     res1 = r1.json()
#     #     chatId = res1['id']
#     #     req.post('http://localhost:8000/session/add', json={"chatId":chatId,"userId":userId})
#     # if sessionId:
#     #     req.put('http://localhost:8000/chat/update', json={"chat_id":chat_id,"updated_conversation":Data})
#     return response


if __name__ == "__main__":
    main()