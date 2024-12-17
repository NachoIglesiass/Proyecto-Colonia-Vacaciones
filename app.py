from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import conexion as conectar
import pymysql
import pandas as pd
from io import BytesIO


app = Flask(__name__)
app.secret_key = "a1B2c3D4e5F6g7H8i9J0!@$%^&*()"
connect = conectar.conectar_bdd()
database = connect[0]
cursor = connect[1]

# Clase Participantes
class Participantes:
    def __init__(self, nombre, apellido, dni, edad, fecha_nacimiento, nombre_padre_tutor, numero_telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
        self.fecha_nacimiento = fecha_nacimiento
        self.nombre_padre_tutor = nombre_padre_tutor
        self.numero_telefono = numero_telefono

    def guardar_en_db(self):
        query = """
               INSERT INTO participantes (nombre, apellido, dni, edad, fecha_nacimiento, nombre_padre_tutor, numero_telefono)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (self.nombre, self.apellido, self.dni, self.edad, self.fecha_nacimiento, self.nombre_padre_tutor, self.numero_telefono)
        
        try:
            cursor.execute(query, valores)
            database.commit()
            return True
        except pymysql.IntegrityError as e:  # Manejo de errores específicos de PyMySQL
            # Verifica si el error es un duplicado
           if e.args[0] == 1062:  # Código de error para duplicados
               flash("Error: El DNI ya está registrado.", "error")
           else:
               flash("Error al guardar en la base de datos.", "error")
           return False
        except Exception as e:  # Captura cualquier otro error no previsto
               flash(f"Ocurrió un error inesperado. El DNI ya esta registrado", "error")
               return False


# Ruta principal para mostrar formulario
@app.route('/')
def index():
    return render_template('index.html')




# Ruta para procesar el formulario
@app.route('/preinscripcion', methods=['POST'])
def preinscripcion():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    edad = request.form['edad']
    fecha_nacimiento = request.form['fecha_nacimiento']
    nombre_padre_tutor = request.form['nombre_padre_tutor']
    numero_telefono = request.form['numero_telefono']
    
    participante = Participantes(nombre, apellido, dni, edad, fecha_nacimiento, nombre_padre_tutor, numero_telefono)
    
    try:
        if participante.guardar_en_db():
            flash("Participante guardado correctamente", "success")
        else:
            flash("Error al guardar participante", "error")
    except KeyError as e:
        flash(f"Falta el campo: {e.args[0]}", "error")
    except Exception as e:
        flash(f"Ocurrió un error inesperado: {e}", "error")
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'german' and password == '39364809':
            session['logged_in'] = True
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('lista_participantes'))
        else:
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')



# Ruta para la lista de participantes
@app.route('/lista_participantes')
def lista_participantes():
    if 'logged_in' in session and session['logged_in']:
        try:
            cursor.execute("SELECT * FROM participantes")
            participantes = cursor.fetchall()
            return render_template('lista_participantes.html', participantes=participantes)
        except Exception as e:
            flash(f"Error al obtener los participantes: {e}", "error")
            return redirect(url_for('index'))
    else:
        flash("Debes iniciar sesión primero", "error")
        return redirect(url_for('login'))



# Ruta para la descarga de la lista de participantes
@app.route('/descargar_participantes')
def descargar_participantes():
    if 'logged_in' in session and session['logged_in']:
        try:
            cursor.execute("SELECT * FROM participantes")
            participantes = cursor.fetchall()

            # Verifica si hay participantes
            if not participantes:
                flash("No hay participantes para descargar.", "info")
                return redirect(url_for('lista_participantes'))

            # Crear un DataFrame de pandas
            df = pd.DataFrame(participantes, columns=['id', 'nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'nombre_padre_tutor', 'numero_telefono', 'fecha_inscripcion'])

            # Crear un objeto BytesIO para guardar el Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Participantes')

                # Obtener el libro y la hoja
                workbook = writer.book
                worksheet = writer.sheets['Participantes']

                # Ajustar el ancho de las columnas
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            output.seek(0)

            # Enviar el archivo Excel como respuesta
            return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='participantes.xlsx')
        except Exception as e:
            flash(f"Error al obtener los participantes: {e}", "error")
            return redirect(url_for('lista_participantes'))
    else:
        flash("Debes iniciar sesión primero", "error")
        return redirect(url_for('login'))


# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
