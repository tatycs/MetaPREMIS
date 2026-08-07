#!/usr/bin/env python3
# MetaPremis — Copyright (C) 2026 Tatiana Canelhas — AGPL-3.0 (ver LICENSE).
"""
Servidor de desenvolvimento do MetaPremis.

Por que existe: o validador XSD embarcado (xmllint-wasm) usa módulo ES + Web
Worker (type:module) + WebAssembly e um fetch do premis-v3-0.xsd. Nada disso
funciona sob file://. Este servidor entrega tudo por http com:
  - MIME correto para .mjs (text/javascript) e .wasm (application/wasm) — sem
    isso o navegador recusa o módulo/worker;
  - atendimento concorrente (ThreadingHTTPServer) — o worker busca o .wasm
    enquanto a página principal aguarda; um servidor single-thread travaria;
  - Cache-Control: no-store — para o desenvolvimento sempre pegar a última versão.

Uso:  python serve.py [porta]   (padrão 8000)
NÃO é necessário em produção: o GitHub Pages já serve .mjs/.wasm com o MIME certo.
"""
import http.server
import mimetypes
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
mimetypes.add_type("text/javascript", ".mjs")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/wasm", ".wasm")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("MetaPremis — servindo %s" % ROOT)
    print("  http://127.0.0.1:%d/premis-builder.html" % PORT)
    print("Ctrl+C para parar.")
    httpd.serve_forever()
