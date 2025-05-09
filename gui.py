import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os

# Global variables
diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

# Load data from files
def preprocess():
    global diseases_list, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map

    with open("diseases.txt", "r") as file:
        diseases_list = file.read().strip().split("\n")

    for disease in diseases_list:
        symptom_file = os.path.join("Disease symptoms", f"{disease}.txt")
        desc_file = os.path.join("Disease descriptions", f"{disease}.txt")
        treatment_file = os.path.join("Disease treatments", f"{disease}.txt")

        if os.path.exists(symptom_file):
            with open(symptom_file, "r") as file:
                symptoms = [s.strip().lower() for s in file.read().split("\n")]
                full_symptom_tuple = tuple(symptoms)
                diseases_symptoms.append(full_symptom_tuple)
                symptom_map[full_symptom_tuple] = disease

        if os.path.exists(desc_file):
            with open(desc_file, "r") as file:
                d_desc_map[disease] = file.read().strip()

        if os.path.exists(treatment_file):
            with open(treatment_file, "r") as file:
                d_treatment_map[disease] = file.read().strip()

# Match symptoms exactly
def identify_disease(symptoms_tuple):
    return symptom_map.get(symptoms_tuple)

# Fuzzy match if no exact match
def fuzzy_match(symptoms_tuple):
    max_overlap = 0
    best_match = None
    for known_symptoms in symptom_map:
        overlap = sum(1 for a, b in zip(symptoms_tuple, known_symptoms) if a == b and a != "no")
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = known_symptoms
    return symptom_map.get(best_match)

# Get details
def get_details(disease):
    return d_desc_map.get(disease, "No details available.")

# Get treatment
def get_treatments(disease):
    return d_treatment_map.get(disease, "No treatment available.")

# Analyze symptoms and display result
def analyze_symptoms():
    symptoms_tuple = tuple(var.get().strip().lower() for var in symptom_vars)
    print("Symptom tuple:", symptoms_tuple)
    disease = identify_disease(symptoms_tuple)

    if disease:
        details = get_details(disease)
        treatment = get_treatments(disease)
        result_text = f"✅ Exact Match Found\n\nPredicted Disease: {disease}\n\n📄 Description:\n{details}\n\n💊 Treatment:\n{treatment}"
    else:
        best_guess = fuzzy_match(symptoms_tuple)
        if best_guess:
            details = get_details(best_guess)
            treatment = get_treatments(best_guess)
            result_text = f"⚠️ No exact match. Most probable disease based on your symptoms:\n\nPredicted Disease: {best_guess}\n\n📄 Description:\n{details}\n\n💊 Treatment:\n{treatment}"
        else:
            result_text = "❌ No matching disease found."

    result_box.config(state=tk.NORMAL)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result_text)
    result_box.config(state=tk.DISABLED)

# Load data
preprocess()

# GUI Setup
root = tk.Tk()
root.title("Disease Diagnosis System")
root.geometry("700x850")
root.configure(bg="#f0f4f7")

# Header
tk.Label(root, text="🩺 Disease Diagnosis System", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#2c3e50").pack(pady=15)

# Instructions
tk.Label(root, text="Select symptom severity:", font=("Arial", 14), bg="#f0f4f7").pack(pady=5)

symptom_labels = [
    "Headache", "Cough", "Chest Pain", "Restlessness", "Fatigue", "Sunken Eyes", "Blurred Vision", 
    "Sore Throat", "Fainting", "Back Pain", "Nausea", "Low Body Temperature", "Fever"
]

options = ["High", "Low", "No"]
symptom_vars = [tk.StringVar(value="No") for _ in symptom_labels]

for i, label in enumerate(symptom_labels):
    frame = tk.Frame(root, bg="#f0f4f7")
    frame.pack(fill="x", padx=100, pady=3)
    tk.Label(frame, text=label, bg="#f0f4f7", width=20, anchor="w").pack(side="left")
    tk.OptionMenu(frame, symptom_vars[i], *options).pack(side="right")

# Analyze Button
tk.Button(root, text="Analyze", command=analyze_symptoms, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=20)

# Scrollable Result Display
tk.Label(root, text="Diagnosis Result:", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=(10, 5))
result_box = ScrolledText(root, width=80, height=20, wrap=tk.WORD, font=("Consolas", 11), bg="#ffffff", fg="#2c3e50", borderwidth=2, relief="groove")
result_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
result_box.config(state=tk.DISABLED)

root.mainloop()
