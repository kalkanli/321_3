from flask import Flask, render_template
from flaskext.mysql import MySQL
from flask import request

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'atk0k0kk00'
app.config['MYSQL_DATABASE_DB']='dtbank'
mysql = MySQL()
mysql.init_app(app)
connection=mysql.connect()
cursor = connection.cursor()



# 9 ?

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
    for tuple in drugs_affecting_same_protein:
        print(tuple)
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
    for tuple in prots_binds_same_drug:
        print(tuple)
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


# 18 ?
@app.route("/dois-and-contributors", methods=['GET'])
def get_dois_and_contributors():
    cursor.execute(
        """SELECT doi, userList
        FROM bindingdb
        GROUP BY doi, userList"""
    )
    dois_and_contributors = cursor.fetchall()
    print(dois_and_contributors)
    return dois_and_contributors

# 19

# 20

# 21

# 22
