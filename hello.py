import json
import numpy as np
from flask import (
    Flask,
    request,
    redirect,
    send_file,
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
import os
import threading
import time

from functions import (
    render,
    LoginForm,
    get_profile_type,
    Soldier,
    Battlefield)

from functions_db import (
    db_add_log, 
    db_add_device,
    db_add_user,
    check_logs,
    check_devices,
    check_users,
    db_change_value,
    db_find_devices,
    check_data,
    db_add_user_data,
    db_get_user_joystick,
    db_get_user_sensor,
    db_update_sensor_data)
#db_get_user_joystick)

# << STATR APP CONFIGURATION >>

app = Flask(__name__,
            template_folder='website/website/src_html',
            static_folder='website/website/static')
cache = Cache(app)


app.config['SECRET_KEY'] = "jnksdckj787887we8hbbjwdKJ8J"

login_manager = LoginManager()
login_manager.init_app(app)

servo_value = 0

###         BF           ###

BF = Battlefield(30, 30)

BF.add_soldier(Soldier(0, 1, s_id=0))
BF.add_soldier(Soldier(2, 1, s_id=1))
BF.add_soldier(Soldier(4, 1, s_id=2))
BF.add_soldier(Soldier(6, 1, s_id=3))
BF.add_soldier(Soldier(8, 1, s_id=4))
BF.add_soldier(Soldier(0, 10, s_id=5))
BF.add_soldier(Soldier(2, 10, s_id=6))
BF.add_soldier(Soldier(4, 10, s_id=7))
BF.add_soldier(Soldier(6, 10, s_id=8))
BF.add_soldier(Soldier(8, 10, s_id=9))

###         BF           ###




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
    try:
        if current_user.id != 0:
            pass
    except Exception:
        return "Login please!"
    print(db_find_devices(current_user.id+1))
    return render('functions/index.html',
                  devices = db_find_devices(current_user.id+1),
                  u_id = current_user.id)


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


### << ADD DEVICE >> ###
@app.route("/add_device", methods=['GET', 'POST'])
def add_device():
    return render('add_device/index.html')


@app.route("/function/add_device", methods=['GET', 'POST'])
def add_device_func():
    if request.method == 'POST':
        filter_dict = dict(request.form)
        post_type = request.form['post_type']
        if post_type == "add_device":
            d_name = request.form['name']
            d_type = request.form['device_type']
            d_room = request.form['room']
            db_add_device(user_id = current_user.id+1,
                       d_name = d_name,
                       d_type = d_type,
                       d_room = d_room, 
                       value = 0)
            print(f"d_name:{d_name};d_type:{d_type};d_room:{d_room}")
            return render('add_device/index_res.html',
                          d_name=d_name,
                          d_type=d_type,
                          d_room=d_room)
    return "Здесь отобразится устройство после добавления"


@app.route("/functions/change_value/<d_id>/<d_value>", methods=['GET', 'POST'])
def change_value(d_id, d_value):
    device_id = int(d_id)
    device_value = int(d_value)
    new_value = 0
    if device_value == 1:
        new_value = 0
    else:
        new_value = 1

    db_change_value(current_user.id+1, device_id, new_value)

    return "res"


###  <<< GET VALUES >>>  ###
@app.route("/get_page/get_values/<user_id>", methods=['GET', 'POST'])
def get_page_values(user_id):
    return render('get_page/get_values.html',
                   devices = db_find_devices(user_id))


@app.route("/sound_get/<data_id>/<data>",
                   methods=['GET', 'POST'])
def sound_get(data_id, data):
    try:
        data_id = data_id[1:]
        data = data[1:]
        print(f"Cathced:    <data_id:{data_id}> <data:{data}>")
        return "1"
    except Exception as e:
        return f"Exception: {str(e)}"


@app.route("/functions/joystick", methods=['GET', 'POST'])
def joystick():
    if request.method == 'POST':
        filter_dict = dict(request.form)
        post_type = request.form['post_type']
        if post_type == "first_file":
            my_file = request.files['first_file']
            my_file.save(os.path.join("uploads", my_file.filename))
    return render('joystick/index.html')


@app.route("/functions/joystick/get/<user_id>", methods=['GET', 'POST'])
def joystick_get(user_id):
    res = db_get_user_joystick(user_id)
    data_str = ""
    for i in range(len(res)):
        data_str += (str(res[i]) + " ")
    return data_str


@app.route("/functions/sensors/get/<user_id>", methods=['GET', 'POST'])
def sensor_get(user_id):
    res = db_get_user_sensor(user_id)
    data_str = ""
    for i in range(len(res)):
        data_str += (str(res[i]) + " ")
    return data_str


@app.route("/functions/sensors/set_all/<user_id>/<gps_lat>/<gps_lng>/<a_x>/<a_y>/<a_z>/<bme_temp>/<bme_pres>/<bme_alt>/<bme_hid>", methods=['GET', 'POST'])
def sensors_set(user_id, gps_lat, gps_lng, a_x, a_y, a_z, bme_temp, bme_pres, bme_alt,  bme_hid):
    db_update_sensor_data(user_id, gps_lat, gps_lng, a_x, a_y, a_z, bme_temp, bme_pres, bme_alt,  bme_hid)
    return str(db_get_user_sensor(user_id))


@app.route("/functions/joystick/set/<user_id>/<j_x>/<j_y>/<c_1>/<c_2>/<c_3>/<c_4>", methods=['GET', 'POST'])
def joystick_set(user_id, j_x, j_y, c_1, c_2, c_3, c_4):
    db_add_user_data(user_id, j_x, j_y, c_1, c_2, c_3, c_4)
    return str(db_get_user_joystick(user_id))


@app.route("/upload_file", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filter_dict = dict(request.form)
        post_type = request.form['post_type']
        if post_type == "first_file":
            my_file = request.files['first_file']
            my_file.save(os.path.join("uploads", my_file.filename))
    return render('upload_file/index.html')


@app.route("/download_file/<file_name>/",
                   methods=['GET', 'POST'])
def download_file(file_name):
    try:
        return send_from_directory(f"uploads", file_name, as_attachment=True)
    except Exception as a:
        return f"Exception: {a}"



### <<< BF FIELD >>> ###


@app.route("/bf/show", methods=['GET', 'POST'])
def bf_show():
    o_arr = []
    for i in range(BF.x_l):
        for j in range(BF.y_l):
            for item in BF.soldier_field[i][j]:
                o_arr.append({"x": item.x, "y": item.y, "h": item.h})
    return render('battlefield/index.html',
                  o_arr=o_arr,
                  bf_set={"x": BF.x_l, "y": BF.y_l})


@app.route("/bf/move/<s_id>/<new_x>/<new_y>", methods=['GET', 'POST'])
def bf_move_soldier(s_id, new_x, new_y):
    BF.move_soldier(s_id, new_x, new_y)
    return "1"


@app.route("/bf/move/group/<new_x>/<new_y>/<id_arr>", methods=['GET', 'POST'])
def bf_move_group(new_x, new_y, id_arr):
    id_array = [int(item) for item in id_arr.split('_')]
    BF.move_group(new_x, new_y, id_array)
    return "1"


@app.route("/bf/get/<s_id>", methods=['GET', 'POST'])
def bf_get_soldier(s_id):
    return BF.get_soldier(s_id)


@app.route("/bf/get_100/<s_id>", methods=['GET', 'POST'])
def bf_get_100(s_id):
    return BF.get_100(s_id)



@app.route("/bf/fire/<s_id>/<aim_x>/<aim_y>", methods=['GET', 'POST'])
def bf_fire(s_id, aim_x, aim_y):
    BF.soldier_fire(s_id, aim_y, aim_x)
    return "1"


def update_bf(value):
    while 1:
        time.sleep(1)
        BF.time_step()


#def create_app():
#   return app
if __name__ == "__main__":
    download_thread = threading.Thread(target=update_bf, args=[0])
    download_thread.start()

    app.run(debug=True)


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
