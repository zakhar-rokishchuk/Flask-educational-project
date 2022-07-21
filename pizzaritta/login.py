from flask import Blueprint, render_template, request, redirect, url_for


login = Blueprint('login', __name__, template_folder='templates')


@login.route('/login')
def login_page():
    return render_template('login.html')


@login.route('/log-in', methods=['POST'])
def login_form():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin_products.admin_products_list'))
    return render_template('login.html', error=error)