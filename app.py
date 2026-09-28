from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    timestamp = datetime.now().strftime('%B %d, %Y')
    return render_template('index.html', name='Kovid', timestamp=timestamp)

if __name__ == '__main__':
    app.run(debug=True)   