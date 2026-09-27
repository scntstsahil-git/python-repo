import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import random
from difflib import SequenceMatcher
import re

DATA_FILE = "chatbot_memory.json"

class AILearningChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Learning ChatBot")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e2e")
        
        self.memory = self.load_memory()
        
        # Header
        header = tk.Label(
            self.root,
            text="🤖 AI Learning ChatBot",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e",
            fg="#00d4ff"
        )
        header.pack(pady=10)
        
        # Chat Display Area
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            width=70,
            height=25,
            bg="#2a2a3e",
            fg="#ffffff",
            font=("Courier", 10),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config("bot", foreground="#00d4ff", font=("Courier", 10, "bold"))
        self.chat_display.tag_config("user", foreground="#00ff88", font=("Courier", 10))
        self.chat_display.tag_config("learn", foreground="#ffaa00", font=("Courier", 9, "italic"))
        self.chat_display.tag_config("error", foreground="#ff4444", font=("Courier", 10))
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # User Input
        self.user_input = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg="#3a3a4e",
            fg="#ffffff",
            insertbackground="#00d4ff"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.user_input.bind("<Return>", lambda e: self.send_message())
        
        # Send Button
        send_btn = tk.Button(
            input_frame,
            text="📤 Send",
            font=("Helvetica", 11, "bold"),
            bg="#00d4ff",
            fg="#1e1e2e",
            cursor="hand2",
            command=self.send_message
        )
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(
            input_frame,
            text="🗑️ Clear",
            font=("Helvetica", 11, "bold"),
            bg="#ff4444",
            fg="#ffffff",
            cursor="hand2",
            command=self.clear_chat
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Status: Ready | Learned patterns: " + str(len(self.memory)),
            font=("Helvetica", 9),
            bg="#2a2a3e",
            fg="#888888"
        )
        self.status_bar.pack(fill=tk.X, padx=10, pady=5)
        
        # Initial message
        self.display_message("Bot", "Namaste! 👋 Main aapka AI ChatBot hoon. Main har baat se seekh sakta hoon!\nAap mujhse kuch poochiye ya bataiye. 😊", "bot")
    
    def load_memory(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_memory(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text.strip()
    
    def similarity_score(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def find_best_match(self, user_text):
        best_key = None
        best_score = 0.0
        
        for key in self.memory:
            score = self.similarity_score(user_text, key)
            if score > best_score:
                best_score = score
                best_key = key
        
        if best_score > 0.5:
            return best_key, best_score
        return None, 0.0
    
    def display_message(self, sender, message, tag="user"):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        user_text = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)
        
        if not user_text:
            return
        
        # Display user message
        self.display_message("You", user_text, "user")
        
        cleaned = self.clean_text(user_text)
        
        if not cleaned:
            self.display_message("Bot", "Kuch boliye na! 😊", "bot")
            return
        
        # Check exact match
        if cleaned in self.memory:
            responses = self.memory[cleaned]
            bot_reply = random.choice(responses)
            self.display_message("Bot", bot_reply, "bot")
            self.update_status()
            return
        
        # Check similar match
        match, score = self.find_best_match(cleaned)
        if match:
            responses = self.memory[match]
            bot_reply = random.choice(responses)
            self.display_message("Bot", bot_reply, "bot")
            self.display_message("Bot", f"(Similarity: {score:.0%} - '{match}')", "learn")
            self.update_status()
            return
        
        # Ask user to teach
        self.display_message("Bot", f"Mujhe '{user_text}' ka matlab samajh nahi aaya. 😕", "error")
        self.display_message("Bot", "Mujhe seekhao - is message ke liye kya reply hona chahiye?", "learn")
        
        # Wait for user input
        self.root.update()
        self.learning_mode = True
        self.current_pattern = cleaned
    
    def handle_learning(self):
        if hasattr(self, 'learning_mode') and self.learning_mode:
            user_reply = self.user_input.get().strip()
            self.user_input.delete(0, tk.END)
            
            if user_reply:
                if self.current_pattern in self.memory:
                    self.memory[self.current_pattern].append(user_reply)
                else:
                    self.memory[self.current_pattern] = [user_reply]
                
                self.save_memory()
                self.display_message("Bot", f"✅ Shukriya! Main ab yaad rakhunga:\n'{self.current_pattern}' → '{user_reply}'", "learn")
                self.learning_mode = False
            else:
                self.display_message("Bot", "⚠️ Theek hai, main isko ignore kar deta hoon.", "error")
                self.learning_mode = False
            
            self.update_status()
    
    def clear_chat(self):
        if messagebox.askyesno("Confirm", "Chat history clear kar doge?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.display_message("Bot", "Chat cleared! 🗑️", "bot")
    
    def update_status(self):
        self.status_bar.config(
            text=f"Status: Ready | Learned patterns: {len(self.memory)}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AILearningChatBot(root)
    root.mainloop()
