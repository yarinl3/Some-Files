import requests
import os.path

try:
    os.mkdir('Digital Whisper')
except:
    pass

for i in range(1, 150):
    hexa = hex(i)
    if len(hexa) == 3:
        hexa = hexa[:-1]+'0'+hexa[-1]
    hexa = hexa[:2] + hexa[2:].upper()
    if os.path.isfile(rf'Digital Whisper/{i}.pdf') is True:
        continue
    url = f'https://www.digitalwhisper.co.il/files/Zines/{hexa}/DigitalWhisper{i}.pdf'
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print('Error in ' + url)
        continue
    with open(rf'Digital Whisper/{i}.pdf', 'wb') as fd:
        fd.write(r.content)
