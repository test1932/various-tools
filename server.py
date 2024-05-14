# imports
import webbrowser
import sys
from flask import Flask, send_from_directory, request
import threading
from bs4 import BeautifulSoup

"""
when using POST requests for updating files, the
body should have form {pNo: integer, text: string}
"""

# globals
PORT = 8080

# replace content of paragraph with new text
def replacePara(fname, paraNo, newText):
    file = open(fname, "r+")
    soup = BeautifulSoup(file.read(), "lxml")
    tag = soup.select_one(f'p:nth-of-type({paraNo})')
    tag.string = newText
    file.seek(0)
    file.truncate()
    file.write(str(soup))
    file.close()

# main
def main():
    if len(sys.argv) != 2:
        print("usage: python -B server.py <filename>.html")
        return
    fname = sys.argv[1]
    
    app = Flask(__name__)

    @app.route('/<path:path>', methods=['GET'])
    def exposeStatic(path: str):
        return send_from_directory('', path)
    
    @app.route('/<path:path>', methods=['POST'])
    def replaceParagraph(path:str):
        paragraphNo = request.json['pNo']
        newText = request.json['text']
        replacePara(path, paragraphNo, newText)
        return send_from_directory('', path)

    def runServer():
        app.run(debug=False, use_reloader = False, port = PORT, host = '0.0.0.0')
    
    serverThread = threading.Thread(None, runServer, "server", [])
    serverThread.start()
    webbrowser.open(f"http://127.0.0.1:8080/{fname}", new = 0)
    serverThread.join()

if __name__ == '__main__':
    main()