from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Product, User

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('main.register'))

        # Tambahkan pengguna ke database
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cari pengguna berdasarkan username
        user = User.query.filter_by(username=username).first()

        # Verifikasi password
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('main.view_products'))  # Ganti dengan view_products
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')



@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


@main.route('/')
@login_required
def index():
    return redirect(url_for('main.view_products'))  # Mengarahkan ke halaman produk

@main.route('/products', methods=['GET'])
@login_required
def view_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = int(request.form['jumlah'])
        harga = float(request.form['harga'])
        product = Product(nama=nama, jumlah=jumlah, harga=harga)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.view_products'))  # Ganti dengan view_products
    return render_template('add_product.html')


@main.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.nama = request.form['nama']
        product.jumlah = int(request.form['jumlah'])
        product.harga = float(request.form['harga'])
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.view_products'))
    return render_template('edit_product.html', product=product)

@main.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('main.view_products'))
