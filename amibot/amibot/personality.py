import random

class Personality:
    """
    Defines AmiBot's tone vocabulary, and general vibe.
    """

    def __init__(self):
        self.general_responses = [
            "Thats fascinating, please tell me more!",
            "Hmm, how do you figure?",
            "Go on...",
            "That's fantastic!!!",
            "You have me curious!"
        ]

        self.keyword_responses = {
            "ice cream": [
                "Ice cream? Solid choice, champ. What flavor we talkin?",
                "Ice Cream is frozen happiness",
                "Now I'm craving Ice Cream!!!"
            ],

            "sad": [
                "I'm sorry about that, champ",
                "That's heavy, would you like to tell me about it?",
                "I'm always here for you, champ, what happened?"
            ],

            "happy": [
                "I love that for you!!!",
                "Good vibes detected",
                "That's awesome -- what made you feel that way?",
            ],

            "tired": [
                "you deserve some rest",
                "Was it a long day, champ?",
                "Tired is a whole mood, what drained you?",
            ]
        }
    def get_keyword_response(self, keyword):
        return random.choice(self.keyword_responses[keyword])
    
    def get_general_response(self):
        return random.choice(self.general_responses)