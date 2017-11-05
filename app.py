from flask import Flask
from flask import Flask, abort
from flask import jsonify
app = Flask(__name__)

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
        return "Hello World"

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
@app.route('/todo/api/v1.0/signUp',methods=['POST'])
def signupuser():
    first_name = request.form['first_name'];
    last_name = request.form['last_name'];
    address = request.form['address'];
    emailid = request.form['emailid'];
    password = request.form['password'];
    phoneno = request.form['phoneno'];
    dob = request.form['dob'];
    securityq1 = request.form['securityq1'];
    securityq2 = request.form['securityq2']
    return json.dumps({'status':'OK'});

if __name__ == '__main__':
    app.run(debug=True)
