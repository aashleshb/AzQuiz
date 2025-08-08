# AzQuiz 🧠  
**Your personal Azure AZ-104 exam practice app**  

AzQuiz is an interactive quiz application built in Python to help you prepare for the **Microsoft Azure Administrator (AZ-104)** certification.  
It provides a clean interface, multiple question sets, progress tracking, review mode, and automatic scoring with pass/fail evaluation.  

---

## 🚀 Features
- **Multiple question sets** (stored in JSON format)  
- **Question & option shuffling** for varied practice  
- **Progress indicator** (e.g., *Question 5 of 20*)  
- **Instant feedback** with explanations  
- **Review mode** with color-coded answers  
- **Final score & pass/fail result**  
- **No internet required** — runs locally on your machine  

---

## 📂 Folder Structure

AzQuiz/
├── main.py              # Entry point for the application
├── gui.py               # Graphical interface for quiz mode
├── cli.py               # Command-line version of the quiz
├── app.py               # Application logic (web mode)
├── config.py            # Configurable settings (shuffle, pass rate, etc.)
├── utils/               # Helper functions
│   └── loader.py        # Functions to load question files
├── templates/           # HTML templates for web interface
│   ├── index.html       # Homepage template
│   ├── quiz.html        # Quiz page template
│   ├── review.html      # Review answers page template
│   └── complete.html    # Quiz completion page template
├── data/                # JSON files with question sets
│   ├── set1.json
│   ├── set2.json
│   └── …
└── pycache/         # Python cache files (auto-generated)

---

## ⚙️ Configuration

Edit **`config.py`** to customize app behavior:  
```python
SHUFFLE_QUESTIONS = True   # Randomize question order
SHUFFLE_OPTIONS = True     # Randomize answer options
SHOW_FEEDBACK = True       # Show immediate feedback
PASS_THRESHOLD = 70        # % required to pass
DEFAULT_QUESTION_SET = "data/set1.json"

📦 Question Format

Each question set is a JSON file like:

[
  {
    "id": 1,
    "question": "Which Azure service provides scalable cloud storage?",
    "options": ["Azure Blob Storage", "Azure VM", "Azure SQL", "Azure Functions"],
    "correct": "Azure Blob Storage",
    "explanation": "Blob Storage is optimized for storing massive amounts of unstructured data."
  }
]

✅ For multiple correct answers, separate them with commas.

⸻

🖥️ Running the App

Run GUI mode:
python gui.py

Run CLI mode:
python cli.py

Run Web mode:
python app.py
Then open your browser and go to: http://127.0.0.1:5000

📜 Disclaimer

This app is not an official Microsoft product, and the questions included are not official exam questions. They were created based on publicly available learning materials to help with personal study.

I am not a professional app developer — I built this tool to practice AZ-104 questions on my laptop. If you find any issues or mistakes, please feel free to submit corrections or improvements via the GitHub repository.

➕ Adding Your Own Questions
	1.	Create a new JSON file in data/ (e.g., set9.json)
	2.	Follow the same format as above
	3.	Your new set will appear in the app’s set selector automatically

🏁 Summary

AzQuiz is your local study companion for AZ-104.
Pick your mode (GUI, CLI, or Web), choose a question set, test yourself, review explanations, and get exam-ready.

💡 Quick Commands
# Start GUI mode
python gui.py

# Start CLI mode
python cli.py

# Start Web mode
python app.py

Good luck with your AZ-104 exam prep!
Feel free to contribute improvements or additional question sets via GitHub.