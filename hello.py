import json
from flask import (
    Flask,
    request,
    redirect,
    send_from_directory
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    UserMixin,
    AnonymousUserMixin,
    logout_user,
    current_user
)
from typing import Union
from cache import Cache

from functions import (
    render,
    LoginForm,
    get_profile_type)

# << STATR APP CONFIGURATION >>

app = Flask(__name__,
            template_folder='website/website/src_html',
            static_folder='website/website/static')
cache = Cache(app)


app.config['SECRET_KEY'] = "jnksdckj787887we8hbbjwdKJ8J"

login_manager = LoginManager()
login_manager.init_app(app)

servo_value = 0


@login_manager.user_loader
def load_user(user_id):
    data = cache.get(f"user_{user_id}")
    if not data:
        return AnonymousUserMixin()
    return User(data)


class User(UserMixin):
    def __init__(self, text_or_dict: Union[dict, str]):
        super().__init__()
        if type(text_or_dict) == str:
            self._data = json.loads(text_or_dict)
        else:
            self._data = text_or_dict
        self._store()

    def __getattr__(self, key):
        return self._data[key]

    def __repr__(self):
        d = self._data.copy()
        return json.dumps(d)

    def __setattr__(self, key: str, value):
        if key == "_data":
            return super(User, self).__setattr__(key, value)
        raise Exception("Cannot set attribute to User")

    def _store(self):
        cache.set(f"user_{self.id}", str(self))


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():  # CHANGE
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        hashed_pass = request.form['password']
        user_data = {"is_error": 0, "user_id": 1, "name": "nm_01"}
        if (not user_data["is_error"]) and \
                (username == "st2257") and \
                (hashed_pass == "st_pass"):
            user = User({
                "id": user_data["user_id"],
                "name": user_data["name"]})
            login_user(user)
            return redirect('/account')
        return render('authorization/index.html',
                      form=form,
                      auth_result="Wrong password or username!")
    return render('authorization/index.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if get_profile_type(current_user) != 0:
        print(f"{current_user.username} tried to reg: "
              f"{get_profile_type(current_user)}")
        return redirect("/logout", code=302)

    if request.method == 'POST':
        filter_dict = dict(request.form)
        password = request.form['password']
        if password != request.form['confirmed_password']:
            return render('registration/index.html',
                          prev_form=dict(request.form),
                          processed_text='Пароли не совпадают')
        hashed_password = password
        filter_dict["hashed_password"] = str(hashed_password)
        filter_dict["profile_type_id"] = 1
        try:
            return redirect('/authorization')
        except Exception as e:
            return render('website/registration/index.html',
                          prev_form=dict(request.form),
                          processed_text=str(e))
    return render('registration/index.html')


@app.route("/account", methods=['GET', 'POST'])
def account():
    try:
        if current_user.id != 0:
            pass
    except Exception:
        return render("account/anonim.html")
    print(f"{current_user.id}")
    return render('account/index.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# << END APP CONFIGURATION >>


@app.route("/")
def index():
    return render('index.html')


@app.route("/about")
def about():
    return render('about/index.html')


@app.route("/functions")
def functions():
    return render('functions/index.html')


@app.route("/new_page")
def new_page():
    return render('new_page/index.html')


@app.route("/url_request/<value>", methods=['GET', 'POST'])
def url_request(value):
    res_value = value
    response = {}
    response["data"] = res_value

    if res_value == "time":
        f = open('website/static/log_test.txt', 'r')
        response["data"] = f.read()
        #print(datetime.now()-now)
        f.close()
    return response


@app.route("/function/servo", methods=['GET', 'POST'])
def servo():
    global servo_value
    if request.method == 'POST':
        filter_dict = dict(request.form)
        post_type = request.form['post_type']
        if post_type == "set_servo":
            value = request.form['value']
            servo_value = value
            print(f"Servo value setted:{value}")
    return str(servo_value)


@app.route("/function/get_servo", methods=['GET', 'POST'])
def get_servo():
    global servo_value
    return str(servo_value)


@application.route("/sound_get/<data_id>/<data>",
                   methods=['GET', 'POST'])
def sound_get(data_id, data):
    try:
        data_id = data_id[1:]
        data = data[1:]
        print(f"Cathced:    <data_id:{data_id}> <data:{data}>")
        return "1"
    except Exception as e:
        return f"Exception: {str(e)}"


def create_app():
   return app
#if __name__ == "__main__":
#    app.run(debug=True)


#from flask import Flask

#application = Flask(__name__)


#@application.route("/")
#def hello():
#   return "<h1 style='color:blue'>Hello There!</h1>"

#def create_app():
#   return application


#if __name__ == "__main__":
#   from waitress import serve
#   serve(app, host="31.31.198.114", port=8080)
#   #application.run(host='31.31.198.114')
