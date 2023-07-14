from flask import Flask, render_template, request, redirect, url_for, session
import openai
import config
import uuid
import os

app = Flask(__name__)

openai.api_key = config.API_KEY
app.secret_key = os.urandom(24)

# Define a dictionary to store user information and preferences
user_info = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3',
    'khaliq': 'khaliq1234'
}
# Define a dictionary to store user registration details
user_info_credentials = {
    'user1': {
        'password': 'password1',
        'age': '25',
        'email': 'user1@example.com',
        'dob': '1996-01-01',
        'full_name': 'John Doe'
    },
    'user2': {
        'password': 'password2',
        'age': '30',
        'email': 'user2@example.com',
        'dob': '1991-05-10',
        'full_name': 'Jane Smith'
    },
    'user3': {
        'password': 'password3',
        'age': '28',
        'email': 'user3@example.com',
        'dob': '1993-09-15',
        'full_name': 'David Johnson'
    }
}
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
    therapist_keywords = ['afraid','therapy','student','stress','name', 'stress', 'tired', 'tire', 'therapist', 'counseling', 'counselling','therapy', 'stress','issue','mental','ill','accident','continue','okay','thank you','name','sick','fire','tramautized','yes', 'tired', 'tire', 'therapist', 'counseling', 'counselling',"anxiety," "depression," "mental health," "well-being," 'help', 'advice', 'support', 'anxious', 'depressed', 'stress', 'cope', 'improve', 'self-care', 'struggling','anxiety', 'self-esteem', 'relationship', 'talk to', 'fears', 'overwhelmed', 'relaxation','scare','sleep', 'grief','work-related stress', 'trauma', 'burnout', 'boundaries', 'lonely', 'work-life balance', 'anger', 'books','resources', 'addiction', 'panic attack', 'mindfulness', 'therapy', 'resilience', 'relaxation apps','positive psychology', 'cognitive skills', 'motivated', 'stress management', 'life transitions', 'self-reflection','mental health conditions', 'support network', 'confidence', 'coping mechanisms', 'self-compassion', 'therapy approaches','social anxiety', 'emotional well-being', 'holistic approaches', 'realistic goals','bad', 'good', 'okay', 'better', 'worst', 'best',"happy", "sad", "angry", "excited", "anxious", "depressed", "frustrated", "calm", "grateful", "content",
        "hopeful", "loved", "lonely", "nervous", "stressed", "bored", "relaxed", "surprised", "disappointed", "jealous",
        "proud", "embarrassed", "confused", "overwhelmed", "energetic","tire","tired", "motivated", "insecure", "guilty",'lost','help','hi','hello',
        "inspired", "fearful", "shocked", "satisfied", "emotional", "safe", "scared", "peaceful", "optimistic", "irritated",
        "joyful", "thankful", "ashamed", "confident", "regretful", "disgusted", "sympathetic", "nostalgic", "hurt",
        "indifferent", "pensive", "amused", "discontent", "envious", "delighted", "exhausted", "miserable", "enthusiastic",
        "shy", "wistful", "lonely", "overjoyed", "courageous", "pessimistic", "agitated", "blissful", "rejected",
        "triumphant", "worried", "peaceful", "annoyed", "fulfilled", "vulnerable", "amazed", "uncomfortable", "suspicious",
        "gloomy", "jubilant", "withdrawn", "carefree", "disappointed", "panicked", "irritable", "serene", "grief-stricken", 'life', 'academic', 'my',
        "indignant", "gleeful", "reserved", "elated", "guarded", "perplexed", "tranquil", "heartbroken", "baffled",'talk', 'money', 'want',
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

        if username in user_info:
            if password == user_info[username]:
                session['username'] = username
                session['full_name'] = user_info_credentials[username]['full_name']
                success_message = "Login successful!"
                return render_template('login_success.html', success_message=success_message)


        error_message = "Invalid username or password. Please try again."
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')


# Define the route for the registration page
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
        
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render_template('register.html', error_message=error_message)
        
        if username in user_info:
            error_message = "Username already exists. Please choose a different username."
            return render_template('register.html', error_message=error_message)
        
        user_info[username] = password
        
        # Add the user's registration details to the login credentials dummy data
        user_info_credentials[username] = {
            'username': username,
            'password': password,
            'age': age,
            'email': email,
            'dob': dob,
            'full_name': full_name
        }
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


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
            return render_template('chat.html', chat_history=chat_history)
        
        chat_history.append('User: ' + user_input)
        
        if user_input.lower() == 'bye':
            bot_reply = "Goodbye! Take care."
            chat_history.append('Bot: ' + bot_reply)
            return redirect(url_for('chat'))
        
        if len(chat_history) == 1:
             # Introduction or greeting
            bot_reply = "Hello, {}! How can I assist you with your mental health or therapy-related concerns?".format(session['full_name'])
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
    # Get the logged-in user's full name from the user_info_credentials dictionary
    username = session['username']
    full_name = user_info_credentials.get(username, {}).get('full_name', '')
    return render_template('chat.html', chat_history=chat_history,full_name=full_name)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
