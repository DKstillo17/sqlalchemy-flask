from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Clase Usuarios & Modelo de la BD
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(70))
    nombre = db.Column(db.String(70))
    email = db.Column(db.String(70), unique=True)
    admin = db.Column(db.String(1))

    def __init__(self, username, password, nombre, email, admin):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.email = email
        self.admin = admin

#Clase Categorias & Modelo de la BD
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreCat = db.Column(db.String(70), unique=True)

    def __init__(self, nombreCat):
        self.nombreCat = nombreCat

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

#Crea todas las tablas
db.create_all()

#Usuarios
#Que datos vamos a utilizar
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'nombre', 'email', 'admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Asignamos una ruta para luego guardarlos por POST
@app.route('/users', methods=['POST'])
def create_user():

   #print(request.json)
   #return 'recibido'

#Decimos que almacene los datos en JSON
  username = request.json['username']
  password = request.json['password']
  nombre = request.json['nombre']
  email = request.json['email']
  admin = request.json['admin']

  new_user = User(username, password, nombre, email, admin)

  db.session.add(new_user)
  db.session.commit()

#Se guardan los datos en la BD
  return user_schema.jsonify(new_user)


#Se asigna una ruta y luego se hace un llamado GET para traer todos los datos guardados
@app.route('/users', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

#Final Usuarios

#Categorias
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombreCat')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@app.route('/categories', methods=['POST'])
def create_category():

   #print(request.json)
   #return 'recibido'

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
#Que datos vamos a utilizar
class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombreArt', 'precio', 'iva', 'descripcion', 'image', 'stock', 'id_Categories')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

#Asignamos una ruta para luego guardarlos por POST
@app.route('/articles', methods=['POST'])
def create_article():

   #print(request.json)
   #return 'recibido'

#Decimos que almacene los datos en JSON
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

#Se guardan los datos en la BD
  return article_schema.jsonify(new_article)


#Se asigna una ruta y luego se hace un llamado GET para traer todos los datos guardados
@app.route('/articles', methods=['GET'])
def get_articles():
  all_articles = Article.query.all()
  result = articles_schema.dump(all_articles)
  return jsonify(result)

#Final Usuarios




if __name__ == "__main__":
    app.run(debug=True)
  

