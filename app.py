from chatbot import get_response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input))