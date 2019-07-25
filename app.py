from flask import Flask, render_template, redirect, request, url_for, session
import sqlite3
import os
import os.path
import time
from werkzeug.utils import secure_filename
clave = os.urandom(32)

app = Flask(__name__)
app.secret_key = clave

@app.route('/home')
def home():
	return render_template('formularios.html')	



if __name__ == '__main__':
	app.run(debug = True)
