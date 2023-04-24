import os
import datetime
from flask import Flask, url_for, render_template, request, redirect
from data import db_session
from data.users import User
from forms.cart import CartForm
from data.products import Product
from forms.users import RegisterForm
from forms.loginform import LoginForm
from forms.products import ProductsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

UPLOAD_FOLDER = '\static\img\products'

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    form = CartForm()
    if request.method == 'POST':
        product = db_sess.query(Product).get(request.form["id"])
        if product is not None:
            user = db_sess.query(User).get(current_user.get_id())
            user.cart += f"{str(product.id)}:{str(form.count.data)},"
            db_sess.commit()
            return redirect(url_for('shop'))
    return render_template('shop.html', products=products, form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ProductsForm()
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    if request.method == 'POST':
        product = Product(
            name=form.name.data,
            picture=form.picture.data.filename,
            price=form.price.data,
            discription=form.discription.data,
            tags=form.tags.data
        )
        db_sess.add(product)
        db_sess.commit()
        file = request.files['picture']
        file.save("static/img/products/" + file.filename)
        return redirect(url_for('admin'))
    return render_template('admin.html', form=form, products=products)


@app.route("/admin/delete/<id>", methods=["GET", "POST"])
def delete(id):
    db_sess = db_session.create_session()
    line = db_sess.query(Product).get(int(id))
    os.remove("static/img/products/" + line.picture)
    db_sess.delete(line)
    db_sess.commit()
    return redirect("/admin")


@app.route('/account', methods=['GET', 'POST'])
def account():
    db_sess, total, cart = db_session.create_session(), 0, []
    user = db_sess.query(User).get(current_user.get_id())
    for item in [item.split(":") for item in user.cart.split(",")]:
        if len(item) != 1:
            product = db_sess.query(Product).get(int(item[0]))
            total += product.price * int(item[1])
            cart.append([product.name, product.price, item[1]])
    if request.method == 'POST':
        user = db_sess.query(User).get(current_user.get_id())
        user.cart = ""
        db_sess.commit()
        return redirect(url_for("account"))
    return render_template('account.html', cart=cart, total=total)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают",
                                   links=[url_for('index'), url_for('shop'), url_for('account')])
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть",
                                   links=[url_for('index'), url_for('shop'), url_for('account')])
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/products.db")
    app.run()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    main()
    app.run(host='0.0.0.0', port=port)
