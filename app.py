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

@app.route('/registrarse', methods = ['GET', 'POST'])
def registro():
	conexion = sqlite3.connect('uranium.db')
	cursor = conexion.cursor()
	if request.method == 'POST':
		nombre = request.form['nombre']
		usuario = request.form['usuario']
		correo = request.form['correo']
		password = request.form['password']
		confirmacion = request.form['cpass']
		if password == confirmacion:
			verificacion = cursor.execute('SELECT usuario, correo FROM usuarios WHERE usuario = (?) AND correo = (?)', [usuario, correo])
			resultado = verificacion.fetchall()
			if resultado:
				return 'Usuario registrado'
			else:
				cursor.execute('''INSERT INTO usuarios (nombre, usuario, correo, password) VALUES (?,?,?,?)''', (nombre, usuario, correo, password))
				conexion.commit()
				conexion.close()
				os.makedirs('./static/fotos/'+ str(usuario))
				os.makedirs('./static/videos/'+ str(usuario))
				os.makedirs('./static/perfil/'+ str(usuario))
				session['usuario'] = usuario
				return redirect(url_for('perfil'))
		else:
			return 'Las contraseñas no coinciden'

@app.route('/foto', methods = ['GET', 'POST'])
def perfil():
	return render_template('iperfil.html')

@app.route('/cambio', methods = ['GET', 'POST'])
def cambio():
	usuario = session.get('usuario', None)
	app.config['UPLOAD_FOLDER'] = './static/perfil/'+ str(usuario) 
	if request.method == 'POST':
		file = request.files['file']
		if file.filename == '':
			return redirect('/foto')
		conexion = sqlite3.connect('uranium.db')
		cursor = conexion.cursor()
		archivo = secure_filename(file.filename)
		ruta = './static/perfil/'+ str(usuario) +'/'+ archivo
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], archivo))
		cursor.execute('''INSERT INTO perfil (nombre, ruta, usuario) VALUES (?,?,?)''', (archivo, ruta, usuario))
		conexion.commit()
		conexion.close()
		return redirect(url_for('inicio'))

@app.route('/validar', methods = ['GET', 'POST'])
def validar():
	conexion = sqlite3.connect('uranium.db')
	cursor = conexion.cursor()
	if request.method == 'POST':
		usuario = request.form['usuario']
		password = request.form['password']
		verificacion = cursor.execute('SELECT usuario, password FROM usuarios WHERE usuario = (?) AND password = (?) ', [usuario, password])
		resultado = verificacion.fetchall()
		conexion.close()
		if resultado:
			session['usuario'] = usuario
			return redirect(url_for('inicio'))
		else:
			return 'Usuario no registrado'

@app.route('/publicar')
def publicar():
	return render_template('publicar.html')

@app.route('/publicacion', methods = ['GET', 'POST'])
def metodo():
	usuario = session.get('usuario', None)
	archivo = request.files['archivo']
	UPLOAD_FOLDER = 'static/videos/'+ str(usuario) 
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
		ruta = 'static/videos/'+ str(usuario) 
		conexion = sqlite3.connect("uranium.db")
		cursor = conexion.cursor()
		arch = archivo.filename
		filename = secure_filename(archivo.filename)
		archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		cursor.execute('''INSERT INTO publicaciones (usuario, nombre, ruta) VALUES (?,?,?)''', [usuario, arch, ruta])
		conexion.commit()
		conexion.close()
		return redirect('/')	

@app.route('/publicacion2', methods = ['GET', 'POST'])
def metodo2():
	usuario = session.get('usuario', None)
	archivo = request.files['archivo']
	UPLOAD_FOLDER = 'static/fotos/'+ str(usuario) 
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
		tipo = 'foto'
		ruta = 'static/fotos/'+ str(usuario) 
		conexion = sqlite3.connect("uranium.db")
		cursor = conexion.cursor()
		arch = archivo.filename
		filename = secure_filename(archivo.filename)
		archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		cursor.execute('''INSERT INTO imagenes ( nombre, usuario, ruta) VALUES (?,?,?)''', [arch, usuario, ruta])
		conexion.commit()
		conexion.close()
		return redirect('/imagenes')
	
@app.route('/', methods = ['GET', 'POST'])
def inicio():
	usuario = session.get('usuario', None)
	conexion = sqlite3.connect('uranium.db')
	cursor = conexion.cursor()
	sql = cursor.execute('SELECT ruta FROM perfil WHERE usuario = ?', [usuario])
	idented = sql.fetchone()
	fotop = str(idented)[2:-3]
	query = cursor.execute('''SELECT  ID, ruta, nombre FROM publicaciones''')
	rango = query.fetchall()
	query2 = cursor.execute('''SELECT usuario FROM publicaciones''')
	rango2 = query.fetchall()	
	conexion.close()
	user = str(query2)
	return render_template('principal.html', rango = rango[::-1], rango2 = rango2[::-1], usuario = usuario)

@app.route('/imagenes', methods = ['GET', 'POST'])
def imagenes():
	usuario = session.get('usuario', None)
	conexion = sqlite3.connect('uranium.db')
	cursor = conexion.cursor()
	sql = cursor.execute('SELECT ruta FROM perfil WHERE usuario = ?', [usuario])
	idented = sql.fetchone()
	fotop = str(idented)[2:-3]
	query = cursor.execute('''SELECT ruta, nombre FROM imagenes''')
	rango = query.fetchall()
	query2 = cursor.execute('''SELECT usuario FROM imagenes''')
	rango2 = query.fetchall()	
	conexion.close()
	user = str(query2)
	return render_template('imagenes.html', rango = rango[::-1], rango2 = rango2[::-1], usuario = usuario)

@app.route('/<ID>', methods = ['GET', 'POST'])
def casilla(ID):
	usuario = session.get('usuario', None)
	conexion = sqlite3.connect('uranium.db')
	cursor = conexion.cursor()
	consulta = cursor.execute('SELECT ruta, nombre FROM publicaciones WHERE ID = ?', [ID])
	resultado = consulta.fetchall()
	return render_template("publicacion.html", rango = resultado[::-1])

@app.route('/salir', methods = ['GET', 'POST'])
def cerrar():
	session.get('usuario', None)
	session.pop('usuario', None)
	return redirect('/home')

if __name__ == '__main__':
	app.run(debug = True)
