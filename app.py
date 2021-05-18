from flask import Flask, render_template, request, redirect, session, json
from flask import Flask
from database import db, Cliente, Usuario, Valor, Cargo, Categoria, Campo, Servicio
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "a"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://epcypyxfdujhmt:f2d2524385174dcec3ee5e41f84c6831998d4ae9c08a7c71a148c8f68208acfb@ec2-35-175-155-248.compute-1.amazonaws.com/d5r8d58gjne92e'
app.debug = True
db.init_app(app)

with app.app_context():
    db.create_all()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def indexEndPoint():
    categorias = Categoria.query.all()
    return render_template('index.html', categorias=categorias)


@app.route('/formulario')
def formularioEndPoint():
    all_data = Servicio.query.all()

    return render_template('formulario.html', Servicio=all_data)

@app.route('/editar_servicios', methods=['GET'])
def editarServiciosEndPoint():
    all_data = Servicio.query.all()
    all_categorias = Categoria.query.all()
    return render_template('editarServicios.html', servicios=all_data, categorias=all_categorias)

@app.route('/editar_servicio', methods=['POST', "GET"])
def editarServicioEndPoint():
    nombre = request.form["Nombre"]
    descripcion = request.form["Descripcion"]
    categoria_id = request.form["Categoria"]
    servicio_id = request.form["Servicio_id"]
    
    servicio = db.session.query(Servicio).filter(Servicio.id == servicio_id)[0]
    servicio.nombre = nombre
    servicio.descripcion = descripcion
    servicio.categoria_id = categoria_id
    
    db.session.add(servicio)
    db.session.commit()

    
    return redirect('/editar_servicios')

@app.route('/nuevo_servicio', methods=['POST', 'GET'])
def nuevoServicioEndPoint():
    nombre = request.form["Nombre"]
    descripcion = request.form["Descripcion"]
    categoria_id = request.form["Categoria"]
    nuevoServicio = Servicio(nombre=nombre, descripcion=descripcion, categoria_id=categoria_id)
    db.session.add(nuevoServicio)
    db.session.commit()
    return redirect('/editar_servicios')


@app.route('/nueva_categoria', methods=['POST', 'GET'])
def nuevaCategoriaEndPoint():
    nombre = request.form["Nombre"]
    categoria = Categoria(nombre=nombre)
    db.session.add(categoria)
    db.session.commit()
    return redirect('/editar_servicios')

@app.route('/formulario', methods=['POST'])
def formularioPost():

    all_data = Servicio.query.all()
    print(all_data)

    nombre = request.form['Nombre']
    apellido = request.form['Apellido']
    correo = request.form['Correo']
    empresa = request.form['EsEmpresa']
    telefono = request.form['Telefono']
    servicio_id = request.form['servicio_cliente']
    #servicio_id = request.form['servicio_id']
    #colocar en el formulario la informacion necesaria
    if request.form["EsEmpresa"] == "false":
        documento = request.form['DNI']
        nuevo = Cliente(nombre=nombre,
                        correo=correo,
                        apellido=apellido,
                        empresa=empresa,
                        documento=documento,
                        telefono=telefono,
                        servicio_id=servicio_id)
    else:
        documento = request.form['RUC']
        nuevo = Cliente(nombre=nombre,
                        correo=correo,
                        apellido=apellido,
                        empresa=empresa,
                        documento=documento,
                        telefono=telefono,
                        servicio_id=servicio_id)
    db.session.add(nuevo)
    db.session.commit()

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


@app.route('/operaciones_registradas', methods=['GET'])
def operacionesRegistradasEndPoint():
    all_data = Cliente.query.all()
    print(all_data)
    for row in all_data:
        print(row.servicio)

    all_data_usuario = db.session.query(Usuario).filter(Usuario.cargo_id == 1)      
    print(all_data_usuario)
    return render_template('dashboard.html', Cliente=all_data, Usuario = all_data_usuario)

    #RESULTADO = db.session.query(Usuario).filter(Usuario.cargo_id == 1)


@app.route('/admin', methods=['POST'])
def submit():
    if request.method == 'POST':
        usuario = request.form['user']
        contrasena = request.form['pwduser']
        user = db.session.query(Usuario).filter(
            Usuario.usuario == usuario, Usuario.contrasena == contrasena)
        if (user.count() > 0):
            session["userId"] = user[0].id
            return redirect('/operaciones_registradas')
        else:
            return redirect('/admin')

@app.route('/Asignar_Analista', methods=['POST', 'GET'])
def Asignar_Analista():
    Id_Usuario = request.form['Id_Usuario']
    Id_Cliente = request.form['Id_Cliente']
    print('Id_Usuario')
    print('Id_Cliente')
    #servicio_id = request.form["Servicio_id"]
    
    cliente = db.session.query(Cliente).filter(Cliente.id == Id_Cliente)[0]
    cliente.usuario_id = Id_Usuario
    
    db.session.add(cliente)
    db.session.commit()
    return redirect('/operaciones_registradas')


#Redirect y RenderTemplate
# TODO: CREAR DASHBOARD DE ADMINISTRADOR
# TODO: HACER QUE LOS USUARIOS SE HAGAN CON LA BASE DE DATOS

if __name__ == '__main__':
    app.debug = True
    app.run()




# @app.route("/login", methods=['POST'])
# def verificarLogin():
#     if request.method == "POST":
#         email = request.form["username"]
#         password = request.form["password"]
#         print(email)
#         print(password)
#         user = db.session.query(User).filter(User.email == email, User.password == password)
#         if user.count() > 0:
#             session["userId"] = user[0].id
#             return redirect("dashboard")
#         else:
#             nuevo = User(email=email, password=password)
#             db.session.add(nuevo)
#             db.session.commit()
#             return render_template("login.html", error=True)  


# @app.route("/logout", methods=['GET'])
# def logOut():
#     session.pop("userId", None)
#     return redirect("/")



# @app.route("/dashboard")
# def dashboard():
#     if "userId" in session:
#         user = db.session.query(User).filter(User.id == session["userId"])[0]
#         grupos = db.session.query(RegisterGroup).filter(RegisterGroup.user_id == session["userId"])

#         for grupo in grupos:
#             grupo.count = db.session.query(Register).filter(Register.registerGroup == grupo).count()
#             print(grupo.count)
#         return render_template("dashboard.html", grupos=grupos)

#     else:
#         return redirect(url_for("login"))
