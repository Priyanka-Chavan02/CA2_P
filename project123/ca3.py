import os
import sqlite3
import time
import shutil
import json
import csv

print("----------------- Welcome to CHROME DATA EXTRACTER -----------\n\n\n\n")
print("---In this software we help to extract the all the browser data---")
print("for chrome history enter 'History':")
print("for chrome cookies Enter 'Cookies':")
print("for Chrome login data Enter 'Login Data':")
print("for Chrome Bookmarks data Enter 'Bookmarks':")
input_data=input()
if input_data=='History':
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, 'History')
    conn1 = sqlite3.connect('import1.db')
    shutil.copy(history_db, 'import1.db')

    # Open the copied database and execute a SQL query
    conn2 = sqlite3.connect('import1.db')
    cursor = conn2.cursor()
    select_state = "SELECT urls.url, urls.title, urls.visit_count, urls.last_visit_time FROM urls, visits WHERE urls.id=visits.url;"
    time.sleep(2)
    cursor.execute(select_state)
    results = cursor.fetchall()
    # Convert the results to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    result_dicts = [dict(zip(columns, row)) for row in results]
    with open('chrome_data.json', 'w') as f:
        json.dump(result_dicts, f)
    with open('chrome_data.json', 'r') as f:
            data = json.load(f)
    with open('chrome_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Visit Count'])

            # Write each data row to the CSV file
            for d in data:
                writer.writerow([d['url'], d['visit_count']])
if input_data=='Cookies':
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    files = os.listdir(data_path)
    cookies_db = os.path.join(data_path, 'Extension Cookies')
    conn = sqlite3.connect(cookies_db)
    cursor = conn.cursor()
    select_state = "SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, creation_utc FROM cookies"
    cursor.execute(select_state)
    results = cursor.fetchall()
    print(f"Number of results: {len(results)}")
    # Convert the results to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    result_dicts = [dict(zip(columns, row)) for row in results]
    with open('chrome_data.json', 'w') as f:
        json.dump(result_dicts, f)
    with open('chrome_data.json', 'r') as f:
        data = json.load(f)

    # Write the data to a CSV file
    with open('cookies.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Host Key', 'Name', 'Value', 'Path', 'Expires UTC', 'Is Secure', 'Is HTTP Only', 'Creation UTC'])
    for d in data:
        writer.writerow([d['host_key'], d['name'], d['value'], d['path'], d['expires_utc'], d['is_secure'], d['is_httponly'], d['creation_utc']])

if input_data=='Bookmarks':
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    bookmarks_path = os.path.join(data_path, 'Bookmarks')

    with open(bookmarks_path, encoding='utf-8') as f:
        bookmarks = json.load(f)

    # Extract relevant information from bookmarks
    bookmark_list = bookmarks['roots']['bookmark_bar']['children']
    result_dicts = []
    for bookmark in bookmark_list:
        bookmark_dict = {}
        bookmark_dict['name'] = bookmark['name']
        bookmark_dict['url'] = bookmark['url']
        result_dicts.append(bookmark_dict)

    # Write the results to a CSV file
    with open('chrome_bookmarks.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'url'])
        writer.writeheader()
        for bookmark_dict in result_dicts:
            writer.writerow(bookmark_dict)
if input_data=="Login Data":
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    files = os.listdir(data_path)
    login_db = os.path.join(data_path, 'Login Data')
    conn1 = sqlite3.connect('import1.db')
    shutil.copy(login_db, 'import1.db')

    # Open the copied database and execute a SQL query
    conn2 = sqlite3.connect('import1.db')
    cursor = conn2.cursor()
    select_state = "SELECT origin_url, username_value, password_value FROM logins;"
    time.sleep(2)
    cursor.execute(select_state)
    results = cursor.fetchall()

    # Convert the results to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    result_dicts = [dict(zip(columns, row)) for row in results]

    # Save data to CSV file
    with open('chrome_login_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Origin URL', 'Username', 'Password'])

        # Write each data row to the CSV file
        for d in result_dicts:
            writer.writerow([d['origin_url'], d['username_value'], d['password_value']])