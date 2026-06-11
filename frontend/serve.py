"""Static file server + reverse proxy for the Stockwise frontend.

Serves the files in this directory on port 3000 and forwards any request whose
path starts with ``/api/products`` or ``/api/stock-items`` to the matching
microservice (8081 / 8082 by default). The proxy lets the browser see a single
origin so the backend does not need CORS middleware.

Run::

    python frontend/serve.py            # defaults: 0.0.0.0:3000
    python frontend/serve.py --port 4000
"""

from __future__ import annotations

import argparse
import os
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib import error as urlerror
from urllib import request as urlrequest

HERE = os.path.dirname(os.path.abspath(__file__))

PRODUCT_BASE = os.environ.get("PRODUCT_API", "http://localhost:8081")
INVENTORY_BASE = os.environ.get("INVENTORY_API", "http://localhost:8082")

ROUTES = (
    ("/api/products", PRODUCT_BASE),
    ("/api/stock-items", INVENTORY_BASE),
)

HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
}


def pick_route(path: str):
    for prefix, base in ROUTES:
        if path == prefix or path.startswith(prefix + "/") or path.startswith(prefix + "?"):
            return base
    return None


class FrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        sys.stderr.write("[serve] %s - %s\n" % (self.address_string(), format % args))

    def do_GET(self) -> None:  # noqa: N802
        if pick_route(self.path):
            self._proxy("GET")
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if pick_route(self.path):
            self._proxy("POST")
            return
        self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def do_PUT(self) -> None:  # noqa: N802
        if pick_route(self.path):
            self._proxy("PUT")
            return
        self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def do_DELETE(self) -> None:  # noqa: N802
        if pick_route(self.path):
            self._proxy("DELETE")
            return
        self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def _proxy(self, method: str) -> None:
        base = pick_route(self.path)
        if base is None:
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        target = base.rstrip("/") + self.path
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length > 0 else None

        forwarded_headers = {
            k: v
            for k, v in self.headers.items()
            if k.lower() not in HOP_BY_HOP and k.lower() != "host"
        }

        req = urlrequest.Request(target, data=body, method=method, headers=forwarded_headers)

        try:
            with urlrequest.urlopen(req, timeout=30) as resp:
                self._write_proxy_response(resp.status, resp.headers.items(), resp.read())
        except urlerror.HTTPError as err:
            payload = err.read() if err.fp else b""
            self._write_proxy_response(err.code, err.headers.items() if err.headers else [], payload)
        except urlerror.URLError as err:
            message = f'{{"code":"BACKEND_UNREACHABLE","message":"{err.reason}"}}'
            self._write_proxy_response(
                HTTPStatus.BAD_GATEWAY,
                [("Content-Type", "application/json")],
                message.encode(),
            )

    def _write_proxy_response(self, status, header_items, body: bytes) -> None:
        self.send_response(int(status))
        for key, value in header_items:
            if key.lower() in HOP_BY_HOP:
                continue
            self.send_header(key, value)
        if not any(k.lower() == "content-length" for k, _ in header_items):
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Stockwise frontend server + API proxy")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=3000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), FrontendHandler)
    print(f"Stockwise frontend listening on http://{args.host}:{args.port}")
    print(f"  proxy /api/products       -> {PRODUCT_BASE}")
    print(f"  proxy /api/stock-items    -> {INVENTORY_BASE}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping frontend server…")
        server.server_close()


if __name__ == "__main__":
    main()
