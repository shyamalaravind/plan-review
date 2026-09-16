#!/usr/bin/env python3
"""Open a markdown file in the browser for inline review; print the feedback when submitted."""
import json
import secrets
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGE = (Path(__file__).resolve().parent / "page.html").read_text()


def one_line(s):
    return " ".join(s.split())


def render(name, r):
    comments, general = r.get("comments", []), r.get("general", "")
    if r.get("approved") and not comments and not general:
        return f"APPROVED: {name} — no changes requested."
    status = "APPROVED WITH NOTES" if r.get("approved") else "CHANGES REQUESTED"
    out = [f"{status}: review of {name}", ""]
    for i, c in enumerate(comments, 1):
        out.append(f'{i}. On: "{one_line(c["quote"])}"')
        out += ["   " + line for line in c["note"].splitlines()]
    if general:
        out += ["", "General:", general]
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: review.py <file.md>")
    path = Path(sys.argv[1]).expanduser()
    plan = json.dumps({"name": path.name, "text": path.read_text()})
    # Random path prefix so other local pages can't read the plan or post fake feedback.
    base = f"/{secrets.token_urlsafe(16)}/"
    done, result = threading.Event(), {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def reply(self, body, ctype):
            data = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == base:
                self.reply(PAGE, "text/html; charset=utf-8")
            elif self.path == base + "plan":
                self.reply(plan, "application/json")
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path != base + "submit" or self.headers.get("Content-Type") != "application/json":
                return self.send_error(404)
            result.update(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            self.reply("{}", "application/json")
            done.set()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}{base}"
    print(f"Review open at {url}", file=sys.stderr, flush=True)
    webbrowser.open(url)
    done.wait()
    server.shutdown()
    print(render(path.name, result))


if __name__ == "__main__":
    main()
