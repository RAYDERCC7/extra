from flask import Flask, render_template, request, redirect, url_for
from models import db, Usuario

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_secreta'  # Necesaria para los formularios de Flask-WTF

# Inicializar la base de datos
db.init_app(app)

# Crear las tablas al iniciar la aplicación
with app.app_context():
    db.create_all()

# Ruta inicial
@app.route('/')
def index():
    return redirect(url_for('listar_usuarios'))

# Ruta para listar usuarios
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()  # Obtener todos los usuarios
    return render_template('index.html', usuarios=usuarios)

# Ruta para crear un nuevo usuario
@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        edad = int(request.form['edad'])
        telefono = request.form['telefono']
        
        # Crear un nuevo usuario
        nuevo = Usuario(nombre=nombre, edad=edad, telefono=telefono)
        db.session.add(nuevo)
        db.session.commit()
        
        return redirect(url_for('listar_usuarios'))
    
    # Mostrar el formulario si es GET
    return render_template('form.html')
@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)  # Obtener el usuario por ID
    if request.method == 'POST':
        # Actualizar los datos del usuario
        usuario.nombre = request.form['nombre']
        usuario.edad = int(request.form['edad'])
        usuario.telefono = request.form['telefono']
        
        db.session.commit()  # Guardar los cambios en la base de datos
        return redirect(url_for('listar_usuarios'))  # Redirigir al listado de usuarios
    
    return render_template('form.html', usuario=usuario)
@app.route('/usuarios/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)  # Obtener el usuario por ID
    db.session.delete(usuario)  # Eliminar el usuario
    db.session.commit()  # Guardar los cambios en la base de datos
    return redirect(url_for('listar_usuarios'))  # Redirigir al listado de usuarios


if __name__ == '__main__':
    app.run(debug=True)

