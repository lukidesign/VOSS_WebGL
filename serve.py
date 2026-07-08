#!/usr/bin/env python3
"""本地运行 Unity WebGL 的简易静态服务器（带正确 MIME 类型）。"""
import http.server
import socketserver
import os

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".unityweb": "application/octet-stream",
        ".wasm": "application/wasm",
        ".js": "application/javascript",
        ".json": "application/json",
        ".webmanifest": "application/manifest+json",
        ".mp4": "video/mp4",
        ".png": "image/png",
        ".ico": "image/x-icon",
        ".css": "text/css",
        ".html": "text/html",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def guess_type(self, path):
        # Unity WebGL 的 .unityweb 包需要按实际内容类型返回
        if path.endswith(".wasm.unityweb"):
            return "application/wasm"
        if path.endswith(".framework.js.unityweb"):
            return "application/javascript"
        if path.endswith(".data.unityweb"):
            return "application/octet-stream"
        if path.endswith(".loader.js"):
            return "application/javascript"
        return super().guess_type(path)

    def end_headers(self):
        # 禁用缓存，便于调试/更新资源
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving VOSS_WebGL at http://localhost:{PORT}")
        print(f"Root: {ROOT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
