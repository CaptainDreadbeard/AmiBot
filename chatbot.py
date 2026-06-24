# chatbot.py

from datetime import datetime
from amibot import ChatBot
import os
import sys
import time
from colorama import Fore, Style, init
init(autoreset=True, convert=True)

def type_out(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def log_message(sender, message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/conversation.txt", "a", encoding="utf-8") as f:
        f.write(f"{sender}: {message}\n")

def main():
    bot = ChatBot(name="AmiBot")

    print("=" * 50)
    print(" Welcome to AmiBot (prototype)")
    print("Type /quit to exit.")
    print("=" * 50)

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n I love you, Goodbye")
            break

        response = bot.get_response(user_input)

        if response == "__QUIT__":
            type_out(Fore.CYAN + f"{bot.name}: " + Style.RESET_ALL + "I love you, bye bye!")
            break
        
        type_out(Fore.CYAN + f"{bot.name}: " + Style.RESET_ALL + response)

        # log messages
        log_message("User", user_input)
        log_message(bot.name, response)


# Main function
if __name__ == "__main__":
    main()