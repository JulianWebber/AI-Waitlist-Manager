from flask import render_template, request, jsonify, url_for, redirect
from app import app, db
from models import WaitlistUser
from flask_mail import Mail, Message
import os

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')

    if not full_name or not email:
        return jsonify({'success': False, 'message': 'Full name and email are required'}), 400

    existing_user = WaitlistUser.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already registered'}), 400

    new_user = WaitlistUser(full_name=full_name, email=email)
    db.session.add(new_user)
    db.session.commit()

    verification_url = url_for('verify_email', token=new_user.verification_token, _external=True)
    msg = Message('Verify your email for AI Startup Waitlist',
                  recipients=[new_user.email])
    msg.body = f'Please click the following link to verify your email: {verification_url}'
    mail.send(msg)

    print(f"Verification email sent to {new_user.email} with token: {new_user.verification_token}")

    return jsonify({'success': True, 'message': 'Successfully registered! Please check your email to verify your address.'}), 201

@app.route('/verify/<token>')
def verify_email(token):
    user = WaitlistUser.query.filter_by(verification_token=token).first()
    if user:
        if not user.is_verified:
            user.is_verified = True
            db.session.commit()
            print(f"User {user.email} has been verified.")
        return render_template('verified.html')
    return render_template('invalid_token.html')

@app.route('/dashboard')
def dashboard():
    # This is a protected route that only verified users should access
    # In a real application, you'd use a login system. For this example, we'll use a dummy user.
    user = WaitlistUser.query.first()
    if user and user.is_verified:
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('index'))
