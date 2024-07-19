import re
import json
import hashlib
import os

while True:
    def clean_chat_data(chat_data):
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?(AM|PM|am|pm|NNBSPAM) - ',  # Remove timestamp lines
            r'This business uses a secure service from Meta to manage this chat. Tap to learn more.',
        ]

        cleaned_data = chat_data
        for pattern in patterns:
            cleaned_data = re.sub(pattern, '', cleaned_data)
        cleaned_data = re.sub(r'\n+', '\n', cleaned_data).strip()
        return cleaned_data


    def extract_question_and_answer(chat_data, question_speaker, answer_speaker):
        lines = chat_data.split('\n')

        question_answer_data = []
        question = None

        for line in lines:
            if f'{question_speaker}: ' in line:
                question = line.split(f'{question_speaker}: ', 1)[1].strip()
            elif f'{answer_speaker}: ' in line and question:
                answer = line.split(f'{answer_speaker}: ', 1)[1].strip()
                question_answer_data.append((question, answer))
                question = None

        return question_answer_data


    def format_training_data(question_answer_data):
        training_data = []
        for question, answer in question_answer_data:
            training_data.append(question)
            training_data.append(answer)

        return training_data


    def load_custom_data(filepath: str) -> dict:
        with open(filepath, "r") as file:
            return json.load(file)


    def save_custom_data(filepath: str, data: dict):
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)


    def load_whatsapp_export(chat_path: str) -> str:
        with open(chat_path, "r") as file:
            chat_data = file.read()
        return chat_data


    def compute_file_hash(file_content: str) -> str:
        return hashlib.sha256(file_content.encode('utf-8')).hexdigest()


    # Path to the JSON file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    flask_folder = os.path.dirname(current_directory)
    flask_ui = os.path.join(flask_folder, 'flask ui')
    custom_data_filepath = os.path.join(flask_ui, "knowledge_base.json")

    # Load existing custom data
    custom_data = load_custom_data(custom_data_filepath)
    training_data = custom_data.get("training_data", [])
    file_hashes = custom_data.get("file_hashes", [])

    # Get the WhatsApp export file path from the user
    file_name = input("ENTER THE FILE NAME YOU WANT TO CLEAN AND APPEND TO JSON FILE.\nTHE FILE CAN ONLY BE SELECTED FROM EXPORT FOLDER: eg 'export1.txt': ")
    exports = os.path.join(flask_folder, 'exports')
    chat_path = os.path.join(exports, file_name)

    # Load chat data and compute its hash
    chat_data = load_whatsapp_export(chat_path)
    file_hash = compute_file_hash(chat_data)

    if file_hash in file_hashes:
        print(f"The {file_name} has already been processed and exists in the knowledge base.")
    else:
        choice = input("Are you sure you want to add cleaned data to the knowledge base json file? \nYou can always undo this action.(yes/no)").lower()

        if choice == 'yes':
            # Get speaker names from the user
            question_speaker = input(f"Enter the name of the QUESTION SPEAKER from the {file_name} (e.g., 'Joyrita','Jon','Max_proy'): ")
            answer_speaker = input(f"Enter the name of the ANSWER SPEAKER from the {file_name} (e.g. 'August AI', 'Ai Doctor', ): ")

            cleaned_data = clean_chat_data(chat_data)
            parsed_data = extract_question_and_answer(cleaned_data, question_speaker, answer_speaker)
            formatted_data = format_training_data(parsed_data)

            # Append the cleaned data to the existing training data
            training_data.extend(formatted_data)
            custom_data["training_data"] = training_data

            # Append the new file hash to the file_hashes list
            file_hashes.append(file_hash)
            custom_data["file_hashes"] = file_hashes

            # Save the updated custom data back to the JSON file
            save_custom_data(custom_data_filepath, custom_data)

            print("Data has been cleaned and appended to the Knowledge_base JSON file.".upper())
            print("The model will now learn from this data.")
        else:
            print("Data has not been cleaned nor appended to the knowledge base.".upper())
            print("The model will not learn from this data.")

    choice = input("DO YOU WISH TO CLEAN ANOTHER EXPORTED FILE (ENTER (yes/no)): ").lower()
    if choice == "no":
        break