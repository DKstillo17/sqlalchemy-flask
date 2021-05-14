from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Realizado por Daniel Castillo & Nefer Blanchar

app = Flask(__name__)

#Configuracion a Mysql
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskdb' #Direccion de la BD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Definiendo que vamos a guardar en la BD
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(70))
    nombre = db.Column(db.String(70))
    email = db.Column(db.String(70), unique=True)
    admin = db.Column(db.String(1))
  #Definimos un constructor para recibir y asignar datos
    def __init__(self, username, password, nombre, email, admin):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.email = email
        self.admin = admin

#Definiendo que vamos a guardar en la BD
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreCat = db.Column(db.String(70), unique=True)
#Definimos un constructor para recibir y asignar datos
    def __init__(self, nombreCat):
        self.nombreCat = nombreCat

#Definiendo que vamos a guardar en la BD
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreArt = db.Column(db.String(70), unique=True)
    precio = db.Column(db.Integer)
    iva = db.Column(db.Integer)
    descripcion = db.Column(db.String(70))
    image = db.Column(db.String(70))
    stock = db.Column(db.Integer)
    id_Categories = db.Column(db.Integer)

    def __init__(self, nombreArt, precio, iva, descripcion, image, stock, id_Categories):
        self.nombreArt = nombreArt
        self.precio = precio
        self.iva = iva
        self.descripcion = descripcion 
        self.image = image 
        self.stock = stock 
        self.id_Categories = id_Categories

#Crea todas las tablas de todas las clases
db.create_all()

#Usuarios
#Que datos vamos a utilizar creando un esquema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'nombre', 'email', 'admin')


user_schema = UserSchema() #Instancia para interactuar con un dato
users_schema = UserSchema(many=True) #Instancia para interactuar con muchos datos

#Asignamos una ruta para luego guardarlos por POST (endspoints)
@app.route('/users', methods=['POST'])
def create_user():

   #print(request.json)
   #return 'recibido'

#Recibimos los datos a traves del request
  username = request.json['username']
  password = request.json['password']
  nombre = request.json['nombre']
  email = request.json['email']
  admin = request.json['admin']

#Creamos un esquema de lo que se va a guardar
  new_user = User(username, password, nombre, email, admin)

#La guardamos en la BD
  db.session.add(new_user)
  db.session.commit()

#Al finalizar nos mostrará los datos guardados
  return user_schema.jsonify(new_user)

#Se asigna una ruta y luego se hace un llamado GET para traer todos los datos guardados
@app.route('/users', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

#Final Usuarios

#Categories
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombreCat')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@app.route('/categories', methods=['POST'])
def create_category():

  nombreCat = request.json['nombreCat']
 
  new_category = Category(nombreCat)

  db.session.add(new_category)
  db.session.commit()

  return category_schema.jsonify(new_category)

@app.route('/categories', methods=['GET'])
def get_categories():
  all_categories = Category.query.all()
  result = categories_schema.dump(all_categories)
  return jsonify(result)

  #Final Categorias
#Articulos
class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombreArt', 'precio', 'iva', 'descripcion', 'image', 'stock', 'id_Categories')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

@app.route('/articles', methods=['POST'])
def create_article():

  nombreArt = request.json['nombreArt']
  precio = request.json['precio']
  iva = request.json['iva']
  descripcion = request.json['descripcion']
  image = request.json['image']
  stock = request.json['stock']
  id_Categories = request.json['id_Categories']

  new_article = Article(nombreArt, precio, iva, descripcion, image, stock, id_Categories)

  db.session.add(new_article)
  db.session.commit()

  return article_schema.jsonify(new_article)

@app.route('/articles', methods=['GET'])
def get_articles():
  all_articles = Article.query.all()
  result = articles_schema.dump(all_articles)
  return jsonify(result)

#Final articulos

if __name__ == "__main__":
    app.run(debug=True)
  

