import json
import random
import smtplib
from email.message import EmailMessage
import bcrypt
import requests
from flask import Flask, jsonify, make_response, request, render_template
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

mysql = mysql.connector.connect(
    host= os.environ.get('MYSQL_HOST_NAME'),
    user= os.environ.get('MYSQL_USER_DATABASE'),
    password= os.environ.get('MYSQL_PASSWORD'),
    database= os.environ.get('MYSQL_USER_DATABASE'),
    port=3306
)

app.secret_key = "ComputeGPT-abhi-2023"


def convert(s):
    math_symbols = {
        '+': 'plus',
        '-': 'minus',
        '×': 'multiplied by',
        '*': 'multiplied by',
        '÷': 'divided by',
        '/': 'divided by',
        '=': 'is equal to',
        '<': 'is smaller than',
        '>': 'is larger than',
        '≤': 'is smaller than or equal to',
        '≥': 'is larger than or equal to',
        '^': 'raised to the power of',
        '√': 'square root of',
        '%': 'percent',
        '|x|': 'absolute value of x',
        'π': 'Pi',
        '∞': 'Infinity',
        '∑': 'Summation',
        'Δ': 'Delta or Change',
        '∫': 'Integral of',
        'd/dx': 'Derivative with respect to x',
        '!': 'Factorial',
        '≠': 'Not equal to',
        '≈': 'Approximately equal to',
        '∝': 'Proportional to',
        '∥': 'Perpendicular to',
        '⊆': 'Subset of',
        '⊇': 'Superset of',
        '||': 'Parallel to',
        '∩': 'Intersection of sets',
        '∪': 'Union of sets',
        '∧': 'Logical AND operation',
        '∨': 'Logical OR operation',
        '∼': 'Logical NOT operation',
        '¬': 'Logical NOT operation',
        '∀': 'For all or Universal quantifier',
        '∃': 'There exists or Existential quantifier',
        '∮': 'Closed line integral'
    }
    for i in s:
        if i in math_symbols:
            s = s.replace(i, math_symbols[i])

    return s


@app.route('/wolfram-step-by-step', methods=['POST', 'GET'])  # GENERATE STEP-BY-STEP SOLUTION
def wolfram_step_by_step():
    app_id = os.environ.get('WOLFRAM_STEPS_KEY')
    data = request.get_json()
    res_query = data.get('query')

    query = convert(res_query)

    width = data.get('width')  # 500 pixels
    maxwidth = data.get('maxWidth')  # 500 pixels
    plotwidth = data.get('plotWidth')
    mag = data.get('mag')  # 1.00
    units = data.get('units')

    # Construct the URL
    url = f'http://api.wolframalpha.com/v2/query?appid={app_id}&input={query}&podstate=Result__Step-by-step+solution&units={units}&width={width}&maxwidth={maxwidth}&plotwidth={plotwidth}&mag={mag}'

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Set the content type as image/jpeg
            print(response.content)
            headers = {'Content-Type': 'image/jpeg'}
            # Create a response with the image content
            # with open('wolfram_image.jpg', 'wb') as f:
            #     f.write(response.content)
            # print(response.content)
            return make_response(response.content, 200, headers)
        else:
            return {'success': True, 'response': 'I cannot understand your input...'}
    except Exception as e:
        print("Exception")


@app.route('/wolfram-conversation', methods=['POST', 'GET'])  # CONVERSE WITH IT LIKE A BOT
def wolfram_conversation():
    app_id = os.environ.get('WOLFRAM_CONVERSATION_KEY')
    data = request.get_json()
    res_query = data.get('query')
    query = convert(res_query)
    conversationid = data.get('conversationID')

    # Construct the URL
    if conversationid == '':
        url = f'http://api.wolframalpha.com/v1/conversation.jsp?appid={app_id}&i={query}&output=json'
    else:
        url = f'https://www6b3.wolframalpha.com/api/v1/conversation.jsp?appid={app_id}&conversationid={conversationid}&i={query}'

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            print(response.content)
            botText = json.dumps(json.loads(response.content.decode('utf-8')), indent=4)
            return {'success': True, 'response': botText}
        else:
            print(response.content)
            return {'success': True, 'response': 'I cannot understand your input...'}
    except Exception as e:
        print("Exception")


@app.route('/wolfram-LLM', methods=['POST', 'GET'])  # GENERATE A SINGLE LONG ANSWER LIKE CHATGPT
def wolfram_llm():
    app_id = os.environ.get('WOLFRAM_LLM_KEY')
    data = request.get_json()
    res_query = data.get('query')
    query = convert(res_query)

    # Modifyable
    maxchars = data.get('maxChars')  # at most 6800
    width = data.get('width')  # 500 pixels
    maxwidth = data.get('maxWidth')  # 500 pixels
    plotwidth = data.get('plotWidth')  # 200 pixels
    mag = data.get('mag')  # 1.00
    units = data.get('units')  # "metric", "nonmetric"     Chosen based on caller's IP address

    # Construct the URL
    url = f'http://api.wolframalpha.com/v2/query?input={query}&appid={app_id}&maxchars={maxchars}&units={units}&width={width}&maxwidth={maxwidth}&plotwidth={plotwidth}&mag={mag}&format=image'

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            print(response.content)
            return make_response(response.content, 200)
        else:
            print(response.content)
    except Exception as e:
        print("Exception")


@app.route('/wolfram-Speech', methods=['POST', 'GET'])  # Voice features
def wolfram_speech():
    app_id = os.environ.get('WOLFRAM_SPEECH_KEY')
    data = request.get_json()
    res_query = data.get('query')

    query = convert(res_query)

    # Construct the URL
    url = f'http://api.wolframalpha.com/v1/spoken?&appid={app_id}&i={query}'

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            print(response.content)
            return jsonify({'success': True, 'response': str(response.content)})
        else:
            print(response.content)
            return {'success': True, 'response': 'I cannot understand your input...'}
    except Exception as e:
        print(e)


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        data = request.get_json()

        cursor = mysql.cursor(dictionary=True)
        cursor.execute("INSERT INTO `feedbacks`(`email`, `feedback`) VALUES (%s, %s)",
                       (data.get('email'), data.get('feedback'),))
        mysql.commit()
        cursor.close()

        return jsonify({'success': True})

    if request.method == 'GET':
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `feedbacks`")
        feedback_data = cursor.fetchall()
        mysql.commit()
        cursor.close()

        return jsonify({'success': True, 'data': feedback_data})


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (data.get('email'),))
        user = cursor.fetchone()
        mysql.commit()
        cursor.close()

        if user:
            error = 'Email address already in use. Please use a different email address.'
            return jsonify({'success': False, 'message': error})
        else:
            msg = EmailMessage()

            # alphabet = string.ascii_letters + string.digits
            otp = random.randint(100000, 999999)
            print(otp)

            cursor = mysql.cursor(dictionary=True)
            cursor.execute("INSERT INTO `otp`(`mail`, `otp`) VALUES (%s, %s)", (data.get('email'), otp,))
            mysql.commit()
            cursor.close()

            msg["Subject"] = "ComputeGPT Verification"
            msg["From"] = "storycircle123@gmail.com"
            msg["To"] = data.get('email')

            html_content = render_template('email.html', name=data.get('name'), otp=otp)
            msg.set_content(html_content, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('storycircle123@gmail.com', 'njoexkbwuscrwdhf')
                smtp.send_message(msg)

            return jsonify({'success': True})


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        data = request.get_json()
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT `otp` FROM `otp` WHERE `mail`=%s ORDER BY `id` DESC LIMIT 1", (data.get('email'),))
        system_otp = cursor.fetchone()
        mysql.commit()
        cursor.close()

        if system_otp['otp'] == data.get('otp'):
            cursor = mysql.cursor(dictionary=True)
            password = data.get('password').encode('utf-8')
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
            cursor.execute("INSERT INTO `users` (`name`, `email`, `password`) VALUES (%s, %s, %s)",
                           (data.get('name'), data.get('email'), hash_password,))
            mysql.commit()
            cursor.close()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('username')
        password = data.get('password').encode('utf-8')

        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `users` WHERE email=%s", (email,))
        user = cursor.fetchone()
        mysql.commit()
        cursor.close()

        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                cursor = mysql.cursor(dictionary=True)
                cursor.execute("INSERT INTO `session`(`id`, `name`, `email`) VALUES (%s, %s, %s)",
                               (user['id'], user['name'], user['email'],))
                mysql.commit()
                cursor.close()

                return jsonify({'login': True, 'message': 'Valid User Login', 'id': user['id'],
                                'name': user['name'], 'email': user['email']})

            else:
                return jsonify({'login': False, 'message': 'Invalid Password'})
        else:
            return jsonify({'login': False})


@app.route('/logincheck', methods=['POST'])
def checklogin():
    # print(session)
    data = request.get_json()
    print(data)

    if data.get('email') == 'Meow':
        return jsonify({'login': False})

    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT `id`, `name`, `email` FROM `session` WHERE `email`= %s ORDER BY `index` DESC LIMIT 1;",
                   (data.get('email'),))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({'login': True, 'message': 'Valid User Login', 'id': user['id'],
                        'name': user['name'], 'email': user['email']})

    else:
        return jsonify({'login': False})


@app.route('/forgot', methods=['POST'])
def forgot():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (data.get('username'),))
        user = cursor.fetchone()
        mysql.commit()

        if user:
            msg = EmailMessage()

            otp = random.randint(100000, 999999)

            cursor = mysql.cursor(dictionary=True)
            cursor.execute("INSERT INTO `otp`(`mail`, `otp`) VALUES (%s, %s)", (data.get('username'), otp,))
            mysql.commit()
            cursor.close()

            msg["Subject"] = "ComputeGPT Verification"
            msg["From"] = "storycircle123@gmail.com"
            msg["To"] = data.get('username')

            html_content = render_template('pass.html', name=user['name'], otp=otp)
            msg.set_content(html_content, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('storycircle123@gmail.com', 'njoexkbwuscrwdhf')
                smtp.send_message(msg)

            return jsonify({'success': True})
        else:
            error = 'No such User found. Please Register first.'
            return jsonify(error)


@app.route('/verifyforgot', methods=['POST'])
def verifyforgot():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT `otp` FROM `otp` WHERE `mail`=%s ORDER BY `id` DESC LIMIT 1;", (data.get('username'),))
        system_otp = cursor.fetchone()
        print(system_otp['otp'])
        mysql.commit()
        cursor.close()

        if str(system_otp['otp']) == data.get('otp'):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})


@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password').encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("UPDATE `users` SET `password`= %s WHERE `email`= %s", (hash_password, data.get('username'),))
        mysql.commit()
        cursor.close()
        return jsonify({'success': True})


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("DELETE FROM `session` WHERE `email` = %s ;", (data.get('email'),))
    mysql.commit()
    cursor.close()
    return jsonify({'logout': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
