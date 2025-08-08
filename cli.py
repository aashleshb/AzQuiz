from utils.loader import load_questions

def run_quiz():
    questions = sorted(load_questions("data/set1.json"), key=lambda q: q['id'])
    score = 0

    for q in questions:
        print(f"\nQ{q['id']}: {q['question']}")
        for i, opt in enumerate(q['options'], 1):
            print(f"  {i}. {opt}")

        try:
            choice = int(input("Your answer (1-4): "))
            selected = q['options'][choice - 1]
        except (ValueError, IndexError):
            print("⚠️ Invalid input. Skipping question.")
            continue

        if selected == q['correct']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {q['correct']}")

    print(f"\n🎯 Quiz Complete! Your score: {score}/{len(questions)}")

if __name__ == "__main__":
    run_quiz()
