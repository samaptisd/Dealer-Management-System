from datetime import datetime, timedelta
import os
from flask import session, redirect, url_for, Flask, render_template, jsonify, request, send_from_directory, flash
from flaskext.mysql import MySQL
import pymysql
import re
import httpagentparser
# from gevent.pywsgi import WSGIServer
import logging
import locale
from jinja2 import Environment, select_autoescape, FileSystemLoader
from flask import Flask, render_template, request
import query_execute
import time
import calendar
from logging.handlers import TimedRotatingFileHandler
from email_function import send_reset_email

# logging.basicConfig(filename=r"Error_Logs.log",
#                     level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#  'ga0qP2pEviOHhEvELY-vNS5PvnDg8XUMbOWxrFqjYUE': 'read', ==> Dealer Credential Sheet
#   'qaZrwTjzqpRtFfePqbRqgWMRq-0nq-tosZVeHl-FuOA': 'read', ==> Direct Order Trigger

api_keys = {
    '': 'read',
    '': 'read',
    '': 'read',
    '': 'write',
    '': 'read_write'
}
request_limit = 60  # in seconds
api_request_time = {}



app = Flask(__name__)


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = "Aludecor-Version-11"


# app.debug = False

log_folder = '/var/www/Dealer_App/Logs'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Setup application logger for informational and error logs with daily rotation
info_handler = TimedRotatingFileHandler(
    os.path.join(log_folder, 'Activity_Log.log'),
    when='midnight',  # Rotate the log file at midnight
    interval=1,       # Interval is set to 1 day
    backupCount=7,    # Keep log files for 7 days
    delay=True        # Delay file opening until the first log message is emitted
)
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s : %(message)s')
info_handler.setFormatter(info_formatter)

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

info_handler.addFilter(InfoFilter())

# Setup error logger for exclusive error logs with daily rotation
error_handler = TimedRotatingFileHandler(
    os.path.join(log_folder, 'Error_Log.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    delay=True
)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(threadName)s : %(message)s')
error_handler.setFormatter(error_formatter)


# Setup API logger for exclusive error logs with daily rotation
api_handler = TimedRotatingFileHandler(
    os.path.join(log_folder, 'API_Log.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    delay=True
)
api_handler.setLevel(logging.INFO)
api_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [API]: %(message)s')
api_handler.setFormatter(api_formatter)

api_logger = logging.getLogger('api_logger')  # Create a unique logger for API logs
api_logger.setLevel(logging.INFO)  # Set the logging level
api_logger.addHandler(api_handler)  # Add the handler configured for API logs



# Add handlers to app's logger
app.logger.addHandler(info_handler)
app.logger.addHandler(error_handler)
# app.logger.addHandler(api_handler)

# Set the base logger's level to INFO
app.logger.setLevel(logging.INFO)


def log_info(logger, api_key, method, query):
    log_message = f"API Key: {api_key}, Method: {method}, Query: {query}"
    logger.info(log_message)  # Use the logger passed to the function


@app.before_request
def start_timer():
    request.start_time = time.time()
    if session.get('username'):
        request.username = session.get('username')
    else:
        request.username = 'Anonymous'
    

@app.after_request
def log_request(response):
    if not hasattr(request, 'start_time'):
        request.start_time = time.time()  # Fallback if for some reason start_timer wasn't executed
    elapsed_time = time.time() - request.start_time
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    try:
        # Initialize platform and user agent details
        platform = 'Unknown'
        browser = 'Unknown'
        browser_version = ''

        # Check for custom user agents first
        if 'app_ios' in user_agent:
            platform = 'iOS App'
        elif 'app_android' in user_agent:
            platform = 'Android App'
        else:
            # Parse the user agent using httpagentparser
            parsed_user_agent = httpagentparser.detect(user_agent)
            
            browser = parsed_user_agent['browser']['name'] if 'browser' in parsed_user_agent else 'Unknown'
            browser_version = parsed_user_agent['browser']['version'] if 'browser' in parsed_user_agent else ''
            os = parsed_user_agent['platform']['name'] if 'platform' in parsed_user_agent else 'Unknown'
            
            platform = os

        simplified_user_agent = f"{browser}/{browser_version} ({platform})"

        app.logger.info(f"IP: {client_ip} | username: {request.username} | Method: {request.method} | Connection: {request.scheme} | URL: {request.full_path} | Status: {response.status} | Time taken: {elapsed_time:.3f} secs | User-Agent: {simplified_user_agent}")
    except Exception as e:
        app.logger.error("Failed to log request: " + str(e))
    return response



mysql = MySQL(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dealer_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


# # Session Log Out
# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=180)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnc.microsoft.icon')


# Custom function to format numbers as currency

def format_currency(value):
    if value is None:
        value = 0
    locale.setlocale(locale.LC_NUMERIC, "en_IN")

    formatted_value = locale.format_string('%.2f', value, grouping=True)
    return f"₹ {formatted_value}"


app.jinja_env.filters['format_currency'] = format_currency


# Login Page
@app.route('/dealer_login', methods=['GET', 'POST'])
def login():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember_me', False)
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['fullname'] = account['fullname']
            session['branch'] = account['branch']
            if remember == 'on':
                # print('yes')
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=180)
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index1.html', msg=msg)


# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_pwd():
#     if request.method == 'GET':
#         return render_template('forgot_pwd.html')
#     if request.method == 'POST':
#         username = request.form.get('username', None)
#         if username:
#             user_query = """
#                             SELECT fullname, username, password, email, pwd_reset_time, pwd_reset_time FROM dealer_db.accounts where username = %s
#                         """
#             conn = mysql.connect()
#             cursor = conn.cursor(pymysql.cursors.DictCursor)
#             cursor.execute(user_query)
#             user = cursor.fetchone()


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_pwd():
    if request.method == 'GET':
        return render_template('forgot_pwd.html')

    if request.method == 'POST':
        username = request.form.get('user_name', None)
        logger.info(username)
        if username:
            user_query = """
                SELECT fullname, username, password, email, pwd_reset_time, pwd_reset_count 
                FROM dealer_db.accounts WHERE username = %s
            """
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(user_query, (username,))
            user = cursor.fetchone()

            if user:
                last_reset_time = user['pwd_reset_time']
                reset_count = user['pwd_reset_count'] if user['pwd_reset_count'] else 0

                # Get current date & check if reset already happened today
                current_time = datetime.now()
                if last_reset_time and last_reset_time.date() == current_time.date():
                    flash("You can request a password only once per day.", "warning")
                    return redirect(url_for('forgot_pwd'))

                email_raw = user['email']
                email_list = re.split(r'[;, ]+', email_raw)  # Split multiple emails
                
                if send_reset_email(email_list, user['fullname'], user['username'], user['password']):
                    # Update password reset time and count in the database
                    update_query = """
                        UPDATE dealer_db.accounts 
                        SET pwd_reset_time = %s, pwd_reset_count = %s 
                        WHERE username = %s
                    """
                    cursor.execute(update_query, (current_time, reset_count + 1, username))
                    conn.commit()

                    flash(f"Password sent to email id: {', '.join(email_list)}", "success")
                else:
                    flash("Failed to send the email. Please try again.", "danger")
            else:
                flash("Username not found!", "danger")

        return redirect(url_for('forgot_pwd'))




# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # # connect
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    #
    # # Output message if something goes wrong...
    # msg = ''
    # # Check if "username", "password" and "email" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    #     # Create variables for easy access
    #     fullname = request.form['fullname']
    #     username = request.form['username']
    #     password = request.form['password']
    #     email = request.form['email']
    #
    #     # Check if account exists using MySQL
    #     cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
    #     account = cursor.fetchone()
    #     # If account exists show error and validation checks
    #     if account:
    #         msg = 'Account already exists!'
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         msg = 'Invalid email address!'
    #     elif not re.match(r'[A-Za-z0-9]+', username):
    #         msg = 'Username must contain only characters and numbers!'
    #     elif not username or not password or not email:
    #         msg = 'Please fill out the form!'
    #     else:
    #         # Account doesnt exists and the form data is valid, now insert new account into accounts table
    #         cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email))
    #         conn.commit()
    #
    #         msg = 'You have successfully registered!'
    # elif request.method == 'POST':
    #     # Form is empty... (no POST data)
    #     msg = 'Please fill out the form!'
    # # Show registration form with message (if any)
    return render_template('register.html', msg='')


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
            account_data = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
            return render_template('home.html', username=session['username'], account=account_data,
                                   fullname=session['fullname'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
        # account = cursor.fetchone()
        query = """
                    Select al as Item_Name, sum(inv_qty) as Total_Qty, round(SUM((Length * Width * inv_qty) / 1000000), 3) as Total_Sqm from
                    (SELECT 
                        inv_qty,
                        al,
                        grade,
                        ad,
                        length,
                        width
                    FROM
                        sales_database.warranty_sales_data
                    WHERE
                        STR_TO_DATE(inv_date, '%%d/%%m/%%Y') >= date('2025-04-01') AND inv_date <= date('2026-03-31')
                        AND 
                        bill_to_code = %s) as data group by al order by al;
                """
        try:
            cursor.execute(query, (session['username']))
            fy_data = cursor.fetchall()
            # print(fy_data)
            if fy_data == ():
                fy_data = [{'Item_Name': 'None', 'Total_Qty': 0, 'Total_Sqm': 0}]

            sum_data = 0
            sum_sqm_data = 0
            for data in fy_data:
                i = data['Total_Qty']
                j = data['Total_Sqm']
                sum_data += i
                sum_sqm_data += j

        finally:
            cursor.close()
            conn.close()
            return render_template('profile.html', fy_data=fy_data, sum_data=round(sum_data, 3), sum_sqm_data=round(sum_sqm_data, 3),
                                   fullname=session['fullname'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Care Support
@app.route('/care_support', methods=['GET', 'POST'])
def care_support():
    if request.method == 'GET':
        if 'loggedin' in session:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            support_query = f"""
                                WITH ActiveEmployee AS (
                                    SELECT P_Code, E_Code, Name, Email_O, Mob_O
                                    FROM fms_scm.employee_active
                                    WHERE Today_Status = 'Employed'
                                )
                                
                                SELECT 
                                    ac.fullname, 
                                    ac.username, 
                                    ac.branch, 
                                    ac.team_name, 
                                    coord1.Name AS Coordi1_Name,
                                    coord1.Email_O AS Coordi1_Email,
                                    coord1.Mob_O AS Coordi1_Mob,
                                    coord2.Name AS Coordi2_Name,
                                    coord2.Email_O AS Coordi2_Email,
                                    coord2.Mob_O AS Coordi2_Mob,
                                    coord3.Name AS Coordi3_Name,
                                    coord3.Email_O AS Coordi3_Email,
                                    coord3.Mob_O AS Coordi3_Mob,
                                    coord4.Name AS Coordi4_Name,
                                    coord4.Email_O AS Coordi4_Email,
                                    coord4.Mob_O AS Coordi4_Mob,
                                    zscm.Name as ZSCM_Name,
                                    zscm.Email_O AS ZSCM_Email,
                                    zscm.Mob_O as ZSCM_Mob,
                                    hscm.Name as HSCM_Name,
                                    hscm.Email_O as HSCM_Email,
                                    hscm.Mob_O as HSCM_Mob,
                                    csm1.Name AS CSM1_Name,
                                    csm1.Email_O AS CSM1_Email,
                                    csm1.Mob_O AS CSM1_Mob,
                                    csm2.Name AS CSM2_Name,
                                    csm2.Email_O AS CSM2_Email,
                                    csm2.Mob_O AS CSM2_Mob,
                                    comm_support.Name AS Comm_Name,
                                    comm_support.Email_O AS Comm_Email,
                                    comm_support.Mob_O AS Comm_Mob,
                                    hcom.Name as HCOM_Name,
                                    hcom.Email_O as HCOM_Email,
                                    hcom.Mob_O as HCOM_Mob,
                                    rh_support.Name AS RH_Name,
                                    rh_support.Email_O AS RH_Email,
                                    rh_support.Mob_O AS RH_Mob,
                                    gm_support.Name AS GM_Name,
                                    gm_support.Email_O AS GM_Email,
                                    gm_support.Mob_O AS GM_Mob
                                FROM dealer_db.accounts AS ac
                                LEFT JOIN dealer_db.care_support AS csb ON csb.Name = ac.branch
                                LEFT JOIN dealer_db.care_support AS css ON css.Name = ac.team_name
                                LEFT JOIN ActiveEmployee AS coord1 ON coord1.P_Code = csb.Co_ordinator_1
                                LEFT JOIN ActiveEmployee AS coord2 ON coord2.P_Code = csb.Co_ordinator_2
                                LEFT JOIN ActiveEmployee AS coord3 ON coord3.P_Code = csb.Co_ordinator_3
                                LEFT JOIN ActiveEmployee AS coord4 ON coord4.P_Code = csb.Co_ordinator_4
                                LEFT JOIN ActiveEmployee AS zscm ON zscm.P_Code = csb.Zonal_SCM
                                LEFT JOIN ActiveEmployee AS hscm ON hscm.P_Code = csb.HO_SCM
                                LEFT JOIN ActiveEmployee AS csm1 ON csm1.P_Code = csb.CSM_Support_1
                                LEFT JOIN ActiveEmployee AS csm2 ON csm2.P_Code = csb.CSM_Support_2
                                LEFT JOIN ActiveEmployee AS comm_support ON comm_support.P_Code = csb.Commercial_Support
                                LEFT JOIN ActiveEmployee AS hcom ON hcom.P_Code = csb.HO_Commercial
                                LEFT JOIN ActiveEmployee AS rh_support ON rh_support.P_Code = css.RH_Support
                                LEFT JOIN ActiveEmployee AS gm_support ON gm_support.P_Code = css.GM_Support
                                WHERE ac.username = %s
                            """
            try:
                cursor.execute(support_query, (session['username']))
                support_data = cursor.fetchone()
                sales_support_query = f"""
                                        SELECT 
                                        css.Customer_Id,
                                        ea.Name,
                                        ea.Email_O,
                                        ea.Mob_O
                                        FROM dealer_db.care_support_sales as css
                                        left join 
                                        (select P_Code, E_Code, Name, Email_O, Mob_O from fms_scm.employee_active where Today_Status = 'Employed') as ea
                                        on ea.P_Code = css.P_Code
                                        where css.Customer_Id = %s
                                    """
                cursor.execute(sales_support_query, (session['username']))
                sales_support_data = cursor.fetchall()
                if sales_support_data == ():
                    sales_support_data = [{'Customer_Id': session['username'], 'Name': None, 'Email_O': None, 'Mob_O': None}]
            finally:
                cursor.close()
                conn.close()
                new_support_data = {key: '' if value is None else value for key, value in support_data.items()}
                new_sales_support_data = [{key: '' if value is None else value for key, value in data.items()} for data in
                                          sales_support_data]
                return render_template('care_support.html', support_data=new_support_data,
                                       sales_support_data=new_sales_support_data)
        else:
            return redirect(url_for('login'))


# Balance Overview
@app.route('/balance_overview', methods=['GET', 'POST'])
def balance_overview():
    if request.method == 'GET':
        if 'loggedin' in session:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query_text = """
                        SELECT 
                            bo.Customer_Id,
                            SUM(bo.Total_Open) AS Total_Open,
                            SUM(bo.D_0_30) AS D_0_30,
                            SUM(bo.D_31_45) AS D_31_45,
                            SUM(bo.D_46_60) AS D_46_60,
                            SUM(bo.D_61_90) AS D_61_90,
                            SUM(bo.D_91_120) AS D_91_120,
                            SUM(bo.D_121_180) AS D_121_180,
                            SUM(bo.D_181_360) AS D_181_360,
                            SUM(bo.D_361) AS D_361,
                            round((SUM(bo.Total_Open) / subquery.TotalAmount) * 100, 2) AS Percent_Total_Open,
                            round((SUM(bo.D_0_30) / subquery.TotalAmount) * 100, 2) AS Percent_D_0_30,
                            round((SUM(bo.D_31_45) / subquery.TotalAmount) * 100, 2) AS Percent_D_31_45,
                            round((SUM(bo.D_46_60) / subquery.TotalAmount) * 100, 2) AS Percent_D_46_60,
                            round((SUM(bo.D_61_90) / subquery.TotalAmount) * 100, 2) AS Percent_D_61_90,
                            round((SUM(bo.D_91_120) / subquery.TotalAmount) * 100, 2) AS Percent_D_91_120,
                            round((SUM(bo.D_121_180) / subquery.TotalAmount) * 100, 2) AS Percent_D_121_180,
                            round((SUM(bo.D_181_360) / subquery.TotalAmount) * 100, 2) AS Percent_D_181_360,
                            round((SUM(bo.D_361) / subquery.TotalAmount) * 100, 2) AS Percent_D_361
                        FROM dealer_db.balance_overview AS bo
                        JOIN (
                            SELECT 
                                Customer_Id,
                                SUM(Total_Open) AS TotalAmount
                            FROM dealer_db.balance_overview
                            GROUP BY Customer_Id
                        ) AS subquery
                        ON bo.Customer_Id = subquery.Customer_Id
                        where bo.Customer_Id = %s
                        GROUP BY bo.Customer_Id
                    """
            try:
                cursor.execute(query_text, (session['username']))
                balance_data = cursor.fetchone()
                # print(balance_data)
            finally:
                cursor.close()
                conn.close()
                return render_template('balance_overview.html', balance_data=balance_data)
        else:
            return redirect(url_for('login'))



# Order booking Form
@app.route('/order_booking_form', methods=['GET', 'POST'])
def form():
    if 'loggedin' in session:
        if request.method == 'GET':
            message = ''
            return render_template('Order_booking_Form.html', username=session['username'], message=message,
                                   fullname=session['fullname'])
        elif request.method == 'POST':
            if 'loggedin' in session:
                conn = mysql.connect()
                cursor = conn.cursor()
                form_data = request.form.to_dict(flat=False)
                diff_address = form_data['diff_address']
                if diff_address == ['No']:
                    address = None
                    state = None
                    pincode = None
                    contact_name = None
                    contact_number = None
                elif diff_address == ['Yes']:
                    address = form_data['address']
                    state = form_data['state']
                    pincode = form_data['pincode']
                    contact_name = form_data['contact_name']
                    contact_number = form_data['contact_number']
                remarks = form_data['remarks']
                order_type = form_data['order_type']
                item_code = form_data.get('item_code', [])
                product_grade = form_data.get('product_grade', [])
                color_code = form_data.get('color_code', [])
                length = form_data.get('length', [])
                width = form_data.get('width', [])
                matching_lot = form_data.get('matching_lot', [])
                order_qty = form_data.get('order_qty', [])
                order_data = []
                item_count = len(item_code)
                for i in list(range(item_count)):
                    row = {
                        'order_type': order_type[i],
                        'diff_address': diff_address,
                        'address': address,
                        'state': state,
                        'pincode': pincode,
                        'contact_name': contact_name,
                        'contact_number': contact_number,
                        'remarks': remarks,
                        'item_code': item_code[i],
                        'product_grade': product_grade[i],
                        'color_code': color_code[i],
                        'length': length[i],
                        'width': width[i],
                        'matching_lot': matching_lot[i],
                        'order_qty': order_qty[i]
                    }
                    order_data.append(row)

                current_timestamp = datetime.now()
                custom_format = current_timestamp.strftime('/%y%m%d/%H%M%S')
                order_no = session['username'] + custom_format
                timestamp = current_timestamp.strftime('%y-%m-%d %H:%M:%S')
                record_no_query = "Select Count(Distinct Order_Id) from dealer_db.orders"
                cursor.execute(record_no_query)
                record_data = cursor.fetchone()
                record_no = int(record_data[0]) + 1
                for order in order_data:
                    sql_query = """
                        INSERT INTO dealer_db.orders (Timestamp, Order_Id, Customer_Id, Order_Type, Diff_Address, Address,
                        State, Pincode, Contact_Name, Contact_No, Item_Code, Product_Grade, Color_Code, Length, Width, Matching_Lot, Order_Qty,
                        Record_No, Customer_Name, Branch, Remarks)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (
                        timestamp,
                        order_no,
                        session['username'],
                        order['order_type'],
                        order['diff_address'][0],
                        order['address'],
                        order['state'],
                        order['pincode'],
                        order['contact_name'],
                        order['contact_number'],
                        order['item_code'],
                        order['product_grade'],
                        order['color_code'],
                        order['length'],
                        order['width'],
                        order['matching_lot'],
                        order['order_qty'],
                        record_no, session['fullname'], session['branch'], order['remarks']
                    )
                    cursor.execute(sql_query, values)
                    conn.commit()
                
                email_quary = """
                                INSERT INTO dealer_db.orders_email
                                    (Order_Id, Order_Time, Branch, SAP_Code, Customer_Name)
                                    VALUES(%s, %s, %s, %s, %s)
                            """
                values1 = (order_no, timestamp, session['branch'], session['username'], session['fullname'])
                cursor.execute(email_quary, values1)
                conn.commit()

                cursor.close()
                conn.close()

                # message = f"Your Order No: {session['username'] + current_timestamp} has been submitted successfully."
                message = f"<i class='fa fa-check-circle'> Your Order No: <b>{order_no}</b> has been submitted successfully.</i>"
                return render_template('Order_booking_Form.html', username=session['username'], message=message,
                                       fullname=session['fullname'])
            return redirect(url_for('login'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# @app.route('/')
# def result():
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('Order_booking_Form.html', username=session['username'], fullname=session['fullname'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))


# Booked_Order_Details
@app.route('/booked_order')
def booked_order():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                """
                    SELECT 
                    o.Order_Id, 
                    o.Item_Code, 
                    o.Product_Grade, 
                    o.Color_Code, 
                    o.Length, 
                    o.Width, 
                    o.Matching_Lot, 
                    o.Order_Qty, 
                    ROUND(SUM(o.Length * o.Width * o.Order_Qty / 1000000)) AS Order_Qty_SQM,
                    o.Timestamp 
                FROM 
                    dealer_db.orders o
                LEFT JOIN 
                    dealer_db.whoms_order_calculation w ON
                    concat(o.Order_Id, o.Item_Code, o.Product_Grade, o.Color_Code, o.Length, o.Width) = w.Static_Unique_Id
                WHERE 
                    o.Customer_Id = %s AND 
                    w.Order_Number IS NULL
                GROUP BY 
                    o.Order_Id, 
                    o.Item_Code, 
                    o.Product_Grade, 
                    o.Color_Code, 
                    o.Length, 
                    o.Width, 
                    o.Matching_Lot, 
                    o.Order_Qty,
                    o.Timestamp

                """, [session['username']])
            orders = cursor.fetchall()


        finally:
            cursor.close()
            conn.close()
            return render_template('booked_order.html', orders=orders,
                                   fullname=session['fullname'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/get_data", methods=["POST", "GET"])
def get_data():
    if request.method == 'POST':
        if 'loggedin' in session:
            start_date = datetime.fromisoformat(request.form['start_date']).strftime('%Y-%m-%d')
            end_date = datetime.fromisoformat(request.form['end_date']).strftime('%Y-%m-%d')
            # print(start_date)
            # print(end_date)
            query = "SELECT * from dealer_db.orders WHERE date_format(Timestamp, '%Y-%m-%d') BETWEEN '{}' AND '{}' and Customer_Id = '{}'".format(
                start_date, end_date, session['username'])
            conn = mysql.connect()
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                ordersrange = cursor.fetchall()
            finally:
                cursor.close()
                conn.close()
                orders = []
                for row in ordersrange:
                    orders.append({
                        'Order_Id': row[2],
                        'Timestamp': datetime.strftime(row[1], '%Y-%m-%d %H:%M:%S'),
                        'Item_Code': row[9],
                        'Product_Grade': row[10],
                        'Color_Code': row[11],
                        'Length': row[12],
                        'Width': row[13],
                        'Matching_Lot': row[14],
                        'Order_Qty': row[15],
                    })
                    print(orders)
                return jsonify({'orders': orders})
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# @app.route('/thank_you')
# def thank():
#     return render_template('thank_you.html')


####Catalouge View####
@app.route('/flip')
def flip():
    if 'loggedin' in session:
        return render_template('flip.html')
    return redirect(url_for('login'))


@app.route('/regular')
def regular():
    if 'loggedin' in session:
        return render_template('MSC Regular.html')
    return redirect(url_for('login'))


@app.route('/special')
def special():
    if 'loggedin' in session:
        return render_template('MSC_Special.html')
    return redirect(url_for('login'))


@app.route('/Aluwall')
def Aluwall():
    if 'loggedin' in session:
        return render_template('Aluwall.html')
    return redirect(url_for('login'))


@app.route('/sand_and_rustic')
def sand_and_rustic():
    if 'loggedin' in session:
        return render_template('Sand and Rustic.html')
    return redirect(url_for('login'))


@app.route('/ACE')
def ACE():
    if 'loggedin' in session:
        return render_template('ACE-Timber-Pedra.html')
    return redirect(url_for('login'))


@app.route('/AL3C')
def AL3C():
    if 'loggedin' in session:
        return render_template('AludecorAL3C.html')
    return redirect(url_for('login'))


@app.route('/wabisabi')
def wabisabi():
    if 'loggedin' in session:
        return render_template('Wabi Sabi.html')
    return redirect(url_for('login'))


@app.route('/elevate')
def elevate():
    if 'loggedin' in session:
        return render_template('elevate.html')
    return redirect(url_for('login'))


@app.route('/booklet')
def booklet():
    if 'loggedin' in session:
        return render_template('3Dbooklet.html')
    return redirect(url_for('login'))


@app.route('/AGArmor')
def AGArmor():
    if 'loggedin' in session:
        return render_template('AGArmor.html')
    return redirect(url_for('login'))


@app.route('/viSecure')
def viSecure():
    if 'loggedin' in session:
        return render_template('vi-Secure.html')
    return redirect(url_for('login'))


@app.route('/aludecorsystem')
def aludecorsystem():
    if 'loggedin' in session:
        return render_template('aludecorsystem.html')
    return redirect(url_for('login'))

@app.route('/zinco')
def zinco():
    if 'loggedin' in session:
        return render_template('zinco.html')
    return redirect(url_for('login'))

@app.route('/rugged')
def rugged():
    if 'loggedin' in session:
        return render_template('rugged.html')
    return redirect(url_for('login'))

@app.route('/earthcoat')
def earthcoat():
    if 'loggedin' in session:
        return render_template('earthcoat.html')
    return redirect(url_for('login'))

@app.route('/titanium')
def titanium():
    if 'loggedin' in session:
        return render_template('titanium.html')
    return redirect(url_for('login'))

@app.route('/sinex')
def sinex():
    if 'loggedin' in session:
        return render_template('sinex.html')
    return redirect(url_for('login'))

@app.route('/louver')
def louver():
    if 'loggedin' in session:
        return render_template('louver.html')
    return redirect(url_for('login'))

# Change Password
@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if request.method == 'GET':
        if 'loggedin' in session:
            logo = '/static/Logo.png'
            # body = '/static/body.jpg'
            message = ''
            return render_template('change_Password_form.html', username=session['username'], logo=logo,
                                   message=message)
        return redirect(url_for('login'))
    elif request.method == 'POST':
        if 'loggedin' in session:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            form_data = request.form.to_dict()
            new_pwd = form_data['newpwd']
            confrim_pwd = form_data['confirmpwd']
            # username = session['username']
            message = ''
            if new_pwd == confrim_pwd:
                try:
                    cur.execute("""
                    Update dealer_db.accounts set password = %s where username = %s;
                    """, [new_pwd, session['username']])
                    conn.commit()
                finally:
                    cur.close()
                    conn.close()
                    message = 'Password has been changed successfully.'
                    logo = '/static/Logo.png'
                    return render_template('change_Password_form.html', username=session['username'], logo=logo,
                                           message=message)
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# booked_order status####
@app.route('/order_status')
def order_status():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute(
        #     f"""
        #                     SELECT
        #                     wo.Timestamp,
        #                     wo.Order_Date,
        #                     wo.Order_Number,
        #                     wo.Bill_to_Code,
        #                     wo.Branch,
        #                     wo.Team_Name,
        #                     wo.Bill_to_Client_Name,
        #                     wo.Static_Unique_Id,
        #                     wo.Item_Name,
        #                     wo.Grade,
        #                     wo.Colour,
        #                     wo.Length,
        #                     wo.Width,
        #                     wo.Required_Batch,
        #                     wo.Order_Qty_Sheet,
        #                     wo.Special_Remarks,
        #                     wo.Ship_Add_Diff,
        #                     wo.Ship_to_Address,
        #                     wo.Order_Qty_Sq_Mtrs,
        #                     wo.SAP_Material_Number,
        #                     wo.Alloy_Grade,
        #                     wo.Ship_To_Code,
        #                     wo.Ship_to_Client_Name,
        #                     wo.Aludecorian,
        #                     wo.PI_Reference_No,
        #                     wo.PO_Reference_No,
        #                     wo.Freight,
        #                     wo.Payment_Terms,
        #                     wo.Order_Reconfirmation,
        #                     wo.Nature_of_Urgency,
        #                     wo.Type_of_Order,
        #                     wo.SO_No,
        #                     wo.STO_Number,
        #                     wo.Other_Branch,
        #                     wo.User_Email,
        #                     wo.Archive_Status,
        #                     cncl.Total_Qty as Cancelled_Qty,
        #                     if(cncl.Total_Qty is null, wo.Order_Qty_Sheet, (wo.Order_Qty_Sheet - cncl.Total_Qty)) as Final_Order_Qty,
        #                     rcv.Total_Qty as Received_Qty_From_Plant,
        #                     rcv.Receiving_Date as Last_Received_Date,
        #                     rcv.Batch_No as Received_Batch_No,
        #                     disp.Total_Qty as Dipatched_Qty_From_WH,
        #                     disp.Dispatched_Date as Last_Dispatched_Date,
        #                     disp.Batch_No as Dispatched_Batch_No,
        #                     case
        #                         when wo.Type_of_Order = 'Plant Order' or wo.Type_of_Order = 'Inter Branch' then
        #                             if(rcv.Total_Qty is null, 0,
        #                                 if(disp.Total_Qty is null, rcv.Total_Qty, (rcv.Total_Qty - Disp.Total_Qty))
        #                             )
        #                         else null
        #                     end as Qty_Pending_At_WH,
        #                     if(cncl.Total_Qty is null, wo.Order_Qty_Sheet, (wo.Order_Qty_Sheet - cncl.Total_Qty)) - if(disp.Total_Qty is null, 0, disp.Total_Qty) as Pending_SO_Qty
        #                 FROM
        #                     dealer_db.whoms_order AS wo
        #                     left join (select Unique_ID, sum(Cancelled_Qty) as Total_Qty, max(str_to_date(timestamp, '%%d/%%m/%%Y')) as Cancel_Date from dealer_db.whoms_cancellation_form group by Unique_ID) as cncl
        #                         on cncl.Unique_Id = concat(wo.Order_Number, wo.SAP_Material_Number)
        #                     left join (Select Unique_ID, sum(Received_Qty_from_Plant) as Total_Qty, max(str_to_date(receiving_date, '%%d/%%m/%%Y')) as  Receiving_Date,
        #                         substring( group_concat(' ', Batch_No, ': ', Received_Qty_from_Plant order by Batch_No), 2) as Batch_No
        #                         from dealer_db.whoms_pdo_receiving group by Unique_ID) as rcv on rcv.Unique_Id = concat(wo.STO_Number, SAP_Material_Number)
        #                     left join (SELECT Unique_Id_WHOMS, SUM(inv_qty) AS Total_Qty, MAX(str_to_date(inv_date, '%%d/%%m/%%Y')) AS Dispatched_Date,
        #                         substring(group_concat(' ', batch, ': ', inv_qty order by batch), 2) as Batch_No
        #                         FROM sales_database.warranty_sales_data GROUP BY Unique_Id_WHOMS) as disp on disp.Unique_Id_WHOMS = concat(wo.SO_NO, wo.SAP_Material_Number)
        #                 WHERE
        #                 wo.SO_No is not null
        #                 AND wo.Bill_to_Code = %s
        #                 AND (if(cncl.Total_Qty is null, wo.Order_Qty_Sheet, (wo.Order_Qty_Sheet - cncl.Total_Qty)) - if(disp.Total_Qty is null, 0, disp.Total_Qty)) > 0
        #
        #
        #     """, [session['username']])
        query = """
                    Select
                        pnd.Order_Number,
                        pnd.Order_Date,
                        pnd.Bill_to_Code,
                        pnd.Item_Name,
                        pnd.Grade,
                        pnd.Colour,
                        pnd.Length,
                        pnd.Width,
                        pnd.Required_Batch,
                        pnd.SO_No,
                        pnd.Pending_SO_Qty,
                        ROUND((pnd.Width * pnd.Length * pnd.Pending_SO_Qty)/1000000, 3) as Pending_SQ_Mtr
                    from
                        (Select
                            woc.Order_Number,
                            woc.Order_Date,
                            woc.Bill_to_Code,
                            woc.Item_Name,
                            woc.Grade,
                            woc.Colour,
                            woc.Length,
                            woc.Width,
                            woc.Required_Batch,
                            woc.SO_No,
                            woc.Pending_SO_Qty
                        from dealer_db.whoms_order_calculation as woc
                        where woc.Pending_SO_Qty > 0 and (woc.Order_Reconfirmation= 'Confirm' or woc.Order_Reconfirmation = 'Revised')) as pnd where pnd.Bill_to_Code = %s
                """
        cursor.execute(query, (session['username']))
        try:
            order_status = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
            return render_template('order_status.html', order_status=order_status, fullname=session['fullname'])
    return redirect(url_for('login'))


@app.route("/get_data_status", methods=["POST", "GET"])
def get_data_status():
    if request.method == 'POST':
        if 'loggedin' in session:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            start_date = datetime.fromisoformat(request.form['start_date']).strftime('%Y-%m-%d')
            end_date = datetime.fromisoformat(request.form['end_date']).strftime('%Y-%m-%d')
            # print(start_date)
            # print(end_date)
            # query = f"""
            #             SELECT
            #             wo.Timestamp,
            #             wo.Order_Date,
            #             wo.Order_Number,
            #             wo.Bill_to_Code,
            #             wo.Branch,
            #             wo.Team_Name,
            #             wo.Bill_to_Client_Name,
            #             wo.Static_Unique_Id,
            #             wo.Item_Name,
            #             wo.Grade,
            #             wo.Colour,
            #             wo.Length,
            #             wo.Width,
            #             wo.Required_Batch,
            #             wo.Order_Qty_Sheet,
            #             wo.Special_Remarks,
            #             wo.Ship_Add_Diff,
            #             wo.Ship_to_Address,
            #             wo.Order_Qty_Sq_Mtrs,
            #             wo.SAP_Material_Number,
            #             wo.Alloy_Grade,
            #             wo.Ship_To_Code,
            #             wo.Ship_to_Client_Name,
            #             wo.Aludecorian,
            #             wo.PI_Reference_No,
            #             wo.PO_Reference_No,
            #             wo.Freight,
            #             wo.Payment_Terms,
            #             wo.Order_Reconfirmation,
            #             wo.Nature_of_Urgency,
            #             wo.Type_of_Order,
            #             wo.SO_No,
            #             wo.STO_Number,
            #             wo.Other_Branch,
            #             wo.User_Email,
            #             wo.Archive_Status,
            #             cncl.Total_Qty as Cancelled_Qty,
            #             if(cncl.Total_Qty is null, wo.Order_Qty_Sheet, (wo.Order_Qty_Sheet - cncl.Total_Qty)) as Final_Order_Qty,
            #             rcv.Total_Qty as Received_Qty_From_Plant,
            #             rcv.Receiving_Date as Last_Received_Date,
            #             rcv.Batch_No as Received_Batch_No,
            #             disp.Total_Qty as Dipatched_Qty_From_WH,
            #             disp.Dispatched_Date as Last_Dispatched_Date,
            #             disp.Batch_No as Dispatched_Batch_No,
            #             case
            #                 when wo.Type_of_Order = 'Plant Order' or wo.Type_of_Order = 'Inter Branch' then
            #                     if(rcv.Total_Qty is null, 0,
            #                         if(disp.Total_Qty is null, rcv.Total_Qty, (rcv.Total_Qty - Disp.Total_Qty))
            #                     )
            #                 else null
            #             end as Qty_Pending_At_WH,
            #             if(cncl.Total_Qty is null, wo.Order_Qty_Sheet, (wo.Order_Qty_Sheet - cncl.Total_Qty)) - if(disp.Total_Qty is null, 0, disp.Total_Qty) as Pending_SO_Qty
            #         FROM
            #             dealer_db.whoms_order AS wo
            #             left join (select Unique_ID, sum(Cancelled_Qty) as Total_Qty, max(str_to_date(timestamp, '%%d/%%m/%%Y')) as Cancel_Date from dealer_db.whoms_cancellation_form group by Unique_ID) as cncl
            #                 on cncl.Unique_Id = concat(wo.Order_Number, wo.SAP_Material_Number)
            #             left join (Select Unique_ID, sum(Received_Qty_from_Plant) as Total_Qty, max(str_to_date(receiving_date, '%%d/%%m/%%Y')) as  Receiving_Date,
            #                 substring( group_concat(' ', Batch_No, ': ', Received_Qty_from_Plant order by Batch_No), 2) as Batch_No
            #                 from dealer_db.whoms_pdo_receiving group by Unique_ID) as rcv on rcv.Unique_Id = concat(wo.STO_Number, SAP_Material_Number)
            #             left join (SELECT Unique_Id_WHOMS, SUM(inv_qty) AS Total_Qty, MAX(str_to_date(inv_date, '%%d/%%m/%%Y')) AS Dispatched_Date,
            #                 substring(group_concat(' ', batch, ': ', inv_qty order by batch), 2) as Batch_No
            #                 FROM sales_database.warranty_sales_data GROUP BY Unique_Id_WHOMS) as disp on disp.Unique_Id_WHOMS = concat(wo.SO_NO, wo.SAP_Material_Number)
            #         WHERE
            #         wo.SO_No is not null
            #         AND str_to_date(wo.Order_Date,'%%d/%%m/%%Y') BETWEEN date('{start_date}') AND date('{end_date}')
            #         AND wo.Bill_to_Code = %s
            #         """
            # cursor.execute(query, [session['username']])
            # print(query)
            query = f"""
                        Select
                            pnd.Order_Number,
                            pnd.Order_Date,
                            pnd.Bill_to_Code,
                            pnd.Item_Name,
                            pnd.Grade,
                            pnd.Colour,
                            pnd.Length,
                            pnd.Width,
                            pnd.Required_Batch,
                            pnd.SO_No,
                            pnd.Pending_SO_Qty,
                            ROUND((pnd.Width * pnd.Length * pnd.Pending_SO_Qty)/1000000, 3) as Pending_SQ_Mtr
                        from
                            (Select
                                woc.Order_Number,
                                woc.Order_Date,
                                woc.Bill_to_Code,
                                woc.Item_Name,
                                woc.Grade,
                                woc.Colour,
                                woc.Length,
                                woc.Width,
                                woc.Required_Batch,
                                woc.SO_No,
                                woc.Pending_SO_Qty
                            from dealer_db.whoms_order_calculation as woc
                            where woc.Pending_SO_Qty > 0) as pnd where pnd.Bill_to_Code = %s
                            AND str_to_date(pnd.Order_Date,'%%d/%%m/%%Y') BETWEEN date('{start_date}') AND date('{end_date}')
                        """
            try:
                cursor.execute(query, (session['username']))
                status = cursor.fetchall()
                # print(status)
            finally:
                cursor.close()
                conn.close()
                # statusrange = []
                # for row in status:
                #     statusrange.append({
                #         'Order_Number': row[2],
                #         'SO_No': row[31],
                #         'Order_Date': row[1],
                #         'Item_Name': row[8],
                #         'Grade': row[9],
                #         'Colour': row[10],
                #         'Length': row[11],
                #         'Width': row[12],
                #         'Required_Batch': row[13],
                #         'Order_Qty_Sheet': row[14],
                #         'Order_Qty_Sq_Mtrs': row[18],
                #     })
                # print(status)
                return jsonify({'order': status})
        ###User is not loggedin redirect to login page
        return redirect(url_for('login'))


# Completed Transuction Histroy ###
@app.route('/order_transuction')
def order_transuction():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.now()
        first_day_of_current_month = now.replace(day=1)
        first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
        start_date = first_day_of_previous_month.strftime('%Y-%m-%d')
        _, last_day = calendar.monthrange(now.year, now.month)
        end_date = now.replace(day=last_day).strftime('%Y-%m-%d')  # Last day of the current month
        try:
            cursor.execute(
                """
                    SELECT
                        bill_to_code,
                        CASE
                            WHEN original_invoice IS NOT NULL AND original_invoice <> '' THEN original_invoice
                            ELSE invno
                        END AS invno,
                        bill_to_name,
                        sales_order,
                        inv_date,
                        original_invoice,
                        batch,
                        inv_qty,
                        al,
                        grade,
                        ad,
                        length,
                        width
                    FROM
                        sales_database.warranty_sales_data
                    WHERE
                        STR_TO_DATE(inv_date, '%%d/%%m/%%Y') >= DATE(%s) AND inv_date <= DATE(%s)
                        AND 
                        bill_to_code = %s
                        ORDER BY inv_date DESC, invno DESC
                """, [start_date, end_date, session['username']])
            order_transuction = cursor.fetchall()
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            return render_template('Completed Transuction History.html', order_transuction=order_transuction,
                                   fullname=session['fullname'], start_date=start_date, end_date=end_date)
    return redirect(url_for('login'))


### Filter Completed Transuction Histroy ###

@app.route("/trunstion_history", methods=["POST", "GET"])
def trunstion_history():
    if request.method == 'POST':
        if 'loggedin' in session:
            conn = mysql.connect()
            cursor = conn.cursor()
            start_date = datetime.fromisoformat(request.form['start_date']).strftime('%Y-%m-%d')
            end_date = datetime.fromisoformat(request.form['end_date']).strftime('%Y-%m-%d')
            # print(start_date)
            # print(end_date)
            query = f"""
                        SELECT
                            bill_to_code,
                            CASE
                                WHEN original_invoice IS NOT NULL AND original_invoice <> '' THEN original_invoice
                                ELSE invno
                            END AS invno,
                            bill_to_name,
                            sales_order,
                            inv_date,
                            original_invoice,
                            batch,
                            inv_qty,
                            al,
                            grade,
                            ad,
                            length,
                            width
                        FROM
                            sales_database.warranty_sales_data
                        WHERE
                            STR_TO_DATE(inv_date, '%%d/%%m/%%Y') BETWEEN date('{start_date}') AND date('{end_date}')
                            AND 
                            bill_to_code = %s 
                            ORDER BY inv_date DESC, invno DESC                                     
                    """
            try:
                cursor.execute(query, [session['username']])
                transuction = cursor.fetchall()
                # print(transuction)
            finally:
                cursor.close()
                conn.close()
                transuctionrange = []
                for row in transuction:
                    transuctionrange.append({
                        'bill_to_code': row[0],
                        'invno': row[1],
                        'bill_to_name': row[2],
                        'sales_order': row[3],
                        'inv_date': row[4],
                        'original_invoice': row[5],
                        'batch': row[6],
                        'inv_qty': row[7],
                        'al': row[8],
                        'grade': row[9],
                        'ad': row[10],
                        'length': row[11],
                        'width': row[12],
                    })
                    print(transuctionrange)
                return jsonify({'histroy': transuctionrange})
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# # account details
# @app.route('/account_details')
# def account_details():
#     if 'loggedin' in session:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # We need all the account info for the user so we can display it on the profile page
#         cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
#         try:
#             account = cursor.fetchone()
#             query_current_fy_data = f"""
#                                     select * from dealer_db.cur_fy_sales where Bill_to_Code = %s
#                                 """
#             cursor.execute(query_current_fy_data, (session['username']))
#             cur_fy_data = cursor.fetchall()
#             if cur_fy_data == ():
#                 cur_fy_data = [{'Bill_to_Code': session['username'], 'Total_Sale': 0, 'Total_Sale_Special': 0}]
#             if float(cur_fy_data[0]['Total_Sale_Special']) >= 20000 or float(cur_fy_data[0]['Total_Sale']) >= 30000:
#                 category = "Platinum"
#             elif float(cur_fy_data[0]['Total_Sale_Special']) >= 15000 or float(cur_fy_data[0]['Total_Sale']) >= 20000:
#                 category = "Gold"
#             elif float(cur_fy_data[0]['Total_Sale_Special']) >= 10000 or float(cur_fy_data[0]['Total_Sale']) >= 15000:
#                 category = "Silver"
#             else:
#                 category = "BASE"
#             query_prev_fy_data = f"""
#                                     select Prev_FY_Status from dealer_db.care_support_sales where
#                                     Customer_Id = %s
#                                 """
#             cursor.execute(query_prev_fy_data, (session['username']))
#             prev_fy_data = cursor.fetchall()
#             if prev_fy_data == ():
#                 prev_fy_data = [{'Prev_FY_Status': 'Base'}]
#         finally:
#             cursor.close()
#             conn.close()
#             # print(member_data)
#             # Show the profile page with account info
#             return render_template('account_details.html',category=category, cur_fy_data=cur_fy_data, prev_fy_data=prev_fy_data, account=account, fullname=session['fullname'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# account details
@app.route('/account_details')
def account_details():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
        try:
            account = cursor.fetchone()
            query_prev_fy_data = f"""
                                        select Prev_FY_Status from dealer_db.care_support_sales where
                                        Customer_Id = %s
                                    """
            cursor.execute(query_prev_fy_data, (session['username']))
            prev_fy_data = cursor.fetchone()
            # print(prev_fy_data)
            if prev_fy_data is None:
                prev_fy_data = {'Prev_FY_Status': 'Base'}
                prev_category = prev_fy_data['Prev_FY_Status']
            else:
                prev_category = prev_fy_data['Prev_FY_Status']

            query_current_fy_data = f"""
                                    select * from dealer_db.cur_fy_sales where Bill_to_Code = %s
                                """
            cursor.execute(query_current_fy_data, (session['username']))
            cur_fy_data = cursor.fetchone()

            # Default values
            cur_total_sale_sp = 0
            cur_total_sale = 0

            if cur_fy_data is None:
                cur_fy_data = {'Bill_to_Code': session['username'], 'Total_Sale': 0, 'Total_Sale_Special': 0}
                cur_total_sale_sp = cur_fy_data['Total_Sale_Special']
                cur_total_sale = cur_fy_data['Total_Sale']
            else:
                cur_total_sale_sp = cur_fy_data['Total_Sale_Special']
                cur_total_sale = cur_fy_data['Total_Sale']

            # print(f"Current Total: {cur_total_sale}")
            # print(f"Current Total SP: {cur_total_sale_sp}")

            tier_id = {1: 'Base',
                       2: 'Silver',
                       3: 'Gold',
                       4: 'Platinum'}

            tier_list_id = {'Base': 1,
                            'Silver': 2,
                            'Gold': 3,
                            'Platinum': 4}

            tier_value_total = {'Base': 0,
                                'Silver': 15000,
                                'Gold': 20000,
                                'Platinum': 30000}

            tier_value_total_sp = {'Base': 0,
                                   'Silver': 10000,
                                   'Gold': 15000,
                                   'Platinum': 20000}

            if float(cur_total_sale_sp) >= tier_value_total_sp['Platinum'] or float(cur_total_sale) >= tier_value_total[
                'Platinum']:
                renew_upgrade_data = {
                    'cur_category': 'Platinum'
                }
            elif float(cur_total_sale_sp) >= tier_value_total_sp['Gold'] or float(cur_total_sale) >= tier_value_total[
                'Gold']:
                renew_upgrade_data = {
                    'cur_category': 'Gold',
                    'next_category': 'Platinum',
                    'req_for_upgrade_t': round(tier_value_total['Platinum'] - float(cur_total_sale), 3),
                    'req_for_upgrade_t_sp': round(tier_value_total_sp['Platinum'] - float(cur_total_sale_sp), 3)
                }
            elif float(cur_total_sale_sp) >= tier_value_total_sp['Silver'] or float(cur_total_sale) >= tier_value_total[
                'Silver']:
                renew_upgrade_data = {
                    'cur_category': 'Silver',
                    'next_category': 'Gold',
                    'req_for_upgrade_t': round(tier_value_total['Gold'] - float(cur_total_sale), 3),
                    'req_for_upgrade_t_sp': round(tier_value_total_sp['Gold'] - float(cur_total_sale_sp), 3)
                }
            else:
                renew_upgrade_data = {
                    'cur_category': 'Base',
                    'next_category': 'Silver',
                    'req_for_upgrade_t': round(tier_value_total['Silver'] - float(cur_total_sale), 3),
                    'req_for_upgrade_t_sp': round(tier_value_total_sp['Silver'] - float(cur_total_sale_sp), 3)
                }

            if tier_list_id[renew_upgrade_data['cur_category']] > tier_list_id[prev_category]:
                renew_upgrade_data['Higher_Achieved'] = 'Yes'
                # print(renew_upgrade_data['Higher_Achieved'])
                if renew_upgrade_data['cur_category'] == 'Platinum':
                    renew_upgrade_data['Max_Tier'] = 'Yes'
                else:
                    renew_upgrade_data['Max_Tier'] = 'No'
                    next_category = tier_id[tier_list_id[renew_upgrade_data['cur_category']] + 1]
                    renew_upgrade_data['next_category'] = next_category
                    renew_upgrade_data['req_for_upgrade_t'] = round(
                        tier_value_total[next_category] - float(cur_total_sale), 3)
                    renew_upgrade_data['req_for_upgrade_t_sp'] = round(
                        tier_value_total_sp[next_category] - float(cur_total_sale_sp), 3)
            else:
                if prev_category == 'Platinum':
                    renew_upgrade_data['Higher_Achieved'] = 'No'
                    renew_upgrade_data['Max_Tier'] = 'Yes'
                else:
                    renew_upgrade_data['Higher_Achieved'] = 'No'
                    renew_upgrade_data['Max_Tier'] = 'No'
                    next_category = tier_id[tier_list_id[prev_category] + 1]
                    renew_upgrade_data['next_category'] = next_category
                    renew_upgrade_data['req_for_upgrade_t'] = round(
                        tier_value_total[next_category] - float(cur_total_sale), 3)
                    renew_upgrade_data['req_for_upgrade_t_sp'] = round(
                        tier_value_total_sp[next_category] - float(cur_total_sale_sp), 3)

            if prev_category == 'Platinum':
                renew_upgrade_data['req_for_renew_t'] = round(tier_value_total['Platinum'] - float(cur_total_sale), 3)
                renew_upgrade_data['req_for_renew_t_sp'] = round(
                    tier_value_total_sp['Platinum'] - float(cur_total_sale_sp), 3)
            elif prev_category == 'Gold':
                renew_upgrade_data['req_for_renew_t'] = round(tier_value_total['Gold'] - float(cur_total_sale), 3)
                renew_upgrade_data['req_for_renew_t_sp'] = round(tier_value_total_sp['Gold'] - float(cur_total_sale_sp),
                                                                 3)
            elif prev_category == 'Silver':
                renew_upgrade_data['req_for_renew_t'] = round(tier_value_total['Silver'] - float(cur_total_sale), 3)
                renew_upgrade_data['req_for_renew_t_sp'] = round(
                    tier_value_total_sp['Silver'] - float(cur_total_sale_sp), 3)
            elif prev_category == 'Base':
                renew_upgrade_data['req_for_renew_t'] = 0
                renew_upgrade_data['req_for_renew_t_sp'] = 0

            # print(renew_upgrade_data)
        finally:
            cursor.close()
            conn.close()
            # print(member_data)
            # Show the profile page with account info
            return render_template('account_details.html',
                                   prev_category=prev_category, renew_upgrade_data=renew_upgrade_data,
                                   cur_fy_data=cur_fy_data, prev_fy_data=prev_fy_data,
                                   account=account, fullname=session['fullname'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# API Configuration
@app.route('/api/get_data', methods=['GET'])
def fetch_data():
    requested_api = request.headers.get('API-Key')
    # print(requested_api)
    query = request.headers.get('Query')
    # print(query)
    log_info(api_logger, requested_api, 'GET', query)
    result = process_request('read', requested_api, query)
    # print(result)
    return result


@app.route('/api/insert_data', methods=['POST'])
def insert_data():
    requested_api = request.headers.get('API-Key')
    # print(requested_api)
    query = request.get_json().get('query')
    # print(query)
    log_info(api_logger, requested_api, 'POST', query)
    result = process_request('write', requested_api, query)
    return result


def process_request(required_role, requested_api, query):
    if requested_api not in api_keys:
        return jsonify({'message': 'Invalid API Key.'}), 401

    api_role = api_keys[requested_api]
    if required_role not in api_role.split('_'):
        return jsonify({'message': 'Insufficient permissions for this API Key.'}), 403

    current_time = time.time()
    last_requested_time = api_request_time.get(requested_api, 0)

    if current_time - last_requested_time < request_limit:
        return jsonify({'message': 'Too many requests. Please try again after some time.'}), 429

    api_request_time[requested_api] = current_time

    result = query_execute.execute_query(query, required_role)
    return result


def log_info(logger, api_key, method, query):
    log_message = f"API Key: {api_key}, Method: {method}, Query: {query}"
    logger.info(log_message)



@app.errorhandler(Exception)
def handle_error(error):
    error_message = f"An error occurred: {str(error)}"
    app.logger.error(f"{session}: Timestamp: {datetime.now()} Url: {request.url} Error: {error_message}")
    return error_message, 500


logger = logging.getLogger(__name__)



@app.route('/requisition')
def requisition():
    return render_template('requistion_form.html')

# @app.route('/requisition', methods=['GET', 'POST'])
# def requisition():
#     if request.method == 'POST':
#         # Process form data here
#         return render_template('thank_you_req.html', message="Form submitted successfully!")
#     return render_template('requistion_form.html')


@app.route('/add_shade_card', methods=['POST'])
            
def add_shade_card():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    data = request.form
    username = session['username']
    fullname = session['fullname']
    
    item_names = data.getlist('shade_item[]')  
    item_quantities = data.getlist('shade_qty[]')  

   
    item_column_mapping = {
        'Aluwall': 'aluwall_qty',
        'MSC_Regular': 'msc_regular_qty',
        'MSC_Special': 'msc_special_qty',
        'AL45': 'al45_qty',
        'Wabi_Sabi_Swatch': 'wabi_sabi_swatch_qty',
        'CCP_ZCP': 'ccp_zcp_qty',
        'Aludecor_Systems': 'aludecor_system_qty',
        'Elevate': 'elevate_qty',
        'Signex': 'signex_qty',
        'Final_Aluminum_Titanium_Catalogue': 'final_aluminum_titanium_catalogue_qty',
        'Final_Metal_Dhara_Lovers_Catalogue': 'final_metal_dhara_lovers_catalogue_qty',
        'Wabi_Sabi_premium':'wabi_sabi_premium_qty',
        'SAND_RUSTIC' :'sand_rustic_qty',
        'Corporate_Profile':'corporate_profile_qty',
        'Why_Aludecor_(English)': 'why_aludecor_english_qty',
        'Why_Aludecor_(Hindi)': 'why_aludecor_hindi_qty',
        'Why_Aludecor_(Tamil)': 'why_aludecor_tamil_qty',
        'Final/Ace/Timber_Combined_Catalogue' :'final_ace_timber_combined_catalogue_qty',
        'Final/3_MM_CLASSIQUE_Catalogue':'final_3_mm_classique_catalogue_qty',
        'Final/4_MM_ENDURA_Catalogue': 'final_4_mm_endura_catalogue_qty',
        'Aludecor_Hanging' :'aludecor_hanging_qty',
        'Aluwall_Hanging': 'aluwall_Hanging',
        'AG+Armor':'ag_armor_qty',
        'Nepal_Regular':'nepal_regular_qty',
        'Nedzink_solid_panel_Brochure':'nedzink_solid_panel_brochure_qty',
        'Nedzink_Catalogue_Nuance':'nedzink_catalogue_nuance',
        'NedZink_Catalogue_NATUREL_NEO_NOIR':'nedzink_catalogue_nature_neo_noir_qty',
        'Vi-Secure':'vi_secure_qty',
        'ZINCHO_Catalogue':'zinco_catalogue_qty',
        'Final_Rugged_Metal_Catalogue':'final_rugged_metal_catalogue_qty',
        'Nexcomb_Brochure':'nexcomb_brochure_qty',
        'Aluwall_Relic':'aluwall_relic_qty',
        'Shades_of_the_Year':'shades_of_the_year_qty',
        'earth_coat': 'earth_coat'


    }

    timestamp = datetime.now()
    columns = ['timestamp', 'username', 'fullname'] + list(item_column_mapping.values())
    values = [ timestamp, username, fullname] + [None] * (len(columns) - 3)

    
    for item, qty in zip(item_names, item_quantities):
        db_column = item_column_mapping.get(item)
        if db_column:
            index = columns.index(db_column)
            values[index] = qty  

    
    query = f"""INSERT INTO dealer_db.shade_cards ({', '.join(columns)}) 
                VALUES ({', '.join(['%s'] * len(values))})"""

    
    print("Query:", query)
    print("Values:", values)

    try:
        

              
        
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        # conn.close()
        return render_template('thank_you_req.html')
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/add_visiting_card', methods=['POST'])
def add_visiting_card():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    data = request.form
    username = session['username']
    fullname = session['fullname']
    query = "INSERT INTO visiting_cards (username, fullname, visiting_qty, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
    values = (username, fullname, data.get('visiting_qty'))
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        return render_template('thank_you_req.html')
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 3002), app, log=logger)
    # http_server.serve_forever()
    app.run(debug=False, host='0.0.0.0', port=4002)
