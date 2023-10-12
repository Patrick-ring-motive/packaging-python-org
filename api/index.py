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
  return req.wfile.write(body)
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
  localhost = req.headers['Host']
  reqHeaders = {}
  reqBody = None
  #print(req.headers)
  for header in req.headers:
    reqHeaders[header] = req.headers[header].replace(localhost,hostTarget)
  requestBodyLength = req.headers['Content-Length']
  if (req.rfile.readable() and requestBodyLength):  
    reqBody = await readRequest(req,int(requestBodyLength));
    if len(reqBody) < 5:
      reqBody = None
  #print(req.path)
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
      localhost = request.headers['Host']
      refererHost=localhost
      if request.headers['Localhost']:
        refererHost=request.headers['Localhost']
   
      response = await fetchResponse(request,hostTarget)
      resBody = await readResponseBody(response)   
      request.send_response(response.status) 
  
      headers = response.getheaders()
      #print(headers)
      for header in headers:
        if header[0]=='Location':
          none()
          #print(header,header[1].replace(hostTarget,refererHost))
        request.send_header(header[0], header[1].replace(hostTarget,localhost))
      await endHeaders(request)
      await writeResponseBody(request,resBody)

    except:
      request.send_response(200)
      request.send_header('Content-type', 'text/html')
      await endHeaders(request)
      await writeResponseBody(request,b'')
      return
    request.wfile.flush()
    #request.wfile.close()
    #closeRequest(request)
  def do_GET(request):
    try:
      asyncio.run(request.do_TEST(request))
    except:
      return
  def do_OPTIONS(request):
    try:
      asyncio.run(writeResponseBody(request,b'*'))
    except:
      none()
  def do_POST(request):
    asyncio.run(request.do_METHOD(request))
  def do_PUT(request):
    asyncio.run(request.do_METHOD(request))
  def do_PATCH(request):
    asyncio.run(request.do_METHOD(request))
  def do_HEAD(request):
    asyncio.run(request.do_METHOD(request))
  def do_DELETE(request):
    asyncio.run(request.do_METHOD(request))
  def do_CONNECT(request):
    asyncio.run(request.do_METHOD(request))
  def do_TRACE(request):
    asyncio.run(request.do_METHOD(request))

  

#asyncio.run(AsyncHTTPServer());
