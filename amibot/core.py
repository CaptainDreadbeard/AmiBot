# engine/core.py
import random
import json
import os
import platform
from .personality import Personality

# ---------------------------------------------------------
# Cross‑platform memory path
# ---------------------------------------------------------
def get_memory_path():
    system = platform.system()

    if system == "Windows":
        base = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "amibot")
    elif system == "Darwin":  # macOS
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "amibot")
    else:  # Linux and others
        base = os.path.join(os.path.expanduser("~"), ".local", "share", "amibot")

    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "longterm_memory.json")


class ChatBot:
    def __init__(self, name="AmiBot"):
        self.name = name
        self.memory = []  # short-term memory
        self.personality = Personality()
        self.emotion = "neutral"
        self.mode = "friendly"
        self.topic = None
        self.longterm = self.load_longterm_memory()

        # Restore bot state
        if "bot_state" in self.longterm:
            self.mode = self.longterm["bot_state"].get("mode", "friendly")
            self.emotion = self.longterm["bot_state"].get("emotion", "neutral")

    # ---------------------------------------------------------
    # Long-term memory load/save (fixed)
    # ---------------------------------------------------------
    def load_longterm_memory(self):
        path = get_memory_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"user_facts": {}, "conversation_history": [], "bot_state": {}}

    def save_longterm_memory(self, data):
        path = get_memory_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # ---------------------------------------------------------
    # Skills
    # ---------------------------------------------------------
    def handle_skill(self, user_input):

        if user_input == "/time":
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

        if user_input == "/date":
            from datetime import datetime
            return f"Today is {datetime.now().strftime('%Y-%m-%d')}."

        if user_input == "/coin":
            return "Heads!" if random.random() < 0.5 else "Tails"

        if user_input == "/roll":
            return f"You rolled a {random.randint(1, 6)}."

        if user_input == "/joke":
            jokes = [
                "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
                "I told my laptop I needed a break… now it won’t stop sending me vacation ads.",
                "Why do programmers prefer dark mode? Because light attracts bugs."
            ]
            return random.choice(jokes)

        if user_input == "/clear_memory":
            self.longterm = {"user_facts": {}, "conversation_history": [], "bot_state": {}}
            self.save_longterm_memory(self.longterm)
            return "All long-term memory cleared."

        if user_input == "/stats":
            return (
                f"Mode: {self.mode}\n"
                f"Emotion: {self.emotion}\n"
                f"Short-term memory: {self.memory}\n"
                f"Long-term facts: {list(self.longterm['user_facts'].keys())}\n"
                f"Conversation history length: {len(self.longterm['conversation_history'])}"
            )

        if user_input.startswith("/define "):
            word = user_input.replace("/define ", "").strip()
            definitions = {
                "python": "A high-level programming language known for readability.",
                "algorithm": "A step-by-step procedure for solving a problem.",
                "chatbot": "A program designed to simulate conversation with humans."
            }
            return definitions.get(word, f"Sorry, I don't have a definition for '{word}'.")

        return None

    # ---------------------------------------------------------
    # Main response logic
    # ---------------------------------------------------------
    def get_response(self, user_input: str) -> str:
        user_input = user_input.strip().lower()

        if not user_input:
            return "Say something, I'm listening!"

        # Quit
        if user_input in {"/quit", "quit", "exit", "goodbye", "bye"}:
            return "__QUIT__"

        # Skills
        skill_response = self.handle_skill(user_input)
        if skill_response:
            return skill_response

        # Remember
        if user_input.startswith("/remember "):
            fact = user_input.replace("/remember ", "").strip()
            if fact:
                self.longterm["user_facts"][fact] = True
                self.save_longterm_memory(self.longterm)
                return f"I'll remember that: '{fact}'."

        # Greetings
        if user_input in {"hi", "hello", "hey"}:
            return f"Hey there, I'm {self.name}. What's on your mind?"

        # Short-term memory
        self.memory.append(user_input)
        if len(self.memory) > 5:
            self.memory.pop(0)

        # Patterns
        if user_input.startswith("i feel "):
            feeling = user_input.replace("i feel ", "").strip()
            return f"Why do you feel {feeling}?"

        if user_input.startswith("i am "):
            state = user_input.replace("i am ", "").strip()
            return f"What makes you feel {state}?"

        # ---------------------------------------------------------
        # ICE CREAM TOPIC LOGIC (PRIORITY)
        # ---------------------------------------------------------

        # Start ice cream topic
        if "ice cream" in user_input:
            self.topic = "ice cream"
            return "I love ice cream! What's your favorite flavor?"

        # Flavor follow-up
        if self.topic == "ice cream":
            flavors = {
                "vanilla": "Vanilla is always a classic choice! Do you prefer it with sprinkles?",
                "chocolate": "Chocolate is goated. Do you want to go get some with me?",
                "strawberry": "Well the good thing about opinions is we are all entitled to have our own.",
                "mint": "Mint is a comfort flavor for sure.",
                "cookie dough": "Cookie dough is what I eat when I'm feeling sad. It's like a hug in dessert form.",
                "pistachio": "Pistachio is like an adventure in your mouth through the canals of Italy."
            }

            for flavor, response in flavors.items():
                if flavor in user_input:
                    self.topic = None
                    return response

            return "Oooh interesting. Tell me more about that flavor! I love trying new ice cream flavors."

        # ---------------------------------------------------------
        # KEYWORD RESPONSES (AFTER TOPIC LOGIC)
        # ---------------------------------------------------------
        for keyword in self.personality.keyword_responses:
            if keyword in user_input:
                return self.personality.get_keyword_response(keyword)

        # ---------------------------------------------------------
        # MEMORY CALLBACK (AFTER TOPIC + KEYWORDS)
        # ---------------------------------------------------------
        if len(self.memory) > 2 and random.random() < 0.10:
            past = random.choice(self.memory[:-1])
            return f"By the way, earlier you mentioned '{past}'. Please elaborate."

        # Emotion detection
        positive_words = {"happy", "excited", "good", "great", "amazing", "love"}
        negative_words = {"sad", "tired", "angry", "upset", "mad", "depressed"}

        if any(word in user_input for word in positive_words):
            self.emotion = "positive"
        elif any(word in user_input for word in negative_words):
            self.emotion = "negative"

        # Emotional tone
        if self.emotion == "positive":
            response = self.personality.get_general_response() + " 😊"
        elif self.emotion == "negative":
            response = "I'm here with you bud. " + self.personality.get_general_response()
        else:
            response = self.personality.get_general_response()

        # Save bot state
        self.longterm["bot_state"] = {
            "mode": self.mode,
            "emotion": self.emotion
        }

        # Save conversation history
        self.longterm["conversation_history"].append(user_input)
        if len(self.longterm["conversation_history"]) > 100:
            self.longterm["conversation_history"].pop(0)

        # Write to disk
        self.save_longterm_memory(self.longterm)

        return response


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
def run():
    bot = ChatBot()
    print("Amibot is running. Type /help for commands...")

    while True:
        user_input = input("> ")
        response = bot.get_response(user_input)

        if response == "__QUIT__":
            print("Goodbye, my love!")
            break

        print(response)
