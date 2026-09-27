import json
import os
import random
from difflib import SequenceMatcher

# JSON file jisme bot apni learning save karega
DATA_FILE = "chatbot_data.json"

def load_data():
    """JSON file se data load karo"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"patterns": {}}

def save_data(data):
    """Data ko JSON file mein save karo"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_similar_pattern(user_input, patterns, threshold=0.6):
    """Sabse similar pattern dhundo"""
    best_match = None
    best_score = threshold
    
    for pattern in patterns:
        score = SequenceMatcher(None, user_input.lower(), pattern.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = pattern
    
    return best_match

def chatbot():
    data = load_data()
    patterns = data["patterns"]
    
    print("🤖 AI ChatBot: Namaste! Main aapka AI chatbot hoon.")
    print("📚 Main har baat se seekh sakta hoon!")
    print("💬 'quit' likho chat khatam karne ke liye.\n")
    
    while True:
        user_input = input("Aap: ").strip()
        
        if user_input.lower() == "quit":
            print("🤖 AI ChatBot: Bye! Aapke saath baat karke maza aaya!")
            break
        
        if not user_input:
            continue
        
        # Pehle exact match dhundo
        if user_input.lower() in patterns:
            response = random.choice(patterns[user_input.lower()])
            print(f"🤖 AI ChatBot: {response}\n")
        else:
            # Similar pattern dhundo
            similar = find_similar_pattern(user_input, patterns)
            
            if similar:
                response = random.choice(patterns[similar])
                print(f"🤖 AI ChatBot: {response}")
                print(f"📌 (Similar to: '{similar}')\n")
            else:
                # Nayi pattern sikhne ka request
                print("🤖 AI ChatBot: Mujhe yeh samajh nahi aaya!")
                response = input("📝 Mujhe seekhao - is input ke liye kya reply hona chahiye? ").strip()
                
                if response:
                    if user_input.lower() in patterns:
                        patterns[user_input.lower()].append(response)
                    else:
                        patterns[user_input.lower()] = [response]
                    
                    data["patterns"] = patterns
                    save_data(data)
                    
                    print("✅ AI ChatBot: Shukriya! Mujhe nayi cheez seekh gayi!\n")
                else:
                    print("⚠️ AI ChatBot: Theek hai, agle baar seekhunga.\n")

if __name__ == "__main__":
    chatbot()
