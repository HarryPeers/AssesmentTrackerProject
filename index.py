from datetime import datetime
from os import path, getcwd
from sys import stderr
import json

global cwd
cwd = getcwd()

global scores

if not path.exists(f"{cwd}/scores.json"):
    with open(f"{cwd}/scores.json", "w") as file:
        file.write("{}")
    scores = {}
else:
    with open(f"{cwd}/scores.json", "r") as file:
        scores = json.load(file)
 
global datetime
date = datetime.now().strftime('%d/%m/%Y')

global positives
positives = ["yes", "y", "yea", "1", "true"]

def save_records():
    with open(f"{cwd}/scores.json", "w") as file:
        json.dump(scores, file, indent=3)

def get_grade(score:int):
    if score >= 80:
        return "A*"
    elif score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"

def insert_scores():
    """
        Iterate until they choose to break, then call insert_score
    """
    _date = input("Is the date today?\n")
    if _date.lower() not in positives:
        selected_date = input("Please enter the date of the assesment in dd/mm/yyyy form\n")
    else:
        selected_date = date

    assesment_name = input("\nPlease enter the assesment name\n")

    tutors_name = input("\nPlease enter the assessors name\n")
     
    while True:
        value = input("\nType 'exit' to exit\nPlease enter the name followed by the score in the following format:\n    Harry peers, 97\n")
        if value.lower() == "exit":
            break
        
        if "," not in value:
            print("\nPlease enter a valid score in the following format:\n    Harry peers, 97", file=stderr)
            continue

        segments = value.split(",")
        name, score = segments[0].lower().strip(), segments[1].strip()

        try:
            """
            If score is not a valid number, raise an error
            """
            score = int(score)
        except:
            print("\nThat score is not a number!", file=stderr)
            continue

        """
        If name already exists in score, append to their record, else create a record (uses ints so it can store many records for each student
        """

        grade = get_grade(score)
        value = {"name": name, "score": score, "date": selected_date, "grade": grade, "assesment": assesment_name, "tutors_name": tutors_name}

        if name in scores.keys():
            scores[name].append(value)
        else:
            scores[name] = [value]
        
        save_records()

        print(f"\n{name} got a grade {grade}")

def insert_score(score:dict):
    """
        Insert to a list stored in a .json file.
    """

def read_scores():
    """
        Print out each value in file.
    """
    if len(scores.keys()) == 0:
        print("\nNo scores available!", file=stderr)
        return
    
    print("")
    
    for name in scores.keys():
        print(f"{name}")
        for score in scores[name]:
            print(f"    {score['assesment']}, {score['date']}, {score['grade']} ({score['score']}) by {score['tutors_name']}")
        print("\n")

def erase_scores():
    """
        Reset the file
    """
    global scores
    scores = {}
    
    with open(f"{cwd}/scores.json", "w") as file:
        file.write("{}")

    print("\nScores erased\n")

def search():
    """
        Search for a student.
    """

    name = input("\n\nPlease enter a student name!\n").lower()
    if name not in scores.keys():
        print("\nStudent doesnt exist!", file=stderr)
        return
    
    print(f"\n{name}")
    for score in scores[name]:
        print(f"    {score['assesment']}, {score['date']}, {score['grade']} ({score['score']}) by {score['tutors_name']}")
    print("\n")
    

while True:
    mode = input("Please enter a mode:\n   1) Insert scores\n   2) Read scores\n   3) Erase scores\n   4) Search student\n   5) Exit\n")
    
    try:
        """
        If exception is raised the inputted option is not a int or a possible option.
        """
        mode = int(mode)
        if mode not in range(1,6):
            raise
    except:
        print("That isnt a valid option!", file=stderr)
        continue

    if mode == 1:
        insert_scores()
    elif mode == 2:
        read_scores()
    elif mode == 3:
        erase_scores()
    elif mode == 4:
        search()
    elif mode == 5:
        break
