import requests as rq


url = 'https://msr8.github.io/cats'

# Download files.json
r = rq.get(f'{url}/files.json')
with open('DATA/files.json', 'wb') as f:
    f.write(r.content)

# Download files_info.json
r = rq.get(f'{url}/files_info.json')
with open('DATA/files_info.json', 'wb') as f:
    f.write(r.content)


