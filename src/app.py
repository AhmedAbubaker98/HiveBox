from flask import Flask, render_template

app = Flask(__name__)

# Define the software version
SOFTWARE_VERSION = "1.0.0"
#create home page with link to version.html
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/version')
def get_version():
    """
    Endpoint to return the software version in a website UI.
    """
    return render_template('version.html', version=SOFTWARE_VERSION)

if __name__ == '__main__':
    app.run(debug=True)