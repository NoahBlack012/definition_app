import random

def create_mc(concept, definition, data_values):
    question = {}
    question["question"] = f"What does {concept} mean?"
    question["correct_answer"] = definition

    answers = [i for i in data_values if i != definition]
    if len(answers) > 2:
        answers = random.sample(answers, 3)
    answers.append(definition)
    random.shuffle(answers)

    question["answers"] = answers
    return question

def create_quiz(data, length):
    """Function that takes in data of topic and length of quiz and generates a array of dicts (Questions) to generate a quiz"""
    data_keys = list(data.keys())
    data_values = list(data.values())
    quiz = []
    indexes_used = []
    for i in range(length):
        try:
            while index in indexes_used:
                index = random.randint(0, len(data) - 1)
        except NameError:
            index = 0
        indexes_used.append(index)
        concept = data_keys[index]
        definition = data[concept]

        question = create_mc(concept, definition, data_values)
        quiz.append(question)

    return quiz





