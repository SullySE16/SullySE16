import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class MBT():

    def __init__(self, name, image):
        self.name = name
        self.image = image

T72 = MBT('T72','T72.jpg')
T64 = MBT('T64','T64.jpg')
Leopard2 = MBT('Leopard 2', 'leopard2.jpg')
Challenger2 = MBT('Challenger 2', 'challenger2.jpg')
M1A1 = MBT('M1A1 Abrams', 'M1A1.jpg')

tanks = [T72, T64, Leopard2, Challenger2, M1A1]
random.shuffle(tanks)



questions = [
    {
        'question': 'Select the name of the AFV from the options below.',
        'image': tanks[0].image,  # Image file for question 1
        'choices': [tanks[0].name, tanks[1].name, tanks[2].name, tanks[3].name],
        'correct_choice': tanks[0].name
    },
    {
        'question': 'Select the name of the AFV from the options below.',
        'image': tanks[1].image,  # Image file for question 1
        'choices': [tanks[3].name, tanks[1].name, tanks[0].name, tanks[2].name],
        'correct_choice': tanks[1].name
    },
    {
        'question': 'Select the name of the AFV from the options below.',
        'image': tanks[2].image,  # Image file for question 1
        'choices': [tanks[1].name, tanks[3].name, tanks[2].name, tanks[0].name],
        'correct_choice': tanks[2].name 
    },
    {
        'question': 'Select the name of the AFV from the options below.',
        'image': tanks[3].image,  # Image file for question 1
        'choices': [tanks[0].name, tanks[1].name, tanks[2].name, tanks[3].name],
        'correct_choice': tanks[3].name}]



score = 0
# Global variable to keep track of the current question index
current_question_index = 0

random.shuffle(questions)

@app.route('/', methods=['GET', 'POST'])
def quiz():
    global current_question_index
    global score
    
    if request.method == 'POST':

        # Get the user's answer from the form
        user_answer = request.form.get('choice')

        # Check if the user's answer is correct
        correct_answer = questions[current_question_index]['correct_choice']
        is_correct = user_answer == correct_answer
        if is_correct:
            score = score+1

        # Move to the next question
        current_question_index += 1

        if current_question_index < len(questions):
            return render_template('quiz.html', question=shuffle_choices(questions[current_question_index]), is_correct=is_correct)
        else:
            return render_template('results.html', is_correct=is_correct, score=score)

    return render_template('quiz.html', question=shuffle_choices(questions[current_question_index]), is_correct=None)

def shuffle_choices(question):
    # Randomly shuffle the choices for a given question
    shuffled_choices = question['choices'][:]
    random.shuffle(shuffled_choices)
    question['choices'] = shuffled_choices
    return question

@app.route('/restart')
def restart_quiz():
    global current_question_index
    global score
    random.shuffle(questions)
    current_question_index = 0
    score = 0
    
    return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True)
