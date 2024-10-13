from flask import render_template, request, jsonify
from app import app, db
from models import WaitlistUser

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

    return jsonify({'success': True, 'message': 'Successfully registered for the waitlist!'}), 201
