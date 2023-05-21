from flask import Flask, request, render_template
import paramiko
import base64
import sqlite3
import datetime
import pathlib

app = Flask(__name__)

def initdb():
    con = sqlite3.connect('ftpstat.db')
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'ftpstat'")
    if res.fetchone() is None:
        res = cur.execute("CREATE TABLE ftpstat(date, filename, result, error)")
    con.close()
initdb()

@app.route("/ftp", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        retcode = get_content(request.json)
        if retcode['status'] == False:
            codetodb(retcode, request.json['filename'])
            return retcode, 400
        else:
            codetodb(retcode, request.json['filename'])
            return retcode, 200
    elif request.method == 'GET':
        selected = select_from_db()
        return render_template('ftp.html', selected=selected)
    
def get_content(jsoncontent):
    if jsoncontent.get('filename') != None and jsoncontent.get('filedata') != None:
        try:
            bdata = jsoncontent['filedata'].encode('ascii')
            fname = jsoncontent['filename']
            with open('files/' + fname, 'wb') as binary_file:
                binary_file.write(base64.b64decode(bdata))
            
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname='10.254.15.127', port=22, username='username', password='password')
            current_path = pathlib.Path.cwd()
            path_to_file = pathlib.Path(current_path, 'files', fname)
            with client.open_sftp() as sftp:            
                sftp.put(localpath=str(path_to_file), remotepath='./'+fname)
            return {'error': '', 'status': True}
        except Exception as er1:         
            return {'error': 'FTP problem ' + str(er1), 'status': False}
    else:
        return {'error': 'Incorrect JSON', 'status': False}
    
def codetodb(retcode, filename):
    row = (str(datetime.datetime.now()), filename, str(retcode['status']), retcode['error'])
    status = retcode['status']
    error = retcode['error']
    strrow = f'{str(datetime.datetime.now())}, {filename}, {status}, {error}'
    con = sqlite3.connect('ftpstat.db')
    con.execute("INSERT INTO ftpstat VALUES (?, ?, ?, ?)", row)
    con.commit()
    con.close()
      
def select_from_db():
    con = sqlite3.connect('ftpstat.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM ftpstat ORDER BY date DESC LIMIT 100")
    return res.fetchall()


if __name__ == '__main__':
    initdb()
    app.run(debug=True, host='0.0.0.0')