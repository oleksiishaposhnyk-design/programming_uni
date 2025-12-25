import requests
import csv
from datetime import datetime, timedelta

url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew"

today = datetime.today()

end_date = today - timedelta(days=1)
start_date = end_date - timedelta(days=6)

dates = []
current_date = start_date
while current_date <= end_date:
    dates.append(current_date.strftime("%Y%m%d"))
    current_date += timedelta(days=1)

file_name = "nbu_last_7_days.csv"

with open(file_name, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Currency code", "Currency name", "Rate (UAH)"])

    for date in dates:
        response = requests.get(url, params={
            "date": date,
            "json": ""
        })

        data = response.json()

        for currency in data:
            writer.writerow([
                currency["exchangedate"],
                currency["cc"],
                currency["txt"],
                currency["rate"]
            ])

print("Дані збережено у файл:", file_name)
