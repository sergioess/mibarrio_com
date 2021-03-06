from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for
# TODO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2


from routes.user_bp import user_bp
from routes.empleado_bp import empleado_bp
from routes.clasificacion_bp import clasificacion_bp
from routes.entrada_bp import entrada_bp
from routes.producto_bp import producto_bp
from routes.salida_bp import salida_bp
# from flask_mongoalchemy import MongoAlchemy

from flask import send_from_directory



# users=[]
# users.append(User(id=1, username='Sergio', password='password'))
# users.append(User(id=2, username='Andres', password='password'))

# print(users)

app = Flask(__name__)

app.config.from_object('config')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678g@localhost:5432/mitienda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oxwttxarfidlxi:89e47cacfc5926776ab52a7e485b08a91bf9632736ca0843d80b6356b506f3f2@ec2-3-231-69-204.compute-1.amazonaws.com:5432/d3hr8qndm4p50h'
db = SQLAlchemy(app)

# TODO
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    # id_usuario = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=True)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id_usuario, nombre_usuario, password):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.password = password

    def __repr__(self):
        return f'<User: {self.nombre_usuario}>'

@login_manager.user_loader
def load_user(id_usuario):
    return User.query.get(int(id_usuario))
    

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(empleado_bp, url_prefix='/empleados')
app.register_blueprint(clasificacion_bp, url_prefix='/clasificacion')
app.register_blueprint(entrada_bp, url_prefix='/entrada')
app.register_blueprint(producto_bp, url_prefix='/producto')
app.register_blueprint(salida_bp, url_prefix='/salida')


@app.route('/')
def index():

    return render_template('index.html')

# TODO
@app.route('/login')
def login():
    user = User.query.filter_by(nombre_usuario='joselin').first()
    print(user)
    login_user(user)
    return render_template('index.html') 
    return 'You are now logged in!'  

# TODO
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html') 
    return 'You are now logged out!'       

@app.route('/perfil')
def perfil():
    return render_template('profile.html')    

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    # print(app.config['CARPETA'])
    return send_from_directory(app.config['CARPETA'], nombreFoto)


@app.route('/uplproductos/<nombreFoto>')
def uplproductos(nombreFoto):
    # print(app.config['CARPETA'])
    return send_from_directory(app.config['CARPETA_PTOS'], nombreFoto)


if __name__ == '__main__':
    app.run(debug=True)
