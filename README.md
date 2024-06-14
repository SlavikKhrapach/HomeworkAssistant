# AI Homework Assistant

## Description
AI Homework Assistant is a Flask web application that allows users to fetch and display their course assignments from an API (Canvas). It provides detailed summaries of assignments using the Groq API.

## Features
- Fetch assignments using course IDs and access tokens.
- Filter assignments by various categories (e.g., upcoming, overdue, past).
- View detailed information and summaries of individual assignments.
- Maintain session state for user inputs.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/SlavikKhrapach/HomeworkAssistant.git
   cd HomeworkAssistant
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt

## Usage
1. **Run the application**:
   ```bash
   python main.py
2. **Access the web application**:
   Open your web browser and navigate to http://127.0.0.1:5000.
3. Fetch assignments:
   - Enter your course IDs, Canvas access token, and Groq API key on the home page.
   - Submit the form to view and filter assignments.

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Contact
For questions or support, please reach out to SlavikKhrapach@gmail.com

