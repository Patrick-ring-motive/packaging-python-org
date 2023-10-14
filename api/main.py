from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio

from index import *

httpd = ThreadingHTTPServer(('', 8000), handler)
httpd.serve_forever()

#:v18-20230807-322e88b