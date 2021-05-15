from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#TODO: HACER LA VALIDACION DE LOS USARIOS CON SU RESPECTIVO CARGO
#TODO: CAMPOS DIFERENTES POR CADA SERVICIO
#TODO: QUE SE MUESTREN LOS CLIENTES REGISTRADOS EN LA BANDEJA DE ADMINISTRACION

class Data(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name =  db.Column(db.String(100))
    apellido =  db.Column(db.String(100))
    dni = db.Column(db.String(100))
    servicio = db.Column(db.String(100))


campo_cliente = db.Table('campo_cliente',
                db.Column('campo_id', db.Integer, db.ForeignKey('campo.id')),
                db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id')))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(100))
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargo.id"))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}


class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    usuario = db.relationship('Usuario', cascade="all,delete", backref="cargo")
    

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    descripcion = db.Column(db.Text)
    imagenURL = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    campo = db.relationship('Campo', cascade="all,delete", backref="servicio")


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    servicio = db.relationship('Servicio', cascade="all,delete", backref="categoria")

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    emmpresa = db.Column(db.Boolean)
    documento = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(15), unique=True)

class Campo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    tipo = db.Column(db.String(100))
    placeholder = db.Column(db.String(100))
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicio.id"))
    cliente = db.relationship('Cliente', secondary=campo_cliente, backref=db.backref('cliente', lazy= 'dynamic'))
        
# class User(db.Model): 1
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100), unique=True)
#     registerGroup = db.relationship('RegisterGroup', cascade="all,delete", backref="user")
#     template = db.relationship('Template', cascade="all,delete", backref='user')

#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class RegisterGroup(db.Model): muchos
#     __tablename__ = "registergroup"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     name = db.Column(db.String(100), unique=True)
#     variable = db.relationship('Variable', cascade="all,delete", backref='registerGroup')
#     register = db.relationship('Register', cascade="all,delete", backref='registerGroup')


#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class Variable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     registerGroup_id = db.Column(db.Integer, db.ForeignKey("registergroup.id"))
#     name = db.Column(db.String(100))
#     value = db.relationship('Value', cascade="all,delete", backref='variable')


#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class Value(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     variable_id = db.Column(db.Integer, db.ForeignKey("variable.id"))
#     register_id = db.Column(db.Integer, db.ForeignKey("register.id"))
#     value = db.Column(db.String(100))


#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class Register(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100))
#     value = db.relationship('Value', cascade="all,delete", backref='register')
#     registerGroup_id = db.Column(db.Integer, db.ForeignKey("registergroup.id"))


#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# class Template(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     description = db.Column(db.String(500))
#     text = db.Column(db.Text)

#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
