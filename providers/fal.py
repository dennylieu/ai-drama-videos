#!/usr/bin/env python3
"""Minimal fal queue runner (no SDK). The API key is injected by the environment's network proxy for queue.fal.run, so
the Authorization header here is only a placeholder; never put a real key in code or args.

Usage:
    python3 -I -B providers/fal.py ENDPOINT INPUT.json OUT_DIR [--poll 5] [--timeout 1800]

INPUT.json is the model's input. Local files can be referenced as "@file:/abs/path.png" anywhere in the JSON
(including inside lists); they are sent inline as data URIs. Every media URL in the result is downloaded into OUT_DIR,
and result.json + request.json (with data URIs elided) are written next to them.
"""
import base64
import json
import mimetypes
import pathlib
import sys
import time
import urllib.request

AUTH = {"Authorization": "Key proxy-injected", "Content-Type": "application/json"}


def inline(v):
    if isinstance(v, str) and v.startswith("@file:"):
        p = pathlib.Path(v[6:])
        mt = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        return f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()
    if isinstance(v, list):
        return [inline(x) for x in v]
    if isinstance(v, dict):
        return {k: inline(x) for k, x in v.items()}
    return v


def call(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=AUTH)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"{}")


def media_urls(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "url" and isinstance(v, str) and v.startswith("http"):
                yield v
            else:
                yield from media_urls(v)
    elif isinstance(o, list):
        for x in o:
            yield from media_urls(x)


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    endpoint, inp, out = a[0], json.load(open(a[1])), pathlib.Path(a[2])
    poll = float(a[a.index("--poll") + 1]) if "--poll" in a else 5
    timeout = float(a[a.index("--timeout") + 1]) if "--timeout" in a else 1800
    out.mkdir(parents=True, exist_ok=True)
    (out / "request.json").write_text(json.dumps({"endpoint": endpoint, "input": inp}, indent=1))
    sub = call("POST", f"https://queue.fal.run/{endpoint}", inline(inp))
    rid, status_url, resp_url = sub["request_id"], sub["status_url"], sub["response_url"]
    print("request_id", rid, flush=True)
    t0 = time.time()
    while True:
        st = call("GET", status_url)
        if st.get("status") == "COMPLETED":
            break
        if time.time() - t0 > timeout:
            sys.exit(f"timeout; request {rid} still {st.get('status')}")
        time.sleep(poll)
    res = call("GET", resp_url)
    (out / "result.json").write_text(json.dumps(res, indent=1))
    for i, u in enumerate(dict.fromkeys(media_urls(res))):
        name = f"{i:02d}_" + u.split("/")[-1].split("?")[0]
        urllib.request.urlretrieve(u, out / name)
        print("saved", out / name)


if __name__ == "__main__":
    main()
