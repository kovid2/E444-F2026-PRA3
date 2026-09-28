from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '_WEHQWFIBFHABDSHUFBWASDBWHURJ_DANFSEJDNDBS___1U2893490Q210'
bootstrap = Bootstrap5(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        email = form.email.data or ''
        if 'utoronto' not in email.lower():
            flash('Please fill in a UofT email address.')
        else:
            # Store name and email directly in Flask session
            session['name'] = form.name.data
            session['email'] = email
            return redirect(url_for('chat_page'))
            
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email'),
        title="Hello! Welcome to PRA3 Docker!"
    )


@app.route('/chat_page', methods=['GET'])
def chat_page():
    if not session.get('name') or not session.get('email'):
        flash('Please enter your name and UofT email first.')
        return redirect(url_for('index'))
    return render_template('chat.html', name=session.get('name'))


@app.route("/chat", methods=["POST"])
def chat():
    # Handle JSON inputs safely
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if "my dog's name is" in message.lower():
        extracted_name = message.lower().split("my dog's name is")[-1].strip().strip('.!').capitalize()
        session['bot_remembered_name'] = extracted_name  # Direct session assignment
        reply = f"Your dog name is, {extracted_name}!"

    # 2. User asks chatbot to recall their name (e.g. "What is my name?")
    elif "what is my dog's name" in message.lower():
        remembered = session.get('bot_remembered_name')
        if remembered:
            reply = f"Your dog name is {remembered}."
        else:
            reply = f"I don't know your dog name yet!"

    else:
        reply = "I don't understand."

    return jsonify({"reply": reply})


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    flash('You have been logged out and remembered information cleared.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)