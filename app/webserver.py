import app.config as config
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')


if __name__ == '__main__':

    mode = 'development'

    if mode == 'development':
        app.config.from_object(config.Development)
        app.run()
    elif mode == 'production':
        app.config.from_object(config.Production)
        app.run()
