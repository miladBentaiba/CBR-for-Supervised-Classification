""" this is the main program """
"""from flask import (
    Flask,
    render_template
)

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():"""
"""
This function just responds to the browser ULR
localhost:5000/

:return:        the rendered template 'home.html'
"""
"""return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run()"""


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    txt = input("Type something to test this out: ")
    print("Is this what you just said? ", txt)
    return txt


if __name__ == "__main__":
    app.run()
