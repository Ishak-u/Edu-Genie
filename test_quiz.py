from quiz_module import generate_quiz

print("Enter a paragraph:\n")

paragraph = input()

result = generate_quiz(paragraph)

print()

if result["success"]:

    for i, q in enumerate(result["quiz"], start=1):

        print(f"Question {i}")

        print(q["question"])

        for key, value in q["options"].items():
            print(f"{key}. {value}")

        print("Correct Answer:", q["correct_answer"])

        print("-" * 40)

else:

    print(result)