import json
from nameko.rpc import RpcProxy
from werkzeug.wrappers import Response
from nameko.web.handlers import http
from urllib.parse import urlparse, parse_qs
import io
from pathlib import Path
import requests

PORT = 9000

class GatewayService:

    name = 'gateway'

    @http('POST', '/api/upload')
    def uploads(self, request):
        for file in request.files.items():
            _, file_storage = file
            file_storage.save(f"upload/{file_storage.filename}")

        return json.dumps({"status": True})

    @http('GET', '/api/download/<string:filename>')
    def get_method(self, request, filename):
        url = "http://127.0.0.1:" + str(PORT) + "/upload/" + str(filename)
        print(url)
        tmp = requests.get(url)
        print(tmp.status_code)
        if tmp.status_code == 200:
            return json.dumps({'files': url})
        else:
            return json.dumps({'files': None})

