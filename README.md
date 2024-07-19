# healthbot-eve


Features
Health and Wellness Advice: Provides expert health tips and answers to health-related questions.
Mathematical Evaluation: Can evaluate and return results for mathematical expressions.
User Interaction: Handles greetings, farewells, and common exit commands.
Help Command: Offers a help message detailing available commands.
Session Management: Allows users to clear chat history and access login/register pages.
Requirements
Python 3.6+
Flask
ChatterBot
NLTK
SymPy
JSON file with health-related training data

Installation
Clone the Repository:


git clone https://github.com/your-username/your-repository.git
cd your-repository
Install Dependencies:

Create a virtual environment and install the required packages:


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Make sure requirements.txt includes:


Flask
ChatterBot
nltk
sympy
Download NLTK Data:

Run the following commands to download necessary NLTK data:

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
Prepare the Knowledge Base:

Ensure you have a knowledge_base.json file in the root directory of the project. This file should contain health-related training data structured as:

json
Copy code
{
    "training_data": [
        "question1",
        "answer1",
        "question2",
        "answer2"
    ]
}
Running the Application
To start the application, run:


python eve.py
The application will be available at http://localhost:5000.


User Guide
Welcome to EVE, your personal health and wellness assistant! EVE is designed to help you with health-related questions and provide useful advice.

Getting Started
To begin interacting with EVE:
1. Visit the chat interface at [your chatbot URL] (e.g., http://localhost:5000).
2. Type your message in the input box and click the "Send" button.

Basic Commands
- Asking Questions: Type any health-related question directly to get advice or information.
- Exiting the Chat: Type 'stop', 'exit', 'quit', or 'bye' to end the chat session.
- Help: Type 'help' to display a list of commands and instructions.

Special Features
EVE can handle various types of interactions;
- Greeting: EVE responds to greetings like "hello", "hi", or "hey".
- Farewells: To end the conversation, use phrases like "goodbye" or "see you".
- Mathematical Queries: EVE can perform basic mathematical calculations. Just enter a mathematical expression, and EVE will evaluate it.

Additional Functions
- Clear Chat History: Click the 'Clear' button to erase the chat history and start fresh.

Example Interactions
- YOU: "Hi there!"
  - EVE: "Hello! How can I assist you today?"

- YOU: "What are some tips for staying healthy?"
  - EVE: [Provides health tips from knowledge base]

- YOU: "2 + 2"
  - EVE: "4"

Troubleshooting
If EVE doesn't understand your query or if you encounter any issues:
- Check your spelling and phrasing.
- Ensure your internet connection is stable.

Enjoy Your Chat!
Feel free to explore EVE's capabilities and ask any health-related questions you have. Have a great conversation!

Additional Information
- Developers: John Maina Wambui
	         Joyita Mithamo Njoki
	         Dwayne Masinde Lawrence
	         Isaac Maina Muraya
- Version: 1.0
- Last Updated: July 17, 2024

For any feedback or suggestions, please reach out to us at;
wambuijonmaina@gmail.com
Joyritanjoki061@gmail.com
maslawayne@gmail.com
Isaacmuraya254@gmail.com

Thank you for using EVE!

