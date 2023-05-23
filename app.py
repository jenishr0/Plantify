from flask import Flask, render_template, request, session
# import ibm_db
# import ibm_boto3
# from ibm_botocore.client import Config, ClientError
import os
app = Flask(__name__)
app.secret_key = "a"

# conn = ibm_db.connect("database =bludb;hostname =19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;port = 30699;uid = kgt86210;password =umagirJzEvpXZIDD;security=SSL;SSLServercertificate = DigiCertGlobalRootCA.crt", " ", " ")
# print("Connection Succesfull")


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM REGISTER WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account['ROLE'] == 0:
            session["Loggedin"] = True
            session["USERNAME"] = account['USERNAME']
            session["USERID"] = account['USERID']
            session['EMAIL'] = account['EMAIL']
            return render_template("home.html")
        elif account['ROLE'] == 1:
            session["Loggedin"] = True
            session["USERID"] = account['USERID']
            return render_template("admin_home.html")
        else:
            msg = "Check the Email and Password you have entered"
    return render_template("login.html", msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ROLE = 0

        sql = "SELECT * FROM REGISTER WHERE EMAIL =  ? "
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            msg = "Account already exits!"
        else:
            sql2 = "SELECT count(*) FROM REGISTER"
            stmt2 = ibm_db.prepare(conn, sql2)
            ibm_db.execute(stmt2)
            length = ibm_db.fetch_assoc(stmt2)
            print(length)
            insert_sql = "INSERT INTO REGISTER VALUES (?, ? , ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, length['1']+1)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, ROLE)
            ibm_db.execute(prep_stmt)
            msg = "your are successfully registered!"
            return render_template("login.html", msg=msg)
    return render_template("register.html", msg=msg)


@app.route('/guide', methods=['GET', 'POST'])
def guide():
    return render_template("guide.html")


@app.route('/addplants', methods=['GET', 'POST'])
def addplants():

    sql = "SELECT * FROM REGISTER WHERE ROLE=1"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_tuple(stmt)
    print(data)

    if (request.method == 'POST'):
        f = request.files['image']
        prodname = request.form['plantname']
        prodid = request.form['plantid']
        cost = request.form['cost']
        insert_sql = "INSERT INTO PRODUCT VALUES(? ,? ,? ,? ,? )"
        stmt1 = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(stmt1, 1, data[0])
        ibm_db.bind_param(stmt1, 2, data[1])
        ibm_db.bind_param(stmt1, 3, prodname)
        ibm_db.bind_param(stmt1, 4, prodid)
        ibm_db.bind_param(stmt1, 5, cost)
        ibm_db.execute(stmt1)

        sql = "SELECT * FROM PRODUCT"
        stmt2 = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt2)
        data = ibm_db.fetch_assoc(stmt2)
        print(data)

        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', '.jpg')
        f.save(filepath)
        cos_endpoint = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        cos_apikey = "7kdV61YoqEME5RtjOKWo8nNRvVwWVJsA_OM_WfK41hGd"
        cos_crn = "crn:v1:bluemix:public:cloud-object-storage:global:a/2d650ed9eaac4e0199a5a4f45176b266:59a87db9-2ce6-4801-9f07-17d5713a4ae4::"
        cos = ibm_boto3.client("s3", ibm_api_key_id=cos_apikey,
                               ibm_service_instance_id=cos_crn, config=Config(signature_version="oauth"), endpoint_url=cos_endpoint)
        cos.upload_file(Filename=filepath, Bucket='myplants74',
                        Key=prodname + '.jpg')
        print("Data sent to DB2")
        return render_template("admin_home.html")
    return render_template("admin_home.html")


@app.route('/transaction')
def transaction():
    select_sql = "SELECT * FROM TRANS"
    stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_tuple(stmt)
    print(data)
    rows = []
    while data != False:
        rows.append(data)
        data = ibm_db.fetch_tuple(stmt)
    print(rows)

    sql = "SELECT SUM(COST) AS TOT FROM TRANS WHERE USERID =" + \
        str(session['USERID'])
    stmt1 = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt1)
    account = ibm_db.fetch_tuple(stmt1)
    print(account)

    if account:
        total = str(account[0])
        print(total)

    return render_template('user_trans.html', rows=rows, total=total)


if __name__ == '__main__':
    app.run()
