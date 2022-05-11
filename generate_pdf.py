import json
import os
import platform
import sys
from datetime import datetime
from typing import List
# import dateutil.utils
import requests
import urllib.parse
import subprocess

pdffile_path = "PLR_Result.pdf"

USAGE = f"Usage: python {sys.argv[0]} [--help] | json file with values]"

url = "https://script.google.com/macros/s/AKfycbxyHE9o9RoxMKtUvWV3mYh9qgmIh_2bbCwaJcUNwsMMZED3Sl6G0Uf_r8cvHMPwJp2n/exec?"
date_order = datetime.today()
date_result = date_order
date_birthday = datetime.strptime("01/01/1990", "%d/%m/%Y")


def calculate_age(date_birthday, date_order):
    # today = datetime.strptime(date_order, "%d/%m/%Y")
    # dob = datetime.strptime(date_birthday, "%d/%m/%Y")
    years = ((date_order - date_birthday).total_seconds() / (365.242 * 24 * 3600))
    yearsInt = int(years)
    months = (years - yearsInt) * 12
    monthsInt = int(months)
    return f"{yearsInt} Y {monthsInt} M"


calculated_age = calculate_age(date_birthday, date_order)
sex = "M"
name = "Ivan"

def validate(args: List[str]):
    with open(args[0]) as json_file:
        payload = json.load(json_file)
        print(f"json loaded {payload}")
        return payload


def main(args: List[str]):
    if not args:
        raise SystemExit(USAGE)

    if args[0] == "--help":
        print(USAGE)
    else:
        payload = validate(args)

    if len(payload) == 0:
        payload = {"date_order": date_order,
                   "date_result": date_result,
                   "date_birthday": date_birthday,
                   "age": calculated_age,
                   "sex": sex,
                   "name": "John Smith"}
    else:
        payload["date_order"] = date_order
        payload["date_result"] = date_result
        payload["calculated_age"] = calculated_age
        payload["name"] = name

    print("processing ")
    u = url + urllib.parse.urlencode(payload)
    response = requests.get(u)
    print("file generated")
    response = requests.get(response.content)
    print("file downloaded")
    with open(pdffile_path, "wb") as f:
        f.write(response.content)

    print("pdf is opening")
    filepath = pdffile_path
    if platform.system() == 'Darwin':
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':
        os.startfile(filepath)
    else:
        subprocess.call(('xdg-open', filepath))


if __name__ == '__main__':
    main(sys.argv[1:])
