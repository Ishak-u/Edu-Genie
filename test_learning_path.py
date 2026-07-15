from learning_path import get_learning_recommendations

topic = input("Enter a Topic: ")

print("\nGenerating Learning Path...\n")

print(get_learning_recommendations(topic))