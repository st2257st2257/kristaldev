import time
import requests
response = requests.get('http://127.0.0.1:5000/bf/get_100/7')

map_s = []

pos_s = []

if response.status_code == 200:
    map_s = str(response.content).split('|')
    map_s[0] = map_s[0][2:]

fire_map = [item.split(' ')[1:] for item in map_s][:-1]


for gg in fire_map:
    print(gg)

pos_s = [int(item) for item in map_s[-1][:-1].split(' ')]

print(pos_s)



# GET X and Y
x = 0
y = 0
if pos_s[1] == 0:
    x = pos_s[3]-5
else:
    x = pos_s[1]+5

if pos_s[0] == 0:
    y = pos_s[3]-5
else:
    y = pos_s[0]+5

print(x, y)


# GET local x, y
l_x = 0 
l_y = 0

if pos_s[1] == 0:
    l_x = pos_s[3]-5
else:
    l_x = 5

if pos_s[0] == 0:
    l_y = pos_s[2]-5
else:
    l_y = 5
print(l_x, l_y)










 
