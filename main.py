import tkinter as tk
from tkinter import messagebox, scrolledtext
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

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result_text)
    result_box.config(state="disabled")

# Load data
preprocess()

# GUI Setup
root = tk.Tk()
root.title("Disease Diagnosis System")
root.geometry("600x700")

tk.Label(root, text="Select symptom severity:", font=("Arial", 14)).pack(pady=10)

symptom_labels = [
    "Headache", "Cough", "Chest Pain", "Restlessness", "Fatigue", "Sunken Eyes", "Blurred Vision", 
    "Sore Throat", "Fainting", "Back Pain", "Nausea", "Low Body Temperature", "Fever"
]

options = ["High", "Low", "No"]
symptom_vars = [tk.StringVar(value="No") for _ in symptom_labels]

for i, label in enumerate(symptom_labels):
    tk.Label(root, text=label).pack()
    tk.OptionMenu(root, symptom_vars[i], *options).pack()

tk.Button(root, text="Analyze", command=analyze_symptoms, bg="green", fg="white").pack(pady=10)

# Scrollable Result Display
tk.Label(root, text="Diagnosis Result:").pack()
result_box = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
result_box.pack(pady=5)
result_box.config(state="disabled")

root.mainloop()
