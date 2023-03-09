from flask import render_template
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import (
    AnonymousUserMixin
)
import sqlite3
import datetime


def db_add_log(log_text):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = int(cur.execute("SELECT COUNT(*) FROM logs").fetchall()[0][0])
    cur.execute(f"""INSERT INTO logs VALUES ({res}, \"{log_text}\");""")

    con.commit()
    con.close()


def db_add_device(user_id, d_name, d_type, d_room, value):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = int(cur.execute("SELECT COUNT(*) FROM devices").fetchall()[0][0]) + 1
    cur.execute(f"INSERT INTO devices VALUES ({res}, {user_id}, \"{d_name}\", {d_type}, \"{d_room}\", {value});")

    con.commit()
    con.close()

def db_add_user(u_name, u_pass, u_type, u_tag):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = int(cur.execute("SELECT COUNT(*) FROM users").fetchall()[0][0]) + 1
    cur.execute(f"INSERT INTO users VALUES ({res}, \"{u_name}\", \"{u_pass}\", {u_type}, {u_tag});")

    con.commit()
    con.close()


def check_logs():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM logs")
    for item in res.fetchall():
        print(item)

    con.commit()
    con.close()


def check_devices():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM devices")
    for item in res.fetchall():
        print(item)

    con.commit()
    con.close()


def check_users():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM users")
    for item in res.fetchall():
        print(item)

    con.commit()
    con.close()


def db_change_value(user_id, device_id, new_value):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    print(user_id,device_id,new_value)
    cur.execute(f"UPDATE devices SET value = {new_value} WHERE device_id = {device_id} AND user_id = {user_id}")

    con.commit()
    con.close()


def db_find_devices(user_id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT * FROM devices WHERE user_id = {user_id}").fetchall()

    con.commit()
    con.close()
    return res


def db_get_user_joystick(user_id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    e = str(datetime.datetime.now())

    #cur.execute("DROP TABLE joystick_current_data")
    res = cur.execute(f"SELECT * FROM joystick_current_data WHERE user_id={user_id}").fetchall()[0]

    con.commit()
    con.close()
    return res

def db_add_user_data(user_id, joy_x=0, joy_y=0, check_1=0, check_2=0, check_3=0, check_4=0, text_field=""):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    e = str(datetime.datetime.now())

    #cur.execute(f"CREATE TABLE joystick_current_data (user_id int, joy_x int, joy_y int, check_1 int, check_2 int, check_3 int, check_4 int, text_field varchar(255));");
    res = int(cur.execute(f"SELECT COUNT(*) FROM joystick_data").fetchall()[0][0])
    cur.execute(f"INSERT INTO joystick_data VALUES ({res+1},{user_id},{joy_x},{joy_y},{check_1},{check_2},{check_3},{check_4},\"{text_field}\", \"{e}\");")
    cur.execute(f"UPDATE joystick_current_data SET user_id={user_id},joy_x={joy_x},joy_y={joy_y},check_1={check_1},check_2={check_2},check_3={check_3},check_4={check_4}  WHERE user_id = {user_id}")
    if (int(cur.execute(f"SELECT COUNT(*) FROM joystick_current_data WHERE user_id={user_id}").fetchall()[0][0]) == 0):
        cur.execute(f"INSERT INTO joystick_current_data VALUES ({user_id},{joy_x},{joy_y},{check_1},{check_2},{check_3},{check_4},\"{text_field}\");")
        print(int(cur.execute(f"SELECT COUNT(*) FROM joystick_current_data WHERE user_id={user_id}").fetchall()[0][0]))

    con.commit()
    con.close()
    return 0

def check_data():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res_1 = cur.execute(f"SELECT * FROM joystick_data").fetchall()
    res_2 = cur.execute(f"SELECT * FROM joystick_current_data").fetchall()
    for i in range(len(res_1)):
        print(res_1[i])
    for j in range(len(res_2)):
        print(res_2[j])

    con.commit()
    con.close()


check_logs()
check_users()
check_devices()
check_data()

#change_value(2, 3, 0)
#add_user("st2257", "wacze000", 5, 1)
#find_devices(2)
#db_add_user_data(3, 0, 0, 0, 0, 0, 0, "")

