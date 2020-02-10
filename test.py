from pathlib import Path
import httpx
from tinyhttp import HttpServer

server = HttpServer()

gold_standard = Path(__file__).read_text()
response = httpx.get('http://localhost:8080/test.py')

assert response.status_code == 200
assert response.content.decode() == gold_standard
