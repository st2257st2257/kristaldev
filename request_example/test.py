import requests
# целевой URL-адрес
url = 'http://kristaldev.online:8091/upload_file'
# открываем файл на чтение в 
# бинарном режиме ('rb')
fp = open('а1.jpg', 'rb')
# помещаем объект файла в словарь 
# в качестве значения с ключом 'file'
files = {'first_file': fp, 'post_type': 'first_file'}
# передаем созданный словарь аргументу `files`
resp = requests.post(url, files=files, data={'post_type': 'first_file'})
fp.close()
resp.text

