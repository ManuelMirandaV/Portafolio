import bcrypt
from flask import Flask, flash, render_template
from flask_mysqldb import MySQL
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import request, session, flash, redirect, url_for, render_template
from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.secret_key = 'secreto_seguro'  
USUARIOS = {'admin': '1234', 'usuario': 'contrasena'}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portafolio'

mysql = MySQL(app)

def obtener_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/lenguages')
def lenguages():
    return render_template('lenguages.html')

@app.route('/project1')
def project1():
    return render_template('project1.html')

@app.route('/project2')
def project2():
    return render_template('project2.html')

@app.route('/project3')
def project3():
    return render_template('project3.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')  
        contrasena = request.form.get('contrasena')  

        if not correo or not contrasena:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, usuario, correo, contrasena FROM usuarios WHERE correo = %s", (correo,))
        usuario = cur.fetchone()
        cur.close()

        if usuario:
            stored_hash = usuario[3]  
            if check_password_hash(stored_hash, contrasena): 
                session['user_id'] = usuario[0]
                session['username'] = usuario[1] 
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('index'))

        flash("Correo o contraseña incorrectos", "danger")

    return render_template('loginpage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        if not usuario or not nombre or not correo or not contrasena:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE correo = %s OR usuario = %s", (correo, usuario))
        usuario_existente = cur.fetchone()

        if usuario_existente:
            flash("El correo o el usuario ya están registrados", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(contrasena)

        cur.execute("INSERT INTO usuarios (usuario, nombre, correo, contrasena) VALUES (%s, %s, %s, %s)",
                    (usuario, nombre, correo, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash("Usuario registrado con éxito, ahora puedes iniciar sesión", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

hashed_password = generate_password_hash("miclave")

if check_password_hash(hashed_password, "miclave"):
    print("¡La contraseña es correcta!")
else:
    print("Contraseña incorrecta.")
    
    
    
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  
EMAIL_PREDETERMINADO = "pmanuelmirandau@gmail.com" 
EMAIL_PASSWORD = "lgqb nbsu zavs vmye"  

@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email_remitente = request.form['email']  
        mensaje = request.form['mensaje']

        if not email_remitente or not mensaje:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for('email'))  

        try:
        
            msg = MIMEMultipart()
            msg['From'] = email_remitente 
            msg['To'] = EMAIL_PREDETERMINADO
            msg['Subject'] = "Nuevo mensaje de contacto"
            
            cuerpo = f"Has recibido un mensaje de {email_remitente}:\n\n{mensaje}"
            msg.attach(MIMEText(cuerpo, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  
            server.login(EMAIL_PREDETERMINADO, EMAIL_PASSWORD)  
            server.sendmail(email_remitente, EMAIL_PREDETERMINADO, msg.as_string())
            server.quit()

            flash("Correo enviado exitosamente", "success")
        except Exception as e:
            flash(f"Error al enviar el correo: {str(e)}", "error")

        return redirect(url_for('email'))  

    return render_template('email.html')  

if __name__ == '__main__':
    app.run(debug=True)
