import json
from difflib import get_close_matches
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get simplified answer using spaCy
def simplify_answer(answer: str) -> str:
    doc = nlp(answer)
    simplified_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

    simplified_sentence = ''
    for token in doc:
        if token.dep_ in ["nsubj", "dobj", "prep", "pobj", "aux", "ROOT", "conj"]:
            if simplified_sentence and token.pos_ != "PUNCT":
                simplified_sentence += ' '
            simplified_sentence += token.text

    return simplified_sentence

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Main function to handle user input and respond
def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    last_answer: str | None = None  # Variable to store last given answer

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            break

        # Requests to simplify the answer
        if user_input.lower() in ["i don't understand", "can u make this simpler", "simplify this"] and last_answer is not None:
            simplified_sentence = simplify_answer(last_answer)
            print(f"Bot: {simplified_sentence}")
            continue

        # Finds the best match, otherwise returns None
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            # If there is a best match, store the full answer from the knowledge base
            last_answer = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {last_answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip: ")
            last_answer = new_answer  # Store the new answer

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! I've learned something new.")

if __name__ == "__main__":
    chatbot()