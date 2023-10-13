from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import sys,threading



def handle_exception(exc_type, exc_value, exc_traceback):
  print("Unhandled Exception")
sys.excepthook = handle_exception

run_old = threading.Thread.run
def run(*args, **kwargs):
    try:
        run_old(*args, **kwargs)
    except:
        handle_exception()
threading.Thread.run = run





def none():
  return
  

def closeRequest(request):
  if 'close' in request.close:
    none()
#async def AsyncHTTPServer():
hostTarget = 'packaging.python.org'
async def endHeaders(request):
  return request.end_headers()
async def readResponseBody(res):
  return res.read()
async def writeResponseBody(req,body):
  return req.wfile.write(body+b'\x03\x04')
async def readRequest(req,length):
  if length < 5:
    return b''
  return req.rfile.read(length)
async def connectClient(host):
  return http.client.HTTPSConnection(host)
async def connectRequest(connection, requestCommand, requestPath, requestBody, requestHeaders):
  return connection.request(requestCommand, requestPath, body=requestBody, headers=requestHeaders)
async def connectResponse(connection):
  return connection.getresponse()
async def connectClose(connection):
  connection.close()
async def streamDetach(stream):
  stream.detach()
async def fetchResponse(req,host):  
  connection = await connectClient(host)
  reqHeaders = {}
  reqBody = None
  for header in req.headers:
    if header == 'Connection':
      continue
    if header == 'Transfer-Encoding':
      continue
    reqHeaders[header] = req.headers[header].replace(req.localhost,hostTarget)
  requestBodyLength = req.headers['Content-Length']
  if (req.rfile.readable() and requestBodyLength):  
    reqBody = await readRequest(req,int(requestBodyLength));
    if len(reqBody) < 5:
      reqBody = None
  await connectRequest(connection, req.command, req.path, reqBody, reqHeaders)
  res = await connectResponse(connection)
  return res
class handler(BaseHTTPRequestHandler):  
  async def do_TEST(self,data):
    self.send_response(200)
    self.send_header('Content-type','text/plain')
    self.end_headers()
    self.wfile.write('Hello, world!'.encode('utf-8'))
    return
  async def do_METHOD(request,data):
    try:
      request.localhost = request.headers['Host']
      request.refererHost=request.localhost
      if request.headers['Localhost']:
        request.refererHost=request.headers['Localhost']
      response = await fetchResponse(request,hostTarget)
      resBody = await readResponseBody(response)   
      request.send_response(response.status) 
      headers = response.getheaders()
      for header in headers:
        if header[0]=='Transfer-Encoding':
          continue
        if header[0]=='Connection':
          continue
        request.send_header(header[0], header[1].replace(hostTarget,request.localhost))
      request.send_header('status','200')
      await endHeaders(request)
      await writeResponseBody(request,resBody)
    except:
      request.send_response(200)
      request.send_header('Content-type', 'text/html')
      await endHeaders(request)
      await writeResponseBody(request,b'\x03\x04')
    request.wfile.flush()
    if request.localhost:
      if request.localhost == 'packaging-python-org.weblet.repl.co':
        request.wfile.close()
        closeRequest(request)
  def do_TRY(request,data):
    try:
      asyncio.run(request.do_METHOD(request))
    except:
      return
  def do_GET(request):
    return request.do_TRY(request)
  def do_POST(request):
    return request.do_TRY(request)
  def do_PUT(request):
    return request.do_TRY(request)
  def do_PATCH(request):
    return request.do_TRY(request)
  def do_HEAD(request):
    return request.do_TRY(request)
  def do_DELETE(request):
    return request.do_TRY(request)
  def do_CONNECT(request):
    return request.do_TRY(request)
  def do_TRACE(request):
    return request.do_TRY(request)
  def do_OPTIONS(request):
    try:
      asyncio.run(writeResponseBody(request,b'*'))
    except:
      return

  

#asyncio.run(AsyncHTTPServer());
