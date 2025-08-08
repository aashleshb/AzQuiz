import tkinter as tk
from tkinter import messagebox
from utils.loader import load_questions
import config
import random
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure 104 Quiz")

        self.available_sets = self.get_question_sets()
        self.question_set = tk.StringVar(value=self.available_sets[0] if self.available_sets else config.DEFAULT_QUESTION_SET)

        self.questions = []
        self.current_index = 0
        self.score = 0
        self.selected_vars = []
        self.review_data = []

        self.setup_menu()

    def get_question_sets(self):
        sets = []
        data_dir = "data"
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith(".json") and file.startswith("set"):
                    sets.append(os.path.join(data_dir, file))

        sets.sort(key=lambda f: int(''.join(filter(str.isdigit, os.path.basename(f))))
                  if any(char.isdigit() for char in os.path.basename(f)) else 0)
        return sets

    def setup_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select Question Set:").pack(pady=10)

        dropdown = tk.OptionMenu(self.root, self.question_set, *self.available_sets)
        dropdown.pack()

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)

    def start_quiz(self):
        try:
            self.questions = load_questions(self.question_set.get())
        except FileNotFoundError:
            messagebox.showerror("Error", f"Question set '{self.question_set.get()}' not found.")
            return

        if config.SHUFFLE_QUESTIONS:
            random.shuffle(self.questions)

        self.score = 0
        self.current_index = 0
        self.review_data = []
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.current_index >= len(self.questions):
            self.show_summary()
            return

        q = self.questions[self.current_index]
        options = q['options'][:]
        if config.SHUFFLE_OPTIONS:
            random.shuffle(options)

        # ✅ Progress label
        progress_text = f"Question {self.current_index + 1} of {len(self.questions)}"
        tk.Label(self.root, text=progress_text, font=("Arial", 12)).pack(pady=(10, 0))

        tk.Label(self.root, text=f"Q{q['id']}: {q['question']}", wraplength=400, justify="left").pack(pady=10)

        self.selected_vars = []
        for opt in options:
            var = tk.BooleanVar()
            self.selected_vars.append((opt, var))
            tk.Checkbutton(self.root, text=opt, variable=var, wraplength=400, anchor="w", justify="left").pack(fill="x", padx=20)

        tk.Button(self.root, text="Submit", command=lambda: self.check_answer(q)).pack(pady=10)

    def check_answer(self, question):
        selected = [opt for opt, var in self.selected_vars if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one option.")
            return

        correct_list = [c.strip() for c in question['correct'].split(',')]
        is_correct = set(selected) == set(correct_list)

        if is_correct:
            self.score += 1
            feedback = "✅ Correct!"
            if config.SHOW_FEEDBACK and 'explanation' in question:
                feedback += f"\n🧠 {question['explanation']}"
        else:
            feedback = f"❌ Incorrect.\nCorrect: {', '.join(correct_list)}"
            if config.SHOW_FEEDBACK and 'explanation' in question:
                feedback += f"\n📘 {question['explanation']}"

        self.review_data.append({
            'id': question['id'],
            'question': question['question'],
            'selected': selected,
            'correct': correct_list,
            'is_correct': is_correct,
            'explanation': question.get('explanation', '')
        })

        messagebox.showinfo("Feedback", feedback)
        self.current_index += 1
        self.show_question()

    def show_summary(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        total = len(self.questions)
        percent = (self.score / total) * 100
        status = "✅ Passed" if percent >= config.PASS_THRESHOLD else "❌ Failed"
        color = "green" if percent >= config.PASS_THRESHOLD else "red"

        tk.Label(self.root, text=f"🎯 Final Score: {self.score}/{total}", font=("Arial", 14)).pack(pady=(20, 5))
        tk.Label(self.root, text=f"{status} ({percent:.1f}%)", font=("Arial", 12), fg=color).pack(pady=(0, 20))

        tk.Button(self.root, text="Review Answers", command=self.show_review).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack()

    def show_review(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="📋 Review", font=("Arial", 14)).pack(pady=10)

        # ✅ Scrollable canvas setup
        canvas = tk.Canvas(self.root, height=500)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ✅ Populate review content
        for item in self.review_data:
            frame = tk.Frame(scroll_frame, bd=1, relief="solid", padx=10, pady=5)
            frame.pack(fill="x", padx=10, pady=5)

            tk.Label(frame, text=f"Q{item['id']}: {item['question']}", wraplength=400, justify="left").pack(anchor="w")

            if item['selected']:
                for ans in item['selected']:
                    color = "green" if ans in item['correct'] else "red"
                    tk.Label(frame, text=f"Your answer: {ans}", fg=color).pack(anchor="w")
            else:
                tk.Label(frame, text="No answer selected", fg="gray").pack(anchor="w")

            if not item['is_correct']:
                tk.Label(frame, text=f"Correct answer: {', '.join(item['correct'])}", fg="blue").pack(anchor="w")

            if item['explanation']:
                tk.Label(frame, text=f"🧠 {item['explanation']}", wraplength=400, justify="left", fg="gray").pack(anchor="w")

        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
