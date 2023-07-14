from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import openai
import config
import uuid
from hashlib import md5
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

openai.api_key = config.API_KEY
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0gazb0iz@localhost:5432/chatdatabase'
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'  # Folder to store profile pictures
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions for profile pictures

db = SQLAlchemy(app)
migrate= Migrate(app,db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    dob = db.Column(db.Date)
    full_name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))  # Column for storing the profile picture filename


# Define a function to check if a user exists in the database
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    return user is not None


# Define a dictionary to store session information
session_info = {}

# Define a list to store the chat messages
chat_history = []

# Define a function to send a message to the chatbot
def send_message(session_id, message):
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=message,
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None,
            timeout=30
        )
        reply = response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        reply = "Sorry, I encountered an error. Please try again later."
    return reply

def is_therapist_query(input_text):
    therapist_keywords = ['therapy', 'stress', 'tired', 'tire', 'therapist', 'counseling', 'counselling','therapy', 'stress','issue','mental','ill','accident','continue','okay','thank you','name','sick','fire','tramautized','yes', 'tired', 'tire', 'therapist', 'counseling', 'counselling',"anxiety," "depression," "mental health," "well-being," 'help', 'advice', 'support', 'anxious', 'depressed', 'stress', 'cope', 'improve', 'self-care', 'struggling','anxiety', 'self-esteem', 'relationship', 'talk to', 'fears', 'overwhelmed', 'relaxation', 'sleep', 'grief','work-related stress', 'trauma', 'burnout', 'boundaries', 'lonely', 'work-life balance', 'anger', 'books','resources', 'addiction', 'panic attack', 'mindfulness', 'therapy', 'resilience', 'relaxation apps','positive psychology', 'cognitive skills', 'motivated', 'stress management', 'life transitions', 'self-reflection','mental health conditions', 'support network', 'confidence', 'coping mechanisms', 'self-compassion', 'therapy approaches','social anxiety', 'emotional well-being', 'holistic approaches', 'realistic goals','bad', 'good', 'okay', 'better', 'worst', 'best',"happy", "sad", "angry", "excited", "anxious", "depressed", "frustrated", "calm", "grateful", "content",
        "hopeful", "loved", "lonely", "nervous", "stressed", "bored", "relaxed", "surprised", "disappointed", "jealous",
        "proud", "embarrassed", "confused", "overwhelmed", "energetic","tire","tired", "motivated", "insecure", "guilty",
        "inspired", "fearful", "shocked", "satisfied", "emotional", "safe", "scared", "peaceful", "optimistic", "irritated",
        "joyful", "thankful", "ashamed", "confident", "regretful", "disgusted", "sympathetic", "nostalgic", "hurt",
        "indifferent", "pensive", "amused", "discontent", "envious", "delighted", "exhausted", "miserable", "enthusiastic",
        "shy", "wistful", "lonely", "overjoyed", "courageous", "pessimistic", "agitated", "blissful", "rejected",
        "triumphant", "worried", "peaceful", "annoyed", "fulfilled", "vulnerable", "amazed", "uncomfortable", "suspicious",
        "gloomy", "jubilant", "withdrawn", "carefree", "disappointed", "panicked", "irritable", "serene", "grief-stricken",
        "indignant", "gleeful", "reserved", "elated", "guarded", "perplexed", "tranquil", "heartbroken", "baffled",
        "humbled", "refreshed", "enraged", "exhilarated", "bewildered", "rejuvenated", "humiliated", "aggravated", "no", "maybe", "I don't know", "possibly", "definitely", "absolutely", "certainly", "surely", "of course",
    "without a doubt", "never", "always", "sometimes", "rarely", "frequently", "occasionally", "perhaps", "it depends",
    "I guess", "I suppose", "not really", "not sure", "not necessarily", "not likely", "not possible", "not at all",
    "not anymore", "not yet", "not quite", "not really sure", "not exactly", "not entirely", "not completely",
    "not necessarily", "not always", "not often", "not usually", "not specifically", "not particularly",
    "not particularly interested", "not really concerned", "not a problem", "not a big deal", "not my thing",
    "not my concern", "not my focus", "not my priority", "not my style", "not my intention", "not my preference",
    "not my area of expertise", "not my cup of tea", "not my responsibility", "not my fault", "not my decision",
    "not my mistake", "not my choice", "not my problem", "not my issue", "not my place", "not my business",
    "not my duty", "not my obligation",'what', "not my responsibility"]
    for keyword in therapist_keywords:
        if keyword in input_text.lower():
            return True
    return False

# Define the route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('chat'))

        error_message = "Invalid username or password. Please try again."
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        age = request.form['age']
        email = request.form['email']
        dob = request.form['dob']
        full_name = request.form['full_name']
        profile_pic = None
        
        # Check if a profile picture file was uploaded
        if 'profile_pic' in request.files:
            profile_pic_file = request.files['profile_pic']
            if profile_pic_file.filename != '':
                # Generate a unique filename using the username
                filename = username + '.' + profile_pic_file.filename.rsplit('.', 1)[1].lower()
                profile_pic = filename

                # Save the profile picture file to the upload folder
                profile_pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render_template('register.html', error_message=error_message)

        if user_exists(username):
            error_message = "Username already exists. Please choose a different username."
            return render_template('register.html', error_message=error_message)

        user = User(username=username, password=password, age=age, email=email, dob=dob, full_name=full_name, profile_pic=profile_pic)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()

    if not user:
        # Handle the case if the user is not found in the database
        return redirect(url_for('login'))

    email = user.email
    age = user.age
    dob = user.dob
    full_name = user.full_name
    profile_pic = user.profile_pic  # Retrieve the profile picture filename

    return render_template('dashboard.html', full_name=full_name, username=username, profile_pic=profile_pic, email=email, age=age, dob=dob)

# Define the route for the chat page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session_id = request.cookies.get('session_id')
        if session_id is None:
            session_id = str(uuid.uuid4())
            session_info[session_id] = {}
        user_input = request.form['user_input']
        
        if user_input.strip() == "":
            return render_template('chat.html', chat_history=chat_history, username=session['username'])
        
        chat_history.append('User: ' + user_input)
        
        if user_input.lower() == 'bye':
            bot_reply = "Goodbye! Take care."
            chat_history.append('Bot: ' + bot_reply)
            return redirect(url_for('chat'))
        
        if len(chat_history) == 1:
            # Introduction or greeting
            bot_reply = "Hello! How can I assist you with your mental health or therapy-related concerns?"
            chat_history.append('Bot: ' + bot_reply)
        else:
            prompt = '\n'.join(chat_history)
            
            if not is_therapist_query(user_input):
                bot_reply = "I'm sorry, but I can only provide assistance with mental health-related topics or therapy-related inquiries."
                chat_history.append('Bot: ' + bot_reply)
            else:
                if 'pronouns' in session_info[session_id]:
                    prompt += '\nUser Pronouns: ' + session_info[session_id]['pronouns']
                if 'focus_area' in session_info[session_id]:
                    prompt += '\nFocus Area: ' + session_info[session_id]['focus_area']
                
                prompt = 'User: ' + user_input + '\nTherapist Bot:\n' + prompt
                bot_reply = send_message(session_id, prompt)
                chat_history.append('Bot: ' + bot_reply)

               
        return redirect(url_for('chat'))
    
    username = session['username']
    profile_pic = url_for('static', filename='profile_pics/' + username + '.png')
        
    
    return render_template('chat.html', chat_history=chat_history, username=username, profile_pic=profile_pic)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
