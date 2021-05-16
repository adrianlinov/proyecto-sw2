
from flask import Flask, render_template, request, redirect, session, json
from flask import Flask
from database import db, Data, Usuario
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "a"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://epcypyxfdujhmt:f2d2524385174dcec3ee5e41f84c6831998d4ae9c08a7c71a148c8f68208acfb@ec2-35-175-155-248.compute-1.amazonaws.com/d5r8d58gjne92e'
app.debug = True
db.init_app(app)



db = SQLAlchemy(app)



with app.app_context():
    db.create_all()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def indexEndPoint():
    return render_template('index.html')

@app.route('/formulario')
def formularioEndPoint():
    #colocar en el formulario la informacion necesaria

    return render_template('formulario.html')

@app.route('/formularioData')
def formularioDataEndPoint():
    #colocar en el formulario la informacion necesaria
    return render_template('formulario.html')

@app.route('/admin')
def adminLogInEndPoint():
    return render_template('login.html')

@app.route('/analistas')
def analistasEndPoint():
    return render_template('analistas.html')

@app.route('/nosotros')
def nosotrosEndPoint():
    return render_template('nosotros.html')

@app.route('/operaciones_registradas',methods=['GET'])
def operacionesRegistradasEndPoint():
    all_data = Data.query.all()
    for row in all_data: 
        print(row.name)
    return render_template('dashboard.html', Data=all_data)


@app.route('/admin', methods=['POST'])
def submit():
    if request.method == 'POST':
        usuario = request.form['user']
        contrasena = request.form['pwduser']
        user = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasena == contrasena)
        if (user.count() > 0):
            session["userId"] = user[0].id
            return redirect('/operaciones_registradas')
        else:
            return redirect('/admin')
        

#Redirect y RenderTemplate
# TODO: CREAR DASHBOARD DE ADMINISTRADOR
# TODO: HACER QUE LOS USUARIOS SE HAGAN CON LA BASE DE DATOS

if __name__ == '__main__':
    app.debug = True
    app.run()
