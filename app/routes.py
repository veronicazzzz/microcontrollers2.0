from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import User, Info
from . import forms
from . import app, db


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.Login()

    if current_user.is_authenticated:
        return redirect(url_for('main'))

    if request.method == 'POST' and form.validate_on_submit():
        login, password = form.data['login'], form.data['password']
        
        user = db.session.query(User).filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Incorrect login or password')
    else:
        flash('Fiil login and password')

    return render_template('index.html', form=form)


@app.route('/main')
@login_required
def main():
    return render_template('main.html')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    q = db.session.query(Info).all()

    d = dict(
        id_ = [elem.id for elem in q],
        temp = [elem.temp for elem in q],
        co = [elem.co for elem in q],
        smoke = [elem.smoke for elem in q],
        humidity = [elem.humidity for elem in q],
        time = [elem.time for elem in q],
    )

    return jsonify(d)

@app.route('/table')
@login_required
def table():
    data = db.session.query(Info).all()
    
    return render_template('table.html', data=data)

@app.route('/updatedb', methods=['GET', 'POST'])
@login_required
def get_table():
    if request.method == 'POST':
        delete = request.form.get('delete')
        field = request.form.get('field')
        value = request.form.get('value')
        editid = request.form.get('id')

        record = db.session.query(Info).filter_by(id=editid).first()
        
        if delete:
            db.session.delete(record)
        else:
            if field == 'temp':
                record.temp = value
            if field == 'humidity':
                record.humidity = value
            if field == 'smoke':
                record.smoke = value
            if field == 'co':
                record.co = value

        db.session.commit()

        success = 1

    return jsonify(success)


@app.route('/getlast')
@login_required
def get_last():
    obj =  db.session.query(Info).order_by(Info.id.desc()).first()
    return  jsonify({
        'temp': obj.temp,
        'humidity': obj.humidity,
        'smoke': obj.smoke,
        'co': obj.co
    })


@app.route('/getdata')
@login_required
def get_data():
    db.session.add(Info(**request.args))
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('index'))

    return response