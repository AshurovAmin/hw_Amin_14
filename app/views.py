from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import User, Transaction, UserMixin
from .forms import UserLoginForm, UserRegisterForm, TransactionsForm, TransactionsUpdateForm


def index():
    transactions = Transaction.query.all()
    return render_template('transactions_view.html', transactions=transactions)

@login_required
def transactions_add():
    form = TransactionsForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_transactions = Transaction(
                period=form.period.data,
                value=form.value.data,
                status=form.status.data,
                unit=form.unit.data,
                subject=form.subject.data
            )
            db.session.add(new_transactions)
            db.session.commit()
            flash('Транзакция успешно добавлена', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении транзакции произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('transactions_add.html', form=form)

@login_required
def admin_transactions_update(transactions_id):
    transactions = Transaction.query.get(transactions_id)
    form = TransactionsUpdateForm(meta={'csrf': False}, obj=transactions)
    if request.method == 'POST':
        form.populate_obj(transactions)
        db.session.add(transactions)
        db.session.commit()
        flash('Транзакция успешно обновлена', 'Успешно!')
        return redirect(url_for('index'))
    else:
        print(form.errors)
        text_list = []
        for field, errors in form.errors.items():
            text_list.append(f'{field} : {", ".join(errors)}')
        flash(f'При обновлении транзакции произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('transactions_add.html', form=form)

@login_required
def admin_transactions_delete(transactions_id):
    transactions = Transaction.query.get(transactions_id)
    if request.method == 'POST':
        db.session.delete(transactions)
        db.session.commit()
        flash('Транзакция успешно удалена', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('transactions_delete.html', transactions=transactions)


def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован!', 'success!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка{". ".join(text_list)}', 'Ошибка!')

    return render_template('accounts/index.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему, Успех!')
                return redirect(url_for('index'))
            else:
                flash('Неверные логин и пароль', 'Ошибка!')
    return render_template('accounts/index.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

