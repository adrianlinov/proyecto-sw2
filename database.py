from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#TODO: HACER LA VALIDACION DE LOS USARIOS CON SU RESPECTIVO CARGO
#TODO: CAMPOS DIFERENTES POR CADA SERVICIO
#TODO: QUE SE MUESTREN LOS CLIENTES REGISTRADOS EN LA BANDEJA DE ADMINISTRACION



class Valor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campo_id = db.Column(db.Integer, db.ForeignKey('campo.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    valor = db.Column(db.Text)



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(100))
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargo.id"))
    cliente = db.relationship('Cliente', cascade="all,delete", backref="usuario")


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}


class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    usuario = db.relationship('Usuario', cascade="all,delete", backref="cargo")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}
    

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    descripcion = db.Column(db.Text)
    imagenURL = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    campo = db.relationship('Campo', cascade="all,delete", backref="servicio")
    cliente = db.relationship('Cliente', cascade="all,delete", backref="servicio")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}

       
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    servicio = db.relationship('Servicio', cascade="all,delete", backref="categoria")


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    esEmpresa = db.Column(db.String(10))
    razonSocial = db.Column(db.String(100))
    documento = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    rubro_id = db.Column(db.Integer, db.ForeignKey("rubro.id"))
    ocupacion_id = db.Column(db.Integer, db.ForeignKey("ocupacion.id"))
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicio.id"))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    valor = db.relationship('Valor', cascade="all,delete", backref="Cliente")
    analisis = db.Column(db.Text)
    direccion = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    distrito = db.Column(db.String(100))
    codigoPostal = db.Column(db.String(10))


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}

class Campo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    tipo = db.Column(db.String(100))
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicio.id"))
    valor = db.relationship('Valor', cascade="all,delete", backref="Campo")
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self._table_.columns}

class Ocupacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    cliente = db.relationship('Cliente', cascade="all,delete", backref="Ocupacion")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.columns}

class Rubro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rubro = db.Column(db.String(100), unique=True)
    cliente = db.relationship('Cliente', cascade="all,delete", backref="Rubro")
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.columns}

class Clientescomite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idAnalista = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    idCliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.columns}

class EstadoSol(db.Model): 
    id = db.Column(db.Integer, primary_key=True)    
    idComite = db.Column(db.Integer, db.ForeignKey("clientescomite.id"))
    Usuario = db.Column(db.String(100))
    idUsuario = db.Column(db.Integer)
    estado = db.Column(db.String(100))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.columns}

