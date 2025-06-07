from chatbot import get_response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input))

import os
from dotenv import load_dotenv

load_dotenv()

  client_id=INzdg_TV7NM6bAcQU-sWRQ
  client_secret=luzjBYenx5pTPKlV4lf_vjEM2VBZAw
  user_agent="ForumChatBot/1.0 by sobeck1001
