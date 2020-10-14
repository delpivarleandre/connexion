from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import pymysql.cursors
import pyodbc

app = Flask(__name__)
CORS(app)


app.config['JWT_SECRET_KEY'] = 'secret'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

id_visiteur = None
def get_mydb():
    mydb = pymysql.connect(
        host="",
        user="",
        passwd="",
        database=""
    )
    return mydb


@app.route('/users/register', methods=['POST'])
def register():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    cur.execute("INSERT INTO users (first_name, last_name, email, password, created) VALUES ('" +
                str(first_name) + "', '" +
                str(last_name) + "', '" +
                str(email) + "', '" +
                str(password) + "', '" +
                str(created) + "')")
    cnxn.commit()

    result = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    }

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    cur.execute("SELECT * FROM Visiteur where login = '" + email + "'")
    rv = cur.fetchall()
    columnsName = [i[0] for i in cur.description]
    tab = [{nameChamp: resultChamp[i]
            for i, nameChamp in enumerate(columnsName)} for resultChamp in rv]
    print(tab)
    for i in tab:
        id_visiteur = i['id']
        nom_visiteur = i['nom']
        prenom_visiteur = i['prenom']
        login_visiteur = i['login']
        mdp_visiteur = i['mdp']
        adresse_visiteur = i['adresse']
        cp_visiteur = str(i['cp'])
        ville_visiteur = i['ville']
        date_embauche_visiteur = i['dateEmbauche']
        daf = str(i['daf'])

        # pas = i['mdp']
        # mail = i['login']
        # first_name = i['nom']
        # last_name = i['prenom']
    # print(bcrypt.check_password_hash(pas, password))
    # if bcrypt.check_password_hash(pas, password):
    #     access_token = create_access_token(identity = {'first_name': first_name,'last_name': last_name,'email': mail})
    #     result = jsonify({"token":access_token})
    if mdp_visiteur == password:
        access_token = create_access_token(
            identity={
            'id':id_visiteur,
            'nom':nom_visiteur,
            'prenom':prenom_visiteur,
            'login':login_visiteur,
            'mdp':mdp_visiteur,
            'adresse':adresse_visiteur,
            'cp':cp_visiteur,
            'ville':ville_visiteur,
            'dateEmbauche':date_embauche_visiteur,
            'daf':daf})
        print(access_token)
        result = jsonify({"token": access_token})
    else:
        result = jsonify({"error": "Invalid username and password"})

    return result


@app.route('/users/etat', methods=['GET'])
def etat():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    cur.execute("SELECT * FROM Etat")
    rv = cur.fetchall()
    columnsName = [i[0] for i in cur.description]
    cnxn.close()
    tab = [{nameChamp: resultChamp[i]
            for i, nameChamp in enumerate(columnsName)} for resultChamp in rv]
    return jsonify(tab)


@app.route('/users/mode_paiement', methods=['GET'])
def mode_paiement():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    cur.execute("SELECT * FROM ModePaiement")
    rv = cur.fetchall()
    columnsName = [i[0] for i in cur.description]
    cnxn.close()
    tab = [{nameChamp: resultChamp[i]
            for i, nameChamp in enumerate(columnsName)} for resultChamp in rv]
    return jsonify(tab)

@app.route('/users/frais_forfait', methods=['GET'])
def frais_forfait():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    cur.execute("SELECT * FROM FraisForfait")
    rv = cur.fetchall()
    columnsName = [i[0] for i in cur.description]
    cnxn.close()
    tab = [{nameChamp: str(resultChamp[i])
            for i, nameChamp in enumerate(columnsName)} for resultChamp in rv]
    return jsonify(tab)


@app.route('/users/ligne_frais_forfait', methods=['GET'])
def test():
    id_visiteur = request.args.get('buttonRadio')
    currentMonth = datetime.now().month
    cnxn = get_mydb()
    cur = cnxn.cursor()
    cur.execute("SELECT * FROM LigneFraisForfait WHERE idVisiteur = '{}' AND mois = 1")
    rv = cur.fetchall()
    columnsName = [i[0] for i in cur.description]
    cnxn.close()
    tab = [{nameChamp: str(resultChamp[i])
            for i, nameChamp in enumerate(columnsName)} for resultChamp in rv]
    return jsonify(tab)


@app.route('/users/update_frais_forfait', methods=['PUT'])
def add_frais_forfait():
    data = request.get_json()
    recipients = data['recipients']
    incident = data['incident']
    for i in 
    cnxn = get_mydb()
    cur = cnxn.cursor()
    cur.execute("""update LigneFraisForfait set LigneFraisForfait.quantite = {quantite}
			where LigneFraisForfait.idVisiteur = '{id_visiteur}' and LigneFraisForfait.mois = '{mois}'
			and LigneFraisForfait.idFraisForfait = '{un_id_frais}'""")
    cnxn.commit()

    return jsonify(1)

@app.route('/users/add_frais_forfait', methods=['POST'])
def add_frais_forfait():
    cnxn = get_mydb()
    cur = cnxn.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    cur.execute("INSERT INTO users (first_name, last_name, email, password, created) VALUES ('" +
                str(first_name) + "', '" +
                str(last_name) + "', '" +
                str(email) + "', '" +
                str(password) + "', '" +
                str(created) + "')")
    cnxn.commit()

    result = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    }
    return jsonify({'result': result})



if __name__ == '__main__':
    app.run(debug=True)
