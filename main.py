from flask import Flask, render_template, flash
from flaskext.mysql import MySQL
from flask import request
import hashlib
from helpers.password import check_password, hash_password

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'atk0k0kk00'
app.config['MYSQL_DATABASE_DB']='dtbank'
mysql = MySQL()
mysql.init_app(app)
connection=mysql.connect()
cursor = connection.cursor()

app.secret_key = 'super secret key'

# 1
@app.route("/db-manager-login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(
            """SELECT password
            FROM dbmanager
            WHERE username=%s""",
            (username)
        )
        hashed_password = cursor.fetchone()
        if(hashed_password is None):
            flash('No user found with given username')
            return render_template('dbManagerLogin.html')
        elif check_password(hashed_password[0], password):
            return render_template('dbManager.html')
        else:
            flash('Wrong password')
            return render_template('dbManagerLogin.html')
    return render_template('dbManagerLogin.html')

# 2
@app.route("/add-new-user", methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        institution = request.form['institution']
        name = request.form['name']
        hashed_password = hash_password(password)
        cursor.execute(
            """INSERT INTO users(username, password, institution, name)
            VALUES(%s, %s, %s, %s)""",
            (username, hashed_password, institution, name)
        )
        connection.commit()
        return render_template('dbManager.html')
    return render_template('addUser.html')

# 3
@app.route("/update-affinity-of-drug", methods=['GET', 'POST'])
def update_affinity_of_a_drug():
    if request.method == 'POST':
        reaction_id = request.form['rid']
        affinity = request.form['affinity']
        cursor.execute(
            """UPDATE bindingdb 
            SET affinity=%s
            WHERE (reaction_id = %s)""",
            (affinity, reaction_id)
        )
        connection.commit()
        return render_template('dbManager.html')
    return render_template('updateAffinityOfDrug.html')

# 4
@app.route("/delete_uniProt", methods=['GET', 'POST'])
def delete_uniProt():
    if request.method == 'POST':
        uniProt_id = request.form['pid']
        cursor.execute(
            """DELETE FROM UniProts 
            WHERE (`id` = %s)""",
            (uniProt_id)
        )
        connection.commit()
        return render_template('dbManager.html')
    return render_template('deleteProt.html')

# 5 ? TODO hard
@app.route("/update-contributors", methods=['GET', 'POST'])
def update_contributors():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        institution = request.form['institution']
        delete = request.form['delete']
        rid = request.form['rid']
        cursor.execute(
            """SELECT doi
            FROM bindingdb
            WHERE reaction_id=%s""",
            (rid)
        )
        doc = cursor.fetchone()
        doi = doc[0]
        if delete == 'Y':
            cursor.execute(
                """DELETE FROM doi 
                WHERE (doi = %s)""",
                (doi)
            )
        elif len(password) > 0:
            hashed_password = hash_password(password)
            cursor.execute(
                """INSERT INTO users(username, password, institution, name)
                VALUES(%s, %s, %s, %s)""",
                (username, hashed_password, institution, name)
            )
            cursor.execute(
                """INSERT INTO doi(doi, institution, author)
                VALUES(%s, %s, %s)""",
                (doi, institution, username)
            )
        else:
            cursor.execute(
                """INSERT INTO doi(doi, institution, author)
                VALUES(%s, %s, %s)""",
                (doi, institution, username)
            )
        connection.commit()
        return render_template('dbManager.html')
    return render_template('updateContributorsOfPaper.html')


# 6 ? TODO ez

# 7
@app.route("/user-login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        institution = request.form['institution']
        password = request.form['password']
        cursor.execute(
            """SELECT password
            FROM users
            WHERE username=%s""",
            (username)
        )
        hashed_password = cursor.fetchone()
        if(hashed_password is None):
            flash('No user found with given username')
            return render_template('userLogin.html')
        elif check_password(hashed_password[0], password):
            return render_template('dbManager.html')
        else:
            flash('Wrong password')
            return render_template('userLogin.html')
    return render_template('userLogin.html')


# 8 TODO 
@app.route("/drugs", methods=['GET'])
def get_drugs():
    cursor.execute(
        """SELECT drug.id, drug.name, drug.smile, drug.description, sid.side_id, bdb.prot_id
        FROM drugs drug, bindingdb bdb, sider sid
        WHERE drug.id=bdb.drug_id AND drug.id=sid.drug_id"""
    )
    drugs = cursor.fetchall()

# 9 TODO
@app.route("/view-interactions-of-drug", methods=['GET', 'POST'])
def view_interactions_of_drug():
    if request.method == 'POST':
        drug_id = request.form['did']
        cursor.execute(
            """SELECT interacts.id2, drug.name
            FROM interactswith interacts, drugs drug
            WHERE interacts.id1=%s AND interacts.id2=drug.id""",
            (drug_id)
        )
        interacts_with = cursor.fetchall()
        print(interacts_with)
    return render_template()


# 10
@app.route("/view-side-effects", methods=['GET', 'POST'])
def view_side_effects():
    if request.method == 'POST':
        drug_id = request.form['did']
        cursor.execute(
            """SELECT SideEffect.name
            FROM sider Sider, sideeffect SideEffect 
            WHERE Sider.drug_id=%s AND Sider.side_id=SideEffect.id""",
            (drug_id)
        )
        side_effects = cursor.fetchall()
        print(side_effects)
    return render_template('viewSideEffectsOfADrug.html')

# 11
@app.route("/view-interacting-targets", methods=['GET', 'POST'])
def view_interacting_targets():
    if request.method == 'POST':
        drug_id = request.form['did']
        cursor.execute(
            """SELECT prot.name
            FROM uniprot prot, bindingdb binding
            WHERE binding.drug_id=%s AND prot.id=binding.prot_id""",
            (drug_id)
        )
        interacting_targets = cursor.fetchall()
        print(interacting_targets)
    return render_template('viewInteractingTargetsOfADrug.html')

# 12
@app.route("/view-interacting-drugs", methods=['GET', 'POST'])
def view_interacting_drugs():
    if request.method == 'POST':
        drug_id = request.form['did']
        cursor.execute(
            """SELECT drug.name
            FROM interactswith interacts, drugs drug
            WHERE interacts.id1=%s AND drug.id=interacts.id2""",
            (drug_id)
        )
        interacting_drugs = cursor.fetchall()
        print(interacting_drugs)
    return render_template('viewInteractingDrugsOfADrug.html')

# 13
@app.route("/view-drugs-affecting-same-protein", methods=['GET'])
def view_drugs_affecting_same_protein():
    cursor.execute(
        """SELECT drug.name, drug.id, prot.name, prot.id
        FROM bindingdb binding, drugs drug, uniprot prot
        WHERE drug.id=binding.drug_id AND prot.id=binding.prot_id
        ORDER BY binding.prot_id"""
    )
    drugs_affecting_same_protein = cursor.fetchall()
    for i in drugs_affecting_same_protein:
        print(i)
    return drugs_affecting_same_protein

# 14
@app.route("/view-proteins-bind-same-drug", methods=['GET'])
def view_proteins_bind_same_drug():
    cursor.execute(
        """SELECT prot.name, prot.id, drug.name, drug.id
        FROM bindingdb binding, drugs drug, uniprot prot
        WHERE drug.id=binding.drug_id AND prot.id=binding.prot_id
        ORDER BY binding.drug_id"""
    )
    prots_binds_same_drug = cursor.fetchall()
    for i in prots_binds_same_drug:
        print(i)
    return prots_binds_same_drug

# 15
@app.route("/view-drugs-with-specific-side-effect", methods=['GET', 'POST'])
def view_drugs_with_specific_side_effect():
    if request.method == 'POST':
        side_effect_id = request.form['seid']
        cursor.execute(
            """SELECT drug.name
            FROM drugs drug, sider sid
            WHERE drug.id=sid.drug_id AND sid.side_id=%s""",
            (side_effect_id)
        )
        prots_binds_same_drug = cursor.fetchall()
        print(prots_binds_same_drug)
    return render_template('viewDrugsWithSpecificSideEffect.html')

# 16
@app.route("/search-keyword-in-drug-descriptions", methods=['GET', 'POST'])
def search_keyword_in_drug_descriptions():
    if request.method == 'POST':
        keyword = request.form['keyword']
        keyword = "%" + keyword + "%"
        cursor.execute(
            """SELECT drug.name
            FROM drugs drug
            WHERE drug.description LIKE %s""",
            (keyword)
        )
        drugs_with_the_keyword = cursor.fetchall()
        print(drugs_with_the_keyword)
    return render_template('searchKeywordInDrugDescriptions.html')

# 17
@app.route("/view-drugs-with-least-side-effects", methods=['GET', 'POST'])
def view_drugs_with_least_side_effects():
    if request.method == 'POST':
        pid = request.form['pid']
        cursor.execute(
            """SELECT drug.name, drug.id, COUNT(side.drug_id) as sideCount
            FROM drugs drug, sider side, bindingdb binding
            WHERE 
                side.drug_id=drug.id 
                AND binding.prot_id=%s 
                AND binding.drug_id=drug.id
            GROUP BY drug.id
            ORDER BY sideCount""",
            (pid)
        )
        drugs_with_least_side_effect = cursor.fetchall()
        print(drugs_with_least_side_effect)
    return render_template('searchKeywordInDrugDescriptions.html')


# 18 ? TODO
@app.route("/dois-and-contributors", methods=['GET'])
def get_dois_and_contributors():
    cursor.execute(
        """SELECT doi, author
        FROM doi
        GROUP BY doi"""
    )
    dois = cursor.fetchall()
    print(dois)
    return dois

# 19 TODO ez
@app.route("rank-institutions", methods=['GET'])
def rank_institutions():
    cursor.execute(
        """SELECT name 
        FROM institution
        ORDER BY points"""
    )
    institutions = cursor.fetchall()
    print(institutions)

# 20 TODO STORED PROCEDURES





@app.route("/test", methods=['GET'])
def test():
    a = {}
    a['test'] = [1, 2]
    if 'asdfasdf' not in a.keys():
        print('testtest')

        
