import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
app.app_context().push()
csrf = CSRFProtect(app)


# Модель продавцов
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)


# Модель товаров
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)


# Модель сделок
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'purchase' or 'sale'


# Создаем таблицы
db.create_all()
seller = db.relationship('Seller', backref=db.backref('transactions', lazy=True))
product = db.relationship('Product', backref=db.backref('transactions', lazy=True))


# Роуты для отображения данных и взаимодействия с приложением
@app.route('/')
def index():
    total_sellers = Seller.query.count()
    total_transactions = Transaction.query.count()
    total_products = Product.query.count()
    total_units = db.session.query(db.func.sum(Product.quantity)).scalar()
    return render_template('index.html', total_sellers=total_sellers,
                           total_transactions=total_transactions,
                           total_products=total_products, total_units=total_units)


# Добавление продавца
# Роут для управления продавцами
@app.route('/manage_sellers', methods=['GET'])
def manage_sellers():
    sellers = Seller.query.all()
    return render_template('manage_sellers.html', sellers=sellers)


# Роут для добавления нового продавца
@app.route('/manage_sellers/add', methods=['POST'])
def manage_sellers_add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_seller = Seller(first_name=first_name, last_name=last_name)
        db.session.add(new_seller)
        db.session.commit()
    return redirect(url_for('manage_sellers'))


# Роут для редактирования продавца
@app.route('/manage_sellers/edit/<int:seller_id>', methods=['GET', 'POST'])
def manage_sellers_edit(seller_id):
    seller = Seller.query.get(seller_id)

    if not seller:
        print(404)  # Вернуть 404, если продавец не найден

    if request.method == 'POST':
        # Получение данных из формы
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Проверка данных перед обновлением
        if first_name and last_name:
            # Обновление данных и сохранение в базе данных
            seller.first_name = first_name
            seller.last_name = last_name
            db.session.commit()

            # Перенаправление на страницу управления продавцами
            return redirect(url_for('manage_sellers'))

    # Если запрос не POST, отобразить страницу редактирования существующего продавца
    sellers = Seller.query.all()
    return render_template('manage_sellers.html', sellers=sellers, editing_seller=seller)


# Роут для удаления продавца
@app.route('/manage_sellers/delete/<int:seller_id>')
def manage_sellers_delete(seller_id):
    seller = Seller.query.get(seller_id)
    db.session.delete(seller)
    db.session.commit()
    return redirect(url_for('manage_sellers'))


# Добавление товара
@app.route('/warehouse', methods=['GET'])
def warehouse():
    products = Product.query.all()
    for product in products:
        if product.image:
            product.image_base64 = base64.b64encode(product.image).decode('utf-8')
    return render_template('warehouse.html', products=products)


# Роут для добавления нового товара на странице "Склад"
@app.route('/warehouse/add', methods=['POST'])
def warehouse_add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        image = request.files['image'].read() if 'image' in request.files else None
        new_product = Product(name=name, quantity=quantity, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()
    return redirect(url_for('warehouse'))


# Роут для отображения страницы редактирования товара
@app.route('/warehouse/edit/<int:product_id>')
def edit_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product.image_base64 = base64.b64encode(product.image).decode('utf-8') if product.image else None
        return render_template('edit_product.html', editing_product=product)
    else:
        return "Product not found", 404


# Роут для обновления товара
@app.route('/update_product', methods=['POST'])
def update_product():
    product_id = request.form.get('productId')
    name = request.form.get('name')
    new_image = request.files.get('newImage')
    quantity = int(request.form.get('quantity', 0))  # Преобразование в целое число, по умолчанию 0
    price = float(request.form.get('price', 0.0))  # Преобразование в число с плавающей точкой, по умолчанию 0.0
    product = Product.query.get(product_id)
    print(price)
    print()
    print(quantity)
    if product:
        product.name = name
        product.quantity = quantity
        product.price = price

        if new_image:
            product.image = new_image.read()

        db.session.commit()
        return "Product updated successfully", 200
    else:
        return "Product not found", 404


# Роут для удаления товара на странице "Склад"
@app.route('/warehouse/delete/<int:product_id>')
def warehouse_delete(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('warehouse'))


# Покупка или продажа товара
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        try:
            seller_id = int(request.form['seller_id'])
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
            transaction_type = request.form['transaction_type']

            # Уменьшаем количество товара при продаже
            if transaction_type == 'sale':
                product = Product.query.get(product_id)
                if product.quantity < quantity:
                    return "Недостаточно товара на складе"

                product.quantity -= quantity

            # Добавляем запись о сделке
            new_transaction = Transaction(
                seller_id=seller_id, product_id=product_id, quantity=quantity,
                transaction_type=transaction_type
            )
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('index'))

        except ValueError:
            return "Некорректные данные в форме"

        except NoResultFound:
            return "Продавец или продукт не найден"

    transactions = Transaction.query.all()
    products_info = {product.id: product.name for product in Product.query.all()}

    # Дополнительный запрос для получения имени продавца
    sellers_info = {seller.id: f"{seller.first_name} {seller.last_name}" for seller in Seller.query.all()}

    sellers = Seller.query.all()
    products = Product.query.all()

    return render_template(
        'transaction.html', sellers=sellers, products=products,
        transactions=transactions, sellers_info=sellers_info, products_info=products_info
    )


if __name__ == '__main__':
    app.run(debug=False)
