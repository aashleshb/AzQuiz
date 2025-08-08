import os
import json
import logging

def load_questions(set_name):
    # Get absolute path to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(project_root, 'data')  # ✅ resolves to /Azure 104 exam/data

    # Debug prints to trace path resolution
    print("🔍 DEBUG PATHS:")
    print("current_dir =", current_dir)
    print("project_root =", project_root)
    print("data_dir =", data_dir)

    # Normalize filename
    filename = os.path.basename(set_name)
    if not filename.endswith('.json'):
        filename += '.json'
    print("filename =", filename)

    filepath = os.path.join(data_dir, filename)
    print("FINAL FILEPATH =", filepath)

    logging.debug(f"🔍 Looking for question file at: {filepath}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Question set not found at: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Failed to parse JSON: {e}")

    valid_questions = []
    for i, q in enumerate(questions):
        if not all(k in q for k in ('id', 'question', 'correct', 'options')):
            logging.warning(f"⚠️ Skipping malformed question at index {i}: {q}")
            continue
        valid_questions.append(q)

    if not valid_questions:
        raise ValueError(f"❌ No valid questions found in: {filepath}")

    valid_questions.sort(key=lambda q: q['id'])
    logging.info(f"✅ Loaded {len(valid_questions)} valid questions from '{filename}'")
    return valid_questions
