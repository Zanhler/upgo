# servidor local sem cache e com suporte a Range (vídeos)
import http.server, sys, os, re
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()
    def send_head(self):
        rng = self.headers.get("Range"); path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path): return super().send_head()
        m = re.match(r"bytes=(\d*)-(\d*)", rng); size = os.path.getsize(path)
        start = int(m.group(1)) if m and m.group(1) else 0
        end = min(int(m.group(2)) if m and m.group(2) else size - 1, size - 1)
        f = open(path, "rb"); f.seek(start)
        self.send_response(206); self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}"); self.send_header("Content-Length", str(end - start + 1))
        self.end_headers(); self._left = end - start + 1; return f
    def copyfile(self, src, dst):
        left = getattr(self, "_left", None)
        if left is None: return super().copyfile(src, dst)
        while left > 0:
            buf = src.read(min(65536, left))
            if not buf: break
            try: dst.write(buf)
            except (ConnectionResetError, BrokenPipeError): break
            left -= len(buf)
        self._left = None
port = int(sys.argv[1]) if len(sys.argv) > 1 else 4200
http.server.ThreadingHTTPServer(("", port), H).serve_forever()
