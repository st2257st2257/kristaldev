from flask import render_template
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import (
    AnonymousUserMixin
)
import numpy as np

def render(address, **kwargs):
    return render_template(address,
                           **kwargs)


# Form shown in /login
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Авторизоваться')


def get_profile_type(current_user):
    if isinstance(current_user, AnonymousUserMixin):
        return 0
    return current_user._data["profile_type"]


class Soldier:
    def __init__(self, x, y, s_id =0, h=100, f=40, w=3):
        self.x = x
        self.y = y
        self.h = h
        self.f = f
        self.w = w
        self.aim_x = None
        self.aim_y = None
        self.new_x = x
        self.new_y = y
        self.s = 1
        self.s_id = s_id

    def move(self):
        if self.h > 0:
            if (int(self.x-self.new_x) != 0) and (int(self.y-self.new_y) != 0):
                self.x += 2*self.s*(self.new_x - self.x)/((self.new_x-self.x)**2+(self.new_y-self.y)**2)**0.5
                self.y += 2*self.s*(self.new_y - self.y)/((self.new_x-self.x)**2+(self.new_y-self.y)**2)**0.5
                self.x = int(self.x)
                self.y = int(self.y)

    def fire(self, aim_x, aim_y):
        if self.w > 0:
            self.aim_x = aim_x
            self.aim_y = aim_y
            self.w =- 1

    def get_fire(self, battlefield):
        self.h -= battlefield.get_power(self.x, self.y)


class Battlefield:
    def __init__(self, x_l=1000, y_l=1000):
        self.x_l = x_l
        self.y_l = y_l
        self.power_field = np.zeros((x_l, y_l))
        self.soldier_field = [[[] for j in range(y_l)] for i in range(x_l)]
        self.dirt_field = np.zeros((x_l, y_l))

    def time_step(self):
        self.update_power_field()
        self.update_soldier_field()


    def add_soldier_fire(self, aim_x, aim_y, f):
        self.power_field[aim_x][aim_y] += f


    def update_power_field(self):
        self.power_field = np.zeros((self.x_l, self.y_l))
        for i in range(self.x_l):
            for j in range(self.y_l):
                if len(self.soldier_field[i][j]) > 0:
                    for item in self.soldier_field[i][j]:
                        if (item.aim_x != None) and (item.aim_y != None):
                            print(999)
                            self.add_soldier_fire(item.aim_x, item.aim_y, item.f * min(item.w, 1))
                            item.w -= 1
                    if item.w == 0:
                        item.aim_x = None
                        item.aim_y = None

    def update_soldier_field(self):
        res_field = [[[] for j in range(self.y_l)] for i in range(self.x_l)]
        soldier_array = []
        for i in range(self.x_l):
            for j in range(self.y_l):
                for item in self.soldier_field[i][j]:
                    soldier_array.append(item)
        for item_s in soldier_array:
            item_s.s = 1-self.dirt_field[item_s.x][item_s.y]
            item_s.move()
            item_s.h -= self.power_field[item_s.x][item_s.y]
            res_field[item_s.x][item_s.y].append(item_s)
        self.soldier_field = res_field 


    def add_soldier(self, soldier):
        self.soldier_field[soldier.x][soldier.y].append(soldier)


    def move_soldier(self, s_id, new_x, new_y, s=1):
        for i in range(self.x_l):
            for j in range(self.y_l):
                for item in self.soldier_field[i][j]:
                    if int(item.s_id) == int(s_id):
                        item.new_x = int(new_x)
                        item.new_y = int(new_y)
                        item.s = s


    def get_soldier(self, s_id):
        for i in range(self.x_l):
            for j in range(self.y_l):
                for item in self.soldier_field[i][j]:
                    if int(item.s_id) == int(s_id):
                        return {"x": item.x, "y": item.y, "h": item.h}


    def move_group(self, new_x, new_y, id_arr=[], s=1):
        for i in id_arr:
            self.move_soldier(i, new_x, new_y, s=s)


    def soldier_fire(self, s_id,  aim_x, aim_y):
        for i in range(self.x_l):
            for j in range(self.y_l):
                for item in self.soldier_field[i][j]:
                    if int(item.s_id) == int(s_id):
                        item.aim_x = int(aim_x)
                        item.aim_y = int(aim_y)


    def get_100(self, s_id):
        soldier = {}
        for i in range(self.x_l):
            for j in range(self.y_l):
                for item in self.soldier_field[i][j]:
                    if int(item.s_id) == int(s_id):
                        soldier["x"] = item.x
                        soldier["y"] = item.y
        soldier["x_min"] = max(0, soldier["x"]-5)
        soldier["x_max"] = min(self.x_l-1, soldier["x"]+5)
        soldier["y_min"] = max(0, soldier["y"]-5)
        soldier["y_max"] = min(self.y_l-1, soldier["y"]+5)

        res_arr = np.zeros((soldier["x_max"]-soldier["x_min"], soldier["y_max"]-soldier["y_min"]))

        for j in range(soldier["y_min"], soldier["y_max"]):
            for i in range(soldier["x_min"], soldier["x_max"]):
                #print(777)
                if len(self.soldier_field[i][j]) > 0:
                    #print(99)
                    res_arr[i-soldier["x_min"]][j-soldier["y_min"]] = 1

        #print(res_arr)

        res_str = ""

        for k in range(len(res_arr)):
            for l in range(len(res_arr[0])):
                res_str += " " + str(res_arr[k][l])
            res_str += "|"
        return res_str + str(soldier["x_min"]) + " " + str(soldier["y_min"]) + " " + str(soldier["x_max"]) + " " + str(soldier["y_max"])






