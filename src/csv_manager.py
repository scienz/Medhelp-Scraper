import csv

def save_as_csv(file_name, mode, data: [[]]):
    with open(file_name, mode) as f:
        fw = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            fw.writerow(row)
