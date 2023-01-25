CREATE TABLE users (user_id int, login varchar(255), password varchar(255), user_type int, tag_1 varchar(255));
INSERT INTO users VALUES (1, "admin", "dbg_admin", 5, 1);
INSERT INTO users VALUES (2, "user_1", "dbg_user", 1, 1);
INSERT INTO users VALUES (3, "user_2", "dbg_user", 1, 1);
INSERT INTO users VALUES (4, "user_3", "dbg_user", 1, 1);
INSERT INTO users VALUES (5, "moder", "dbg_moder", 3, 1);

CREATE TABLE devices (device_id int, user_id int, d_name varchar(255), d_type int, d_room varchar(255));
INSERT INTO devices VALUES (1, 2, "Rele_0", 0, "room_1");
INSERT INTO devices VALUES (1, 2, "Rele_1", 0, "room_1");
INSERT INTO devices VALUES (1, 2, "Rele_2", 0, "room_1");
INSERT INTO devices VALUES (1, 3, "Rele_0", 0, "room_2");
INSERT INTO devices VALUES (1, 3, "Servo_1", 1, "room_2");
INSERT INTO devices VALUES (1, 3, "Led_2", 2, "room_2");
INSERT INTO devices VALUES (1, 3, "Camera_3", 3, "room_2");
INSERT INTO devices VALUES (1, 3, "Micro_4", 4, "room_2");
INSERT INTO devices VALUES (1, 3, "Sound_5", 5, "room_2");

CREATE TABLE logs (log_id int, log_text varchar(255));
