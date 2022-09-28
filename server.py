#  coding: utf-8 
import socketserver
import mimetypes
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Copyright 2022 Mathew Davies
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()

        decoded_string = self.data.decode('utf-8')
        
        # Isolate the request
        request = decoded_string.split('\r\n')[0].split()
        
        # Handle the request
        if (len(request) == 0): # Saftey
            return
        if request[0] != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nError, Method Not Allowed", 'utf-8'))
        else:
            # Get the path & normalize *1.
            path = os.path.normpath('./www' + request[1])
            # Check if exists and if file or path *2.
            if os.path.exists(path) and path.split('/')[0] == 'www':
                if os.path.isdir(path):
                    if request[1][-1] == '/':
                        self.read_and_send_file(path + '/index.html')
                    else:
                        new_path = "http://localhost:8080/" + request[1] + '/'
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\n\r\nLocation: " + new_path, 'utf-8'))
                else:
                    # The path is a file
                    self.read_and_send_file(path)
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nError, Not Found", 'utf-8'))        

    def read_and_send_file(self, path):
        f = open(path, 'r')
        page = f.read()
        f.close()
        # Find the filetype and send the file *3.
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: " + mimetypes.MimeTypes().guess_type(path)[0] + "\r\n\r\n" + page, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()