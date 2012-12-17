import string, cgi, time
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    
    def get_document(self, source, formatted):
        lines = []

        top = open('toHtmlTop.html', 'r')
        for line in top:
            lines.append(line)
        top.close()

        lines.append(source)

        mid = open('toHtmlMid.html', 'r')
        for line in mid:
            lines.append(line)
        mid.close()

        lines.append(formatted)

        bot = open('toHtmlBot.html', 'r')
        for line in bot:
            lines.append(line)
        bot.close()

        return lines

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            lines = self.get_document('', '')
            for line in lines:
                self.wfile.write(line)

            return
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        sourceText = postvars['source'][0]
        inputFile = open('input.txt', 'w')
        inputFile.write(sourceText)
        inputFile.close()

        command = 'source-highlight -s cpp -f html -i input.txt'
        formatted = os.popen(command)
        formattedText = ''
        for line in formatted:
            formattedText += line

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        lines = self.get_document(sourceText, formattedText)
        for line in lines:
            self.wfile.write(line)

def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'starting server on port 8000'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

# import SimpleHTTPServer
# import SocketServer

# PORT = 8000

# Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

# httpd = SocketServer.TCPServer(("", PORT), Handler)

# print "serving at port", PORT
# httpd.serve_forever()
