from flask import render_template
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import (
    AnonymousUserMixin
)
import sqlite3


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


check_logs()
check_users()
check_devices()


#change_value(2, 3, 0)
#add_user("st2257", "wacze000", 5, 1)
#find_devices(2)
