from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, url_for
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import requests

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'a'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('logIn.html', title='Home')

@app.route('/', methods=['POST'])
def index_post():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = mysql.get_db().cursor()
    cursor.execute("""SELECT email, contrasena FROM Usuarios WHERE email=%s""", email)
    result = cursor.fetchall()
    if len(result) == 0:
        return render_template('logIn.html', title='Usuario desconocido')
    else:
        if result[0].get('contrasena') == password:
            return redirect(url_for('.main', user=email))
        else:
            return render_template('logIn.html', title='Contraseña incorrecta')
    
@app.route('/signUp', methods=['GET'])
def signUp():
    return render_template('signUp.html', title='Home')

@app.route('/signUp', methods=['POST'])
def signUp_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('nombre'), request.form.get('apellidos'), request.form.get('email'),
                 request.form.get('password'))
    sql_insert_query = """INSERT INTO Usuarios (Nombre, Apellidos, email, Contrasena) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/main/<user>', methods=['GET'])
def main(user):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id, Gasto, Tienda, Descripcion, Importe, Moneda, Fecha FROM Gastos WHERE Usuario=%s', user)
    result = cursor.fetchall()
    resultados = []
    for i in result:
        i['Importe'] = requests.get('http://172.26.1.2:9393/convert?amount=' + str(i.get('Importe')) + '&src_currency=' + str(i.get('Moneda')) + '&dest_currency=EUR&reference_date=2023-12-01').json().get('amount')
        i['Moneda'] = 'EUR'
        resultados.append(i)
    return render_template('index.html', title='Home', user=user, gastos=resultados)

@app.route('/main/<user>', methods=['POST'])
def main_post(user):
    monedaDisplay = request.form.get('Moneda')
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Gastos')
    result = cursor.fetchall()
    resultados = []
    for i in result:
        i['Importe'] = requests.get('http://172.26.1.2:9393/convert?amount=' + str(i.get('Importe')) + '&src_currency=' + str(i.get('Moneda')) + '&dest_currency='+ str(monedaDisplay)+'&reference_date=2023-12-01').json().get('amount')
        i['Moneda'] = monedaDisplay
        resultados.append(i)
    return render_template('index.html', title='Home', user=user, gastos=resultados)

@app.route('/view/<int:gasto_id>/<user>', methods=['GET'])
def record_view(gasto_id, user):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Gastos WHERE id=%s', gasto_id)
    result = cursor.fetchall()
    return render_template('view.html', title='Ver Detalles', gasto=result[0], user=user)


@app.route('/edit/<int:gasto_id>/<user>', methods=['GET'])
def form_edit_get(gasto_id,user):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Gastos WHERE id=%s', gasto_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Editar Gasto', gasto=result[0], user=user)


@app.route('/edit/<int:gasto_id>/<user>', methods=['POST'])
def form_update_post(gasto_id, user):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Gasto'), request.form.get('Tienda'), request.form.get('Descripcion'),
                 request.form.get('Importe'), request.form.get('Moneda'), request.form.get('Fecha'), gasto_id)
    sql_update_query = """UPDATE Gastos g SET g.Gasto = %s, g.Tienda = %s, g.Descripcion = %s, g.Importe = 
    %s, g.Moneda = %s, g.Fecha = %s WHERE g.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect(url_for('.main', user=user))

@app.route('/compras/new/<user>', methods=['GET'])
def form_insert_get(user):
    #monedas = requests.get('http://172.26.1.2:9393/convert?amount=10&src_currency=EUR&dest_currency=GBP&reference_date=2023-11-13').json()
    return render_template('new.html', title='Nuevo Gasto', user=user)


@app.route('/compras/new/<user>', methods=['POST'])
def form_insert_post(user):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Gasto'), request.form.get('Tienda'), request.form.get('Descripcion'),
                 request.form.get('Importe'), request.form.get('Moneda'), request.form.get('Fecha'), user)
    sql_insert_query = """INSERT INTO Gastos (Gasto, Tienda, Descripcion, Importe, Moneda, Fecha, Usuario) VALUES (%s, %s,%s, %s,%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect(url_for('.main', user=user))

@app.route('/delete/<int:gasto_id>/<user>', methods=['POST'])
def form_delete_post(gasto_id, user):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM Gastos WHERE id = %s """
    cursor.execute(sql_delete_query, gasto_id)
    mysql.get_db().commit()
    return redirect(url_for('.main', user=user))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
