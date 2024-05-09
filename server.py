from flask import Flask, render_template
from flask import Response, request, jsonify

app = Flask(__name__)

# Data
rules = [
    {
     "id": 1,
     "contact_type": "contact while throwing",
     "definition": "non-minor contact between the thrower and the marker is considered a foul on the defender; examples include contact with the thrower’s hand during the throwing motion.",
     "terms": {
        "thrower": "the player who possesses the disc and intends to pass it to a teammate by throwing it.",
        "marker": "the defender who is guarding the thrower, attempting to prevent them from making a successful throw.",
        "stall count": "the count, usually from 1 to 10, indicating the maximum time a thrower has to release the disc after the marker has initiated the stall count."
     },
     "relevant_info": ["contact occurring during the follow through (after the disc has been released) is not a foul.", "if the foul is called after the throw goes off and the pass is not completed, the disc returns to the thrower.", "when a foul is committed by the marker, the stall count goes down to 0."],
     "media": [['contact-throwing-1.mp4', ['contact-throwing-1-pic-1.jpg', 'contact-throwing-1-pic-2.jpg'], "in this example, the marker smacks the disc out of the thrower's hand before the disc is released. this interferes with the throw and does not constitute as legal defense. after this call, the disc goes back to the thrower."], ['contact-throwing-2.mp4', ['contact-throwing-2-pic-1.jpg', 'contact-throwing-2-pic-2.jpg'], "in this example, the marker contacts the thrower's hand at the disc's point of release. as seen in the video, the disc is able to go off but the contact initiated by the marker with the thrower's hand before the disc is released constitutes as non-minor contact. after this call, the disc goes back to the thrower."]]},
    {
     "id": 2,
     "contact_type": "contact while catching",
     "definition": "non-minor contact between opposing players while, or directly after, either player makes a play on the disc; examples include contact with an opponent’s extended arms or hands that are about to, or already are, contacting the disc.",
     "terms": {
                "play on the disc": "any action related to attempting to catch, intercept, or defend the disc during play.",
                "legitimately positioned": "being in a legal and fair position on the field in accordance with the rules.",
                "contested": "refers to a situation where there is disagreement between players regarding a call or ruling.",
                "uncontested": "refers to a situation where there is agreement between players regarding a call or ruling."
     },
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul.", "if a catching foul occurs and is uncontested, the player fouled gains possession at the point of the infraction. If the call is contested, the disc goes back to the thrower."],
     "media": [['contact-catching-1.mp4', ['contact-catching-1-pic-1.jpg', 'contact-catching-1-pic-2.jpg'], 'an example of a contested foul. from the frame-by-frame, we can see that the defender contacts the disc before the offender does; however, the offender claimed to stop rotation of the disc before the defender got to it, thus calling a foul. it was contested, so the disc goes back to the thrower where the foul was initially called.'], ['contact-catching-2.mp4', ['contact-catching-2-pic-1.png', 'contact-catching-2-pic-2.png'], "an example of a defensive foul. the defender chases after the offender and attempts to slap down the disc before it is caught, but instead slaps her left hand with the disc. if uncontested, the play would resume where the disc would've been caught. if contested, the disc would go back to the player who initially threw the disc."]]},
    {
     "id": 3,
     "contact_type": "contact away from the disc",
     "definition": "it is the responsibility of all players to avoid contact in any way possible. violent impact with legitimately positioned opponents constitutes harmful endangerment, a foul, and must be strictly avoided.",
     "terms": {
        "violent impact": "forceful contact between players that poses a risk of injury or harm.",
        "harmful endangerment": "actions or behaviors that put players at risk of injury or harm, including violent impacts."
     },
     "relevant_info": ["if the foul is accepted, the fouled player may make up any positional disadvantage caused by the foul."],
     "media": [['contact-away-1.mp4', ['contact-away-1-pic-1.jpg', 'contact-away-1-pic-2.jpg'], 'both the offender and the defender are running in the same direction, and both are away from the disc. however, when the offender changes direction, this causes the defender to run into them and topple to the ground. since this foul did not affect the play, the disc remains with the player who has it in their possession, but the defender is allowed to get back up and catch up with the person they are defending before the play resumes.'], ['contact-away-2.mp4', ['contact-away-2-pic-1.jpg', 'contact-away-2-pic-2.jpg'], "this is a failed box-out which occurred away from the disc. although the defender is ahead of the offender, the defender shoves the offender with their right arm, and thus initiates non-minor contact with the offender, interfering with the offender's ability to run into their space."]]}
    ]
fouls = [
    {
     "id": 1,
     "foul_type": "offensive",
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul."],
     "media": ['offensive.mp4', ['offensive-1.jpg', 'offensive-2.jpg', 'offensive-3.jpg'], ['offensive-w-1.jpg', 'offensive-w-2.jpg', 'offensive-w-3.jpg']]},
    {
     "id": 2,
     "foul_type": "defensive",
     "relevant_info": ["if a player contacts an opponent before the disc arrives and thereby interferes with that opponent's attempt to make a play on the disc, that player has committed a foul.", "if a player's attempt to make a play on the disc causes significant impact with a legitimately positioned stationary opponent, before or after the disc arrives, that player has committed a foul.", "non-minor contact between the thrower and the marker is considered a foul."],
     "media": ['defensive.mp4', ['defensive-1.jpg', 'defensive-2.jpg', 'defensive-3.jpg'], ['defensive-w-1.jpg', 'defensive-w-2.jpg', 'defensive-w-3.jpg']]},
    {
     "id": 3,
     "foul_type": "dangerous-plays",
     "relevant_info": ["it is the responsibility of all players to avoid contact in any way possible.", "violent impact with legitimately positioned opponents constitutes harmful endangerment, a foul, and must be strictly avoided."],
     "media": ['dangerous-play.mp4', ['dangerous-1.jpg', 'dangerous-2.jpg', 'dangerous-3.jpg'], ['dangerous-w-1.jpg', 'dangerous-w-2.jpg', 'dangerous-w-3.jpg']]} 
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





