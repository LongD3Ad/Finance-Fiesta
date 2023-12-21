import tkinter as tk
from tkinter import font, ttk
import customtkinter
from customtkinter import *
import json
# Assuming 'chatbot' is a module that you have that contains these functions
from chatbot import find_best_match, get_answer_for_question, load_knowledge_base, save_knowledge_base

# Dummy credentials - Replace this with your authentication mechanism
VALID_USERNAME = "wesleysam"
VALID_PASSWORD = "family123"

# New function to handle the login button click
def on_login_button_click():
    username = entry1.get()
    password = entry2.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        root.destroy()  # Close the login window
        open_chat_window()  # Open the chat window
    else:
        label_error = customtkinter.CTkLabel(master=frame, text="Invalid credentials!", text_color=("red", "red"))
        label_error.pack(pady=5)

def open_chat_window():
    # Chatbot Window Code Below
    chat_root = tk.Tk()
    chat_root.title("FINANCE FIESTA")

    # Custom logo image
    # Make sure 'chatbot_logo.png' is available in the script's directory or provide full path
    chat_logo = tk.PhotoImage(file='chatbot_logo.png')
    chat_root.iconphoto(False, chat_logo)
    
    # Use a new color scheme and font
    bg_color = '#1E1F26'
    text_color = '#FFFFFF'
    accent_color = '#008000'
    chat_font = font.Font(family='Arial', size=12)

    # Load the knowledge base
    knowledge_base = load_knowledge_base('knowledge_base.json')
    
    # Function to handle user input and bot response
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
        chat_history.insert(tk.END, "Bot: " + "What is your next question." + "\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.yview(tk.END)
        user_message.delete(0, tk.END)

    # Chat history display
    chat_history = tk.Text(chat_root, bg=bg_color, fg=text_color, font=chat_font)
    chat_history.pack(fill='both', expand=True, padx=20, pady=10)

    # ... rest of your chat window code

    # Add a scrollbar 
    scrollbar = ttk.Scrollbar(chat_root, command=chat_history.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_history.config(yscrollcommand=scrollbar.set)

    # User input section
    input_frame = ttk.Frame(chat_root, padding=10)
    input_frame.pack(fill='x')

    user_message = ttk.Entry(input_frame, font=chat_font)
    user_message.grid(row=0, column=0, sticky='ew')

    send_button = ttk.Button(input_frame, text="Send", command=send_message, style="Custom.TButton", width=10)
    send_button.grid(row=0, column=1, padx=10)

    # Start the GUI event loop
    chat_root.mainloop()


# Login Window Code Below
root = CTk()
root.geometry("500x350")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

frame = CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = CTkButton(master=frame, text="Login", command=on_login_button_click)
button.pack(pady=12, padx=10)

checkbox = CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

root.mainloop()

