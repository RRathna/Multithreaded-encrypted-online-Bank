from flask import Flask
from flask import Flask, abort
from flaskext.mysql import MySQL
from flask import jsonify
from flask_restful import reqparse
from flask import request
import requests
from werkzeug import generate_password_hash, check_password_hash
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Bank_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


customers = [
    {
        'id': 1,
        'acc_type': 'credit',
        'acc_number': '2835647',
        'first_name': 'Kalyani',
        'last_name': 'Kulkarni',
        'address ': '2200 Monroe st,1610,California',
        'emailid': 'kalyani24kulkarni@gmail.com',
        'password': 'abc',
        'phoneno': '4089308672',
        'dob': '24/05/1990',
        'securityq1': 'Your mom''s birthplace',
        'securityq2': 'Your Dad''s birthplace'
    },
    {
        'id': 2,
        'acc_type': 'debit',
        'acc_number': '82734',
        'first_name': 'Prasad',
        'last_name': 'Deshpande',
        'address ': '2200 Monroe st,1610,California',
        'emailid': 'prasad.0210@gmail.com',
        'password': 'abc',
        'phoneno': '4089308676',
        'dob': '02/10/1986',
        'securityq1': 'Your mom''s birthplace',
        'securityq2': 'Your Dad''s birthplace'
    }
]

account_details = [
    {
        'acc_number':1,
        'trans_date':'11/03/2017',
        'transaction_id':'198456',
        'message':'this is id 1',
        'amount':'$9000',
        'from_to':'Facebook',
        'debit':'yes',
        'credit':'no',
        'balance':'2679354976565848'
    },
    {
        'acc_number':2,
        'trans_date':'12/03/2017',
        'transaction_id':'298456',
        'message':'this is id 2',
        'amount':'$10000',
        'from_to':'Facebook',
        'debit':'yes',
        'credit':'yes',
        'balance':'2679354976565848'
    }
]
#-----------------------------------------------WELCOME!--------------------------------------------------
@app.route ('/')
def index():
    cursor = mysql.connect().cursor()
    cursor.execute("select * from customers")
    data =  cursor.fetchall()
    if data is None:
        return "no data\n"
    else:
        for row in data:
            return jsonify({'row':row[1]})


#-----------------get data of all customers---------------------------------------------------------------
@app.route('/todo/api/v1.0/user',methods=['GET'])
def get_all_customers():
    return jsonify({'customers':customers})

#-----------------get data of customer from id-------------------------------------------------------------
@app.route('/todo/api/v1.0/user/<int:customer_id>',methods=['GET'])
def get_customers(customer_id):
    customer = [customer for customer in customers if customer['id'] == customer_id ]
    if len(customer) == 0:
        abort(404)
    return jsonify({'customer': customer[0]})

#-----------------get all account details-------------------------------------------------------------------
@app.route('/todo/api/v1.0/accounts',methods=['GET'])
def get_all_transactions():
    return jsonify({'account_details':account_details})

#-----------------get transaction details from account number------------------------------------------------
@app.route('/todo/api/v1.0/accounts/<int:acc_num>',methods=['GET'])
def get_transactions(acc_num):
    transaction = [transaction for transaction in account_details if transaction['acc_number']== acc_num ]
    if len(transaction) == 0:
        abort(404)
    return jsonify({'transaction':transaction[0]})

#---------------------------------------Create new user-------------------------------------------------------
@app.route('/api/v1.0/user',methods=['PUT'])
def create_user():
    parser = reqparse.RequestParser()
    conn = mysql.connect()
    cursor = conn.cursor()
    parser.add_argument('first_name',required=True)
    parser.add_argument('last_name')
    parser.add_argument('address',required=True)
    parser.add_argument('emailid',required=True)
    parser.add_argument('password',required=True)
    parser.add_argument('phoneno',required=True)
    parser.add_argument('ssn',required=True)
    parser.add_argument('user_name',required=True)

    args = parser.parse_args()

    first_name = args['first_name']
    last_name = args['last_name']
    address = args['address']
    emailid = args['emailid']
    password = args['password']
    phoneno = args['phoneno']
    ssn = args['ssn']
    user_name = args['user_name']
    _hashed_password = generate_password_hash(password)
    cursor.callproc('create_user',(first_name,last_name,address,emailid,_hashed_password,phoneno,ssn,user_name))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return jsonify({'message':'User created successfully !'})
    else:
        return jsonify({'error':str(data[0])})

#---------------------------------------Sign in user using user_id and password-------------------------------------------------------

@app.route('/api/v1.0/sign-in',methods = ['OPTIONS'])
def sign_in():
    conn = mysql.connect()
    cursor = conn.cursor()
    parser = reqparse.RequestParser()
    parser.add_argument('user_name',required = True)
    parser.add_argument('password',required = True)

    args = parser.parse_args()

    user_name = args['user_name']
    password = args['password']
    cursor.execute("select password from customers where user_name = '"+user_name+"' ")
    data = cursor.fetchone()
    if data is not None and check_password_hash(data[0],password):
        return jsonify({'message':'logged in successfully !'})
    else:
        return jsonify({'message':'Username or password is wrong'})

#---------------------------------------Create user account-------------------------------------------------------

@app.route('/api/v1.0/create',methods = ['PUT'])
def create_account():
    conn = mysql.connect()
    cursor = conn.cursor()
    parser = reqparse.RequestParser()
    parser.add_argument('u_id',required = True)
    parser.add_argument('ac_type',required = True)
    parser.add_argument('bal',required = True)

    args = parser.parse_args()

    u_id = args['u_id']
    ac_type = args['ac_type']
    bal = args['bal']

    cursor.callproc('create_account',(u_id,ac_type,bal))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return jsonify({'message':'Account created successfully !'})
    else:
        return jsonify({'error':str(data[0])})

#---------------------------------------Create Teller-------------------------------------------------------

@app.route('/api/v1.0/teller',methods = ['PUT'])
def create_teller():
    conn = mysql.connect()
    cursor = conn.cursor()
    #r =  requests.post('http://www.localhost:5000/api/v1.0/user',auth=('first_name','last_name','address','emailid','password','phoneno','ssn','user_name'))
    #return jsonify({'message':r.status_code})
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',required=True)
    parser.add_argument('last_name')
    parser.add_argument('address',required=True)
    parser.add_argument('emailid',required=True)
    parser.add_argument('password',required=True)
    parser.add_argument('phoneno',required=True)
    parser.add_argument('ssn',required=True)
    parser.add_argument('user_name',required=True)

    args = parser.parse_args()

    first_name = args['first_name']
    last_name = args['last_name']
    address = args['address']
    emailid = args['emailid']
    password = args['password']
    phoneno = args['phoneno']
    ss = args['ssn']
    u_name = args['user_name']
    _hashed_password = generate_password_hash(password)
    cursor.callproc('create_user',(first_name,last_name,address,emailid,_hashed_password,phoneno,ss,u_name))
    data = cursor.fetchall()

    cursor.execute("select id from customers where user_name = '"+ u_name +"' and ssn = '"+ ss +"'")
    uid = cursor.fetchall()
    cursor.callproc('create_teller',uid)
    teller_data = cursor.fetchall()

    if len(teller_data) is 0:
        conn.commit()
        return jsonify({'message':'Teller created successfully !'})
    else:
        return jsonify({'error':str(data[0])})

#---------------------------------------Info update by customer-------------------------------------------------------

@app.route('/api/v1.0/update-info',methods = ['POST'])
def update_info():
    conn = mysql.connect()
    cursor = conn.cursor()
    parser = reqparse.RequestParser()

    parser.add_argument('user_name',required=True)
    parser.add_argument('address')
    parser.add_argument('emailid')
    parser.add_argument('password')
    parser.add_argument('phoneno')
    args = parser.parse_args()
    u_name = args['user_name']
    addr = args['address']
    email = args['emailid']
    passw = args['password']
    phone = args['phoneno']
    print("value of email is ",email)
    result = ''
    if addr is not None:
        affected_address_rows = cursor.execute("update customers set address = '"+ addr +"' where user_name = '"+ u_name +"'")
        print("Number of affected rows of address in db is",affected_address_rows)
        conn.commit()
        if affected_address_rows == 1:
            result = 'Address updated successfully'
    if email is not None:
        affected_email_rows = cursor.execute("update customers set emailid = '"+ email +"' where user_name = '"+ u_name +"'")
        print("Number of affected rows for email in db is",affected_email_rows)
        conn.commit()
        if affected_email_rows == 1:
            result = result + '\n' + 'Email updated successfully'
    if passw is not None:
        _hashed_password = generate_password_hash(passw)
        affected_password_rows = cursor.execute("update customers set password = '"+ _hashed_password +"' where user_name = '"+ u_name +"'")
        print("Number of affected rows for password in db is",affected_password_rows)
        conn.commit()
        if affected_password_rows == 1:
            result = result + '\n' + 'password updated successfully'
    if phone is not None:
        affected_phoneno_rows = cursor.execute("update customers set phoneno = '"+ phone +"' where user_name = '"+ u_name +"'")
        print("Number of affected rows for email in db is",affected_phoneno_rows)
        conn.commit()
        if affected_phoneno_rows == 1:
            result = result + '\n' + 'phone number updated successfully'
    return jsonify({'message':result})

if __name__ == '__main__':
    app.run(debug=True)
