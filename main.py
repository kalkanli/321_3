from flask import Flask, render_template, flash
from flaskext.mysql import MySQL
from flask import request
import hashlib
from helpers.password import check_password, hash_password

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'atk0k0kk00'
app.config['MYSQL_DATABASE_DB'] = 'dtbank'
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()

app.secret_key = 'super secret key'


@app.route("/", methods=['GET', 'POST'])
def homePage():
    return render_template('homepage.html')

# 1 DONE


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

# 2 DONE


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

# 3 DONE


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

# 4 DONE


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

# 5 NEEDS TESTING BUT DONE


@app.route("/update-contributors", methods=['GET', 'POST'])
def update_contributors():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
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
        cursor.execute(
            """SELECT institution
            FROM publications
            WHERE doi=%s""",
            (doi)
        )
        doc = cursor.fetchone()
        institution = doc[0]
        if delete == 'Y':
            cursor.execute(
                """DELETE FROM contributors
                WHERE (doi=%s AND author=%s)""",
                (doi, username)
            )
        elif len(password) > 0:
            hashed_password = hash_password(password)
            cursor.execute(
                """INSERT INTO user(username, password, institution, name)
                VALUES(%s, %s, %s, %s)""",
                (username, hashed_password, institution, name)
            )
            cursor.execute(
                """INSERT INTO contributors(doi, author)
                VALUES(%s, %s)""",
                (doi, username)
            )
        else:
            cursor.execute(
                """INSERT INTO contibutors(doi, author)
                VALUES(%s, %s)""",
                (doi, username)
            )
        connection.commit()
        return render_template('dbManager.html')
    return render_template('updateContributorsOfPaper.html')


# 6 TODO
@app.route("/show-data-admin/<string:type>", methods=['GET'])
def view_data_admin(type):
    if type == 'drug':
        try:
            cursor.execute("SELECT * FROM Drugs ")
            data=cursor.fetchall()
            return render_template('Drugs6.html', data=data)
        except Exception as e:
            return 'db error' 
    elif type=='prot':
        try:
            cursor.execute("SELECT * FROM UniProt ")
            data=cursor.fetchall()
            return render_template('UniProt6.html', data=data)
        except Exception as e:
            print("Problem deleting from db: " + str(e))
            return 'db error'
        
    elif type=='side-effects':
        try:
            cursor.execute("SELECT * FROM SideEffect ")
            data=cursor.fetchall()
            print(data)
            return render_template('SideEffects6.html', data=data)
        except Exception as e:
            print("error deleting from db: " + str(e))
            return 'db error'
        
    elif type=='drug-target':
        try:
            cursor.execute("SELECT reaction_id,drug_id,prot_id,affinity,measure FROM BindingDB ")
            data=cursor.fetchall()
            return render_template('DrugTarget6.html', data=data)
        except Exception as e:
            print("error deleting from db: " + str(e))
            return 'db error'
        
    elif type=='users':
        try:
            cursor.execute("SELECT * FROM user")
            data=cursor.fetchall()
            return render_template('Users6.html', data=data)
        except Exception as e:
            print("error deleting from db: " + str(e))
            return 'db error'
    elif type=='paper':
        try:
            cursor.execute("SELECT * FROM contributors")
            data=cursor.fetchall()
            result ={}
            print (data[0])
            for k in data:
                result[k[0]]=[]
            for k in data:
                print(k[0],k[1])
                result[k[0]].append(k[1])
                print(result)

            return render_template('contributors6.html',data=(result))
            
        except Exception as e:
            print("error deleting from db: " + str(e))
            return 'db error'
    elif type=='home':
        return render_template('showDataAdmin6.html')
# 7 DONE
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
            return render_template('user.html')
        else:
            flash('Wrong password')
            return render_template('userLogin.html')
    return render_template('userLogin.html')


# 8 DONE
@app.route("/drugs", methods=['GET'])
def get_drugs():
    cursor.execute(
        """SELECT d.id, d.name, d.smile, d.description, u.name, e.name
        FROM drugs d,bindingdb b, sider s, uniprot u, sideeffect e
        WHERE d.id=b.drug_id AND s.drug_id=d.id AND s.side_id=e.id AND b.prot_id=u.id"""
    )
    drugs = cursor.fetchall()
    last_drug = ""
    arr = []
    for i in drugs:
        if last_drug != i[1]:
            last_drug = i[1]
            arr.append((i[0], i[1], i[2], i[3], [i[4]], [i[5]]))
        else:
            last_tuple = arr.pop()
            if last_tuple[4].count(i[4]) == 0:
                last_tuple[4].append(i[4])
            if last_tuple[5].count(i[5]) == 0:
                last_tuple[5].append(i[5])
            arr.append(last_tuple)
    return render_template('drugs.html', data=arr)
    


# 9 DONE
@app.route("/view-interactions-of-drug", methods=['GET', 'POST'])
def view_interactions_of_drug():
    if request.method == 'POST':
        drug_id = request.form['did']
        cursor.execute(
            """SELECT d.id, d.name
            FROM interactswith i, drugs d
            WHERE %s IN (i.id1, i.id2) AND (i.id1=%s OR i.id2=%s) AND d.id!=%s AND d.id IN (i.id1, i.id2)""",
            (drug_id, drug_id, drug_id, drug_id)
        )
        interacts_with = cursor.fetchall()
        return render_template('drugInteractions.html', data=interacts_with)
    return render_template('viewInteractionsOfADrug.html')


# 10 DONE
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
        return render_template('sideEffects.html', data=side_effects)
    return render_template('viewSideEffectsOfADrug.html')

# 11 DONE
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
        return render_template('interactingProts.html', data=interacting_targets)
    return render_template('viewInteractingTargetsOfADrug.html')

# 12 DONE
@app.route("/view-interacting-drugs", methods=['GET', 'POST'])
def view_interacting_drugs():
    if request.method == 'POST':
        protein_id = request.form['pid']
        cursor.execute(
            """SELECT drug.name
            FROM bindingdb b, drugs drug
            WHERE b.prot_id=%s AND drug.id=b.drug_id""",
            (protein_id)
        )
        interacting_drugs = cursor.fetchall()
        print(interacting_drugs)
        return render_template('bindingDrugs.html', data = interacting_drugs)
    return render_template('viewInteractingDrugsOfAProt.html')

# 13 DONE
@app.route("/view-drugs-affecting-same-protein", methods=['GET'])
def view_drugs_affecting_same_protein():
    cursor.execute(
        """SELECT drug.id, prot.id
        FROM bindingdb binding, drugs drug, uniprot prot
        WHERE drug.id=binding.drug_id AND prot.id=binding.prot_id
        ORDER BY binding.prot_id"""
    )
    drugs_affecting_same_protein = cursor.fetchall()
    last_prot = ""
    arr = []
    for i in drugs_affecting_same_protein:
        if last_prot != i[1]:
            last_prot = i[1]
            arr.append((i[1], [i[0]]))
        else:
            last_tuple = arr.pop()
            last_tuple[1].append(i[0])
            arr.append(last_tuple)
    return render_template('drugsAffectingSameProtein.html', data=arr)

# 14 DONE
@app.route("/view-proteins-bind-same-drug", methods=['GET'])
def view_proteins_bind_same_drug():
    cursor.execute(
        """SELECT prot.id, drug.id
        FROM bindingdb binding, drugs drug, uniprot prot
        WHERE drug.id=binding.drug_id AND prot.id=binding.prot_id
        ORDER BY binding.drug_id"""
    )
    prots_binds_same_drug = cursor.fetchall()
    last_drug = ""
    arr = []
    for i in prots_binds_same_drug:
        if last_drug != i[1]:
            last_drug = i[1]
            arr.append((i[1], [i[0]]))
        else:
            last_tuple = arr.pop()
            if last_tuple[1].count(i[0]) == 0:
                last_tuple[1].append(i[0])
            arr.append(last_tuple)
    return render_template('protsBindingSameDrug.html', data=arr)

# 15 DONE
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
        return render_template('drugsWithSpecificSideEffect.html', data = prots_binds_same_drug)
    return render_template('viewDrugsWithSpecificSideEffect.html')

# 16 DONE
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
        return render_template('drugsWithSpecificSideEffect.html', data=drugs_with_the_keyword)
    return render_template('searchKeywordInDrugDescriptions.html')

# 17 DONE
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
        return render_template('drugsWithSpecificSideEffect.html', data=drugs_with_least_side_effect)
    return render_template('viewDrugsWithLeastSideEffects.html')


# 18 DONE
@app.route("/dois-and-contributors", methods=['GET'])
def get_dois_and_contributors():
    cursor.execute(
        """SELECT doi, author
        FROM contributors
        ORDER BY doi"""
    )
    dois = cursor.fetchall()
    last_doi = ""
    arr = []
    for i in dois:
        if last_doi != i[0]:
            last_doi = i[0]
            arr.append((i[0], [i[1]]))
        else:
            last_tuple = arr.pop()
            if last_tuple[0].count(i[1]) == 0:
                last_tuple[1].append(i[1])
            arr.append(last_tuple)
    return render_template('doiContributors.html', data = arr)

# 19 DONE
@app.route("/rank-institutions", methods=['GET'])
def rank_institutions():
    cursor.execute(
        """SELECT name, points
        FROM institution
        ORDER BY points DESC"""
    )
    institutions = cursor.fetchall()
    return render_template('institutionRanking.html', data=institutions)

# 20 TODO STORED PROCEDURES





@app.route("/test", methods=['GET'])
def test():
    a = {}
    a['test'] = [1, 2]
    if 'asdfasdf' not in a.keys():
        print('testtest')

        
