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

        # Keyword responses
        for keyword in self.personality.keyword_responses:
            if keyword in user_input:
                return self.personality.get_keyword_response(keyword)

        # Mode change
        if user_input.startswith("/mode "):
            new_mode = user_input.replace("/mode ", "").strip()
            valid_modes = {"friendly", "serious", "chaotic", "sarcastic"}

            if new_mode not in valid_modes:
                return f"Invalid mode. Available modes: {', '.join(valid_modes)}"

            self.mode = new_mode
            return f"Personality mode changed to: {new_mode}"

        # Help
        if user_input == "/help":
            return (
                "Here are my available commands:\n"
                "/time - show the current time\n"
                "/date - show the current date\n"
                "/joke - tell a joke\n"
                "/roll - roll a die\n"
                "/coin - flip a coin\n"
                "/remember <fact> - store a fact\n"
                "/clear_memory - erase long-term memory\n"
                "/stats - show internal state\n"
                "/define <word> - define a word\n"
                "/mode <type> - change personality\n"
                "/help - show this help menu\n"
                "/whoami - show what I remember about you\n"
                "/whoareyou - show information about me"
            )

        if user_input.startswith("/") and user_input not in {"/help", "/whoami", "/whoareyou"}:
            return "I don't recognize that command. Type /help to see what I can do."

        # Who am I
        if user_input == "/whoami":
            facts = self.longterm["user_facts"]
            if not facts:
                return "The girls dem suga."
            lines = "\n".join(f"- {fact}" for fact in facts)
            return f"Here's what I remember about you:\n{lines}"

        # Who are you
        if user_input == "/whoareyou":
            return (
                f"I'm {self.name}, a small CLI chatbot with memory and personality.\n"
                f"My current mode is: {self.mode}\n"
                f"My emotional tone is: {self.emotion}"
            )

        # Total recall
        for fact in self.longterm["user_facts"]:
            if fact in user_input:
                return f"You told me before that '{fact}'. Is that still true?"

        # Emotion detection
        positive_words = {"happy", "excited", "good", "great", "amazing", "love"}
        negative_words = {"sad", "tired", "angry", "upset", "mad", "depressed"}

        if any(word in user_input for word in positive_words):
            self.emotion = "positive"
        elif any(word in user_input for word in negative_words):
            self.emotion = "negative"

        # Memory callback
        if len(self.memory) > 2 and random.random() < 0.10:
            past = random.choice(self.memory[:-1])
            return f"By the way, earlier you mentioned '{past}'. Please elaborate."

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
