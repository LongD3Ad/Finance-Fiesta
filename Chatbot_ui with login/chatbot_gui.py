import tkinter as tk
from tkinter import font, ttk
from chatbot import find_best_match, get_answer_for_question, load_knowledge_base, save_knowledge_base

# Create an instance of the Tkinter class
root = tk.Tk()
root.title("FINANCE FIESTA")

# Custom logo image
logo = tk.PhotoImage(file='chatbot_logo.png')
root.iconphoto(False, logo)

# Use a new color scheme and font
bg_color = '#1E1F26'
text_color = '#FFFFFF'
accent_color = '#008000'
chat_font = font.Font(family='Arial', size=12)

# Load the knowledge base
knowledge_base = load_knowledge_base('knowledge_base.json')

# Function to handle user input and return responses
def send_message(event=None):
    user_input = user_message.get()
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        chat_history.insert(tk.END, "Bot: " + answer + "\n")
    else:
        print("Bot: I don't know the answer. Can you teach me?")
        new_answer = input("Type the answer or 'skip' to skip: ")

        if new_answer.lower() != 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            print("Bot: Thank you! I've learned something new.")

# Update the user interface to display the bot's response
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bot: " + "What is your next question" + "\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)
    user_message.delete(0, tk.END)


# Chat history display
chat_history = tk.Text(root, bg=bg_color, fg=text_color, font=chat_font)
chat_history.pack(fill='both', expand=True, padx=20, pady=10)

# Add a scrollbar 
scrollbar = ttk.Scrollbar(root, command=chat_history.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.config(yscrollcommand=scrollbar.set)

# User input section
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill='x')

user_message = ttk.Entry(input_frame, font=chat_font)
user_message.grid(row=0, column=0, sticky='ew')

send_button = ttk.Button(input_frame, text="Send", command=send_message, style="Custom.TButton", width=10)
send_button.grid(row=0, column=1, padx=10)

# Start the GUI event loop
root.mainloop()
