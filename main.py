import random
import sys
from utils.loader import load_questions
import config

def run_quiz(questions):
    if config.SHUFFLE_QUESTIONS:
        random.shuffle(questions)

    score = 0
    for q in questions:
        options = q['options'][:]
        if config.SHUFFLE_OPTIONS:
            random.shuffle(options)

        print(f"\nQ{q['id']}: {q['question']}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

        try:
            choice = int(input("Your answer (1-4): "))
            selected = options[choice - 1]
        except (ValueError, IndexError):
            print("⚠️ Invalid input. Skipping question.")
            continue

        if selected == q['correct']:
            if config.SHOW_FEEDBACK:
                print("✅ Correct!")
                if 'explanation' in q and q['explanation']:
                    print(f"🧠 Why it's correct: {q['explanation']}")
            score += 1
        else:
            if config.SHOW_FEEDBACK:
                print(f"❌ Incorrect. Correct answer: {q['correct']}")
                if 'explanation' in q and q['explanation']:
                    print(f"📘 Explanation: {q['explanation']}")

    if config.SHOW_SUMMARY:
        print(f"\n🎯 Final Score: {score}/{len(questions)}")

if __name__ == "__main__":
    # Get question set name from command-line or fallback to default
    question_set = sys.argv[1] if len(sys.argv) > 1 else config.DEFAULT_QUESTION_SET
    print(f"📦 Loading question set: {question_set}")
    questions = load_questions(question_set)
    run_quiz(questions)
