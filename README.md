# Virtual Therapy

Virtual Therapy is a web application that provides an interactive chat interface for users to seek assistance with their mental health or therapy-related concerns. The application uses OpenAI's language model to generate responses and engage in conversations with users.

## Features

- User Registration: Users can create an account by providing their username, password, full name, age, email, and date of birth. They can also upload a profile picture during registration.
- User Login: Registered users can access the chat interface and other features.
- Chat Interface: Users can engage in a conversation with the virtual therapist. The application utilizes OpenAI's language model to generate responses based on user input and provide assistance on mental health-related topics.
- Profile Dashboard: Users can view their profile information, including their username, email, age, date of birth, and profile picture.
- Logout: Users can securely log out from their account.

## Technologies Used

- Python
- Flask: A micro web framework used for developing the web application.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python used for database management.
- OpenAI API: An API used for generating responses to user queries.
- HTML/CSS: Markup language and styling used for creating web pages.
- Bootstrap: A CSS framework used for responsive and mobile-first web design.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/virtual-therapy-chatbot.git


2. Navigate to the project directory:

    ```bash
    cd virtual-therapy-chatbot

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt

4. Set up the database:

  - Create a PostgreSQL database and update  the SQLALCHEMY_DATABASE_URI configuration in the app.py 
    file with your database credentials.

   - Run the database migration commands:

        ```bash
        flask db init
        flask db migrate
        flask db upgrade
5. Run the application:

     ```bash
    python app.py

6.  Open your web browser and navigate to http://localhost:5000 to access the Virtual Therapy application.

## Usage

i. Register a new account by providing the required information, including a profile picture if desired.
ii. Login with your credentials.
iii. Engage in a conversation with the virtual therapist by typing your queries or concerns in the chat interface.
iv. Explore the dashboard to view your profile information.
v. Log out when you're done using the application.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the functionality of the Virtual Therapy application, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
