from flask import Flask, render_template

app = Flask(__name__)

# Define the software version
SOFTWARE_VERSION = "1.0.0"
#home page
@app.route('/')
def home():
    return render_template('home.html')
#version page
@app.route('/version')
def get_version():
    """
    Endpoint to return the software version in a website UI.
    """
    return render_template('version.html', version=SOFTWARE_VERSION)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
