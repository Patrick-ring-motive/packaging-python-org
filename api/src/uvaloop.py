import asyncio
import sys
import uvloop
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client

def async_run(fun,params):
  if sys.version_info >= (3, 11):
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
      if len(params) > 0:
        runner.run(fun(*params))
      else:
        runner.run(fun())
  else:
    uvloop.install()
    asyncio.run(fun(*params))