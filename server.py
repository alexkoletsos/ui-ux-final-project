from flask import Flask, render_template
from flask import Response, request, jsonify

app = Flask(__name__)

# Data
rules = [
    {
     "id": 1,
     "contact_type": "contact while throwing",
     "definition": "non-minor contact between the thrower and the marker is considered a foul on the defender; examples include contact with the thrower’s hand during the throwing motion.",
     "terms": ['thrower', 'marker', 'stall count'],
     "relevant_info": ["contact occurring during the follow through (after the disc has been released) is not a foul.", "if the foul is called after the throw goes off and the pass is not completed, the disc returns to the thrower.", "when a foul is committed by the marker, the stall count goes down to 0."],
     "media": [['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'an example of a contested foul. from the frame-by-frame, we can see that the defender contacts the disc before the offender does; however, the offender claimed to stop rotation of the disc before the defender got to it, thus calling a foul. it was contested, so the disc goes back to the thrower.'], ['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'hi hi hi.']]},
    {
     "id": 2,
     "contact_type": "contact while catching",
     "definition": "non-minor contact between opposing players while, or directly after, either player makes a play on the disc; examples include contact with anopponent’s extended arms or hands that are about to, or already are, contacting the disc.",
     "terms": ['play on the disc', 'legitimately positioned', 'contested', 'uncontested'],
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul.", "if a catching foul occurs and is uncontested, the player fouled gains possession at the point of the infraction. If the call is contested, the disc goes back to the thrower."],
     "media": [['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'an example of a contested foul. from the frame-by- frame, we can see that the defender contacts the disc before the offender does; however, the offender claimed to stop rotation of the disc before the defender got to it, thus calling a foul. it was contested, so the disc goes back to the thrower.'], ['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'hi hi hi.']]},
    {
     "id": 3,
     "contact_type": "contact away from the disc",
     "definition": "it is the responsibility of all players to avoid contact in any way possible. violent impact with legitimately positioned opponents constitutes harmful endangerment, a foul, and must be strictly avoided.",
     "terms": ['violent impact', 'endangerment'],
     "relevant_info": ["if the foul is accepted, the fouled player may make up any positional disadvantage caused by the foul."],
     "media": [['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'an example of a contested foul. from the frame-by- frame, we can see that the defender contacts the disc before the offender does; however, the offender claimed to stop rotation of the disc before the defender got to it, thus calling a foul. it was contested, so the disc goes back to the thrower.'], ['catching_1.mp4', ['catching_pic_1.jpg', 'catching_pic_2.jpg'], 'hi hi hi.']]}
    ]
fouls = [
    {"foul_type": "offensive",
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul."],
     "media": ['offensive.mp4', ['offensive-1.jpg', 'offensive-2.jpg', 'offensive-3.jpg'], ['offensive-w-1.jpg', 'offensive-w-2.jpg', 'offensive-w-3.jpg']]},
    {"foul_type": "defensive",
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul.", "non-minor contact between the thrower and the marker is considered a foul."],
     "media": ['offensive.mp4', ['offensive-1.jpg', 'offensive-2.jpg', 'offensive-3.jpg'], ['offensive-w-1.jpg', 'offensive-w-2.jpg', 'offensive-w-3.jpg']]} 
    ]


quiz = [
    {
        "id": 1,
        "type": "multiple choice",
        "question": "is this a foul? if so, which type?",
        "video":'defensive_foul.mp4',
        "media": None,
        "responses": ["yes - offensive foul", "yes - defensive foul", "no, not a foul"],
        "correct": "yes - defensive foul"
    },
    {
        "id": 2,
        "type": "multiple choice",
        "question": "where did the foul occur?",
        "video": None,
        "media": {"frame a": "quiz2_a.jpg", "frame b": "quiz2_b.jpg", "frame c": "quiz2_c.jpg"},
        "responses": ["frame a", "frame b", "frame c"],
        "correct": "frame c"
    },
    {
        "id": 3,
        "type": "multiple choice",
        "question": "if a foul is contested, where does the disc go?",
        "video": None,
        "media": None,
        "responses": ["the disc stays with the player who called the foul.", "the disc goes back to the player who threw the disc previously.", "the player who contested the foul gets possession of the disc."],
        "correct": "the disc goes back to the player who threw the disc previously."
    },
    {
        "id": 4,
        "type": "multiple choice",
        "question": "which space would be dangerous for the defender to enter if the offender is running in the direction of the black arrow?",
        "video": None,
        "media": ["quiz3.jpg"],
        "responses": ["space A", "space B", "space C", "space D"],
        "correct": "space B"
    },
    {
        "id": 5,
        "type": "interactive",
        "question": "enter the correct frame corresponding to each description",
        "video": None,
        "media": {"a.": "quiz5_a.png", "b.": "quiz5_b.png", "c.": "quiz5_c.png"},
        "responses": {"1": "one player jumps into another’s vertical space.", "2": "one player is positioned stationary and prepares to jump up for the disc.", "3": "one player initiates contact by jumping into his opponent’s vertical space."},
        "correct": {"1":"b", "2":"a", "3":"c"}
    }
]

quiz_ans = [

    {
        "id": 1,
        "answer": None
    },
    {
        "id": 2,
        "answer": None
    },
    {
        "id": 3,
        "answer": None
    },
    {
        "id": 4,
        "answer": None
    },
    {
        "id": 5,
        "answer": None
    },

]

# ROUTES 

@app.route('/')
def home():
    is_home_page = True
    return render_template('home.html', is_home_page = is_home_page) 

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/rules/<string:contact_type>')
def contact_rules(contact_type):
    contact_type = contact_type.replace("-", " ")
    item = None
    for rule in rules:
        if rule["contact_type"] == contact_type:
            item = rule
            break
    return render_template('rules_of_contact.html', rule=item, rules=rules)

@app.route('/identifying-fouls/<string:foul_type>')
def identifying_fouls(foul_type):
    item = None
    for foul in fouls:
        if foul["foul_type"] == foul_type:
            item = foul
            break
    return render_template('identifying_fouls.html', foul=item, fouls=fouls)

@app.route('/<string:section>')
def section_home(section):
    description = ''
    url = ''
    if section == 'rules':
        section = 'part 1: rules of contact'
        description = 'frisbee is a non-contact sport, so what happens when contact is drawn?'
        url = 'rules/contact-while-throwing'
    if section == 'identifying-fouls':
        section = 'part 2: identifying fouls'
        description = "frisbee is a self-refereed sport, so let's learn how to make the right call against our opponents."
        url = 'identifying-fouls/offensive'
    if section == 'quiz':
        section = 'part 3: test your knowledge'
        description = "you've completed the lesson! find out if you're a frisbee expert."
        url = 'quiz/1'
    return render_template('section_home.html', section=section, description=description, url=url)


@app.route('/quiz/<string:id>')
def quiz_question(id):

    id = int(id)
    item = None
    question_type = None
    for question in quiz:
        if question["id"] == id:
            item = question
            question_type = question["type"]
            break
    if question_type == "multiple choice":
        return render_template('quiz_mc.html', question=item)
    else:
        return render_template('quiz_interactive.html', question=item)
    
@app.route('/quiz_results')
def display_results():

    global quiz_ans

    global quiz

    result = {}

    for question, answer in zip(quiz, quiz_ans):
        question_id = question["id"]
        correct_answer = question["correct"]
        user_answer = answer["answer"]
        if user_answer == correct_answer:
            result[question_id] = True
        else:
            result[question_id] = False

    correct_num = 0
    for item in result.values():
        if item:
            correct_num += 1

    return render_template('quiz_results.html', result=result, correct_num=correct_num)
    
@app.route('/store_response', methods=['POST'])
def store_response():

    global quiz_ans
    
    data = request.get_json()
    
    response = data['response']
    question_id = data['question_id']
    
    for qa in quiz_ans:
        if qa['id'] == int(question_id):
            qa['answer'] = response
            break
    
    return jsonify(quiz_ans = quiz_ans)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():

    global quiz_ans
    
    data = request.get_json()
    
    response = data['response']
    question_id = data['question_id']
    
    for qa in quiz_ans:
        if qa['id'] == int(question_id):
            qa['answer'] = response
            break
    
    return jsonify(quiz_ans = quiz_ans)

if __name__ == '__main__':
   app.run(debug=True)





