import webbrowser
import requests
import hashlib
import json
import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD


def main():
    def drop_inside_listbox(event):
        listb.config(text="")
        filename = event.data.replace('{', '').replace('}', '')
        with open(filename, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            hash256 = hashlib.sha256(bytes).hexdigest()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
                   "Accept": "application/json",
                   "Accept-Language": "he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Referer": "https://www.virustotal.com/",
                   "content-type": "application/json",
                   "X-Tool": "vt-ui-main",
                   "x-app-version": "v1x62x1",
                   "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
                   "X-VT-Anti-Abuse-Header": "MTkzMzY2OTUyMTYtWkc5dWRDQmlaU0JsZG1scy0xNjQzMzIwMTM5LjgwNA==",
                   "DNT": "1",
                   "Connection": "keep-alive",
                   "Sec-Fetch-Dest": "empty",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Site": "same-origin",
                   "TE": "trailers"}
        result = requests.get(f'https://www.virustotal.com/ui/files/{hash256}', headers=headers)
        content = result.content
        site_json = json.loads(content)
        if 'error' in site_json:
            listb.config(font=("Courier", 12))
            listb.config(text=f"{site_json['error']['message']})")
            button.config(command=lambda: webbrowser.open_new_tab('https://www.virustotal.com/'))
        else:
            listb.config(font=("Courier", 20))
            link = site_json['data']['links']['self']
            link = f"https://www.virustotal.com/gui/file/{link[link.find('files') + 6:]}"
            total_votes = site_json['data']['attributes']['total_votes']
            last_data = site_json['data']['attributes']['last_analysis_stats']
            data1 = '\n'.join([str(i) + ' = ' + str(total_votes[i]) for i in total_votes])
            data2 = '\n'.join([str(i) + ' = ' + str(last_data[i]) for i in last_data])
            listb.config(text=f"{site_json['data']['attributes']['meaningful_name']}\n"
                              f"\ntotal_votes:\n{data1}\n"
                              f"\nlast_analysis_stats:\n{data2}")
            button.config(command=lambda: webbrowser.open_new_tab(link))


    root = TkinterDnD.Tk()
    root.geometry("800x500")
    listb = tk.Label(root, background="#ffe0d6")
    listb.pack(fill="both", expand=True)
    listb.drop_target_register(DND_FILES)
    listb.dnd_bind("<<Drop>>", drop_inside_listbox)
    button = tk.Button(root, text="Virus Total")
    button.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
