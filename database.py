import sqlite3
con = sqlite3.connect("data.db")


cur = con.cursor()

cur.execute("DROP TABLE joystick_current_data;")
cur.execute("DROP TABLE joystick_data;")
cur.execute("DROP TABLE users;")
cur.execute("DROP TABLE devices;")
cur.execute("DROP TABLE logs;")
cur.execute("DROP TABLE sensors_data;")
cur.execute("DROP TABLE sensors_current_data;")


cur.execute("CREATE TABLE users (user_id int PRIMARY KEY, login varchar(255), password varchar(255), user_type int, tag_1 varchar(255));")
cur.execute("INSERT INTO users VALUES (1, \"admin\", \"dbg_admin\", 5, 1);")
cur.execute("INSERT INTO users VALUES (2, \"user_1\", \"dbg_user\", 1, 1);")
cur.execute("INSERT INTO users VALUES (3, \"user_2\", \"dbg_user\", 1, 1);")
cur.execute("INSERT INTO users VALUES (4, \"user_3\", \"dbg_user\", 1, 1);")
cur.execute("INSERT INTO users VALUES (5, \"moder\", \"dbg_moder\", 3, 1);")

res = cur.execute("SELECT * FROM users")
print(res.fetchall())

cur.execute("CREATE TABLE devices (device_id int PRIMARY KEY, user_id int, d_name varchar(255), d_type int, d_room varchar(255), value int);")
cur.execute("INSERT INTO devices VALUES (1, 2, \"Rele_0\", 0, \"room_1\", 0);")
cur.execute("INSERT INTO devices VALUES (2, 2, \"Rele_1\", 0, \"room_1\", 0);")
cur.execute("INSERT INTO devices VALUES (3, 2, \"Rele_2\", 0, \"room_1\", 0);")
cur.execute("INSERT INTO devices VALUES (4, 2, \"Rele_4\", 0, \"room_2\", 0);")
cur.execute("INSERT INTO devices VALUES (5, 3, \"Servo_1\", 1, \"room_2\", 0);")
cur.execute("INSERT INTO devices VALUES (6, 3, \"Led_2\", 2, \"room_2\", 0);")
cur.execute("INSERT INTO devices VALUES (7, 3, \"Camera_3\", 3, \"room_2\", 0);")
cur.execute("INSERT INTO devices VALUES (8, 3, \"Micro_4\", 4, \"room_2\", 0);")
cur.execute("INSERT INTO devices VALUES (9, 3, \"Sound_5\", 5, \"room_2\", 0);")

res_devices = cur.execute("SELECT * FROM devices")
print(res_devices.fetchall())

cur.execute("CREATE TABLE logs (log_id int PRIMARY KEY, log_text varchar(255));")


cur.execute(f"CREATE TABLE joystick_data (data_id int PRIMARY KEY, user_id int, joy_x int, joy_y int, check_1 int, check_2 int, check_3 int, check_4 int, text_field varchar(255), time_data varchar(255));");
cur.execute(f"CREATE TABLE joystick_current_data (user_id int, joy_x int, joy_y int, check_1 int, check_2 int, check_3 int, check_4 int, text_field varchar(255));");

cur.execute(f"CREATE TABLE sensors_data (data_id int PRIMARY KEY, user_id int, gps_lat double, gps_lng double, a_x double, a_y double, a_z double, bme_temp double, bme_pres double, bme_alt double, bme_hid double, time_data varchar(255));");
cur.execute(f"CREATE TABLE sensors_current_data (user_id int, gps_lat double, gps_lng double, a_x double, a_y double, a_z double, bme_temp double, bme_pres double, bme_alt double, bme_hid double);");


con.commit()

con.close()
