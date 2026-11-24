#!/usr/bin/env python3
"""Higgsfield API example: Seedance 2.5 text-to-video via the official Python SDK (higgsfield-client).

Credentials: HF_KEY in .env.local (KEY_ID:KEY_SECRET), loaded at runtime and never printed. In the cloud environment
the real key is injected by the network proxy for api.higgsfield.ai and .env.local holds only a placeholder.

Run:  python3 main.py
Exits 0 and prints the video URL only when the request completed; exits non-zero on failed, canceled or moderated
(nsfw) requests, or on any API error.
"""
import sys

from dotenv import load_dotenv

load_dotenv(".env.local")

import higgsfield_client  # noqa: E402  (import after the env file is loaded)
from higgsfield_client import types_  # noqa: E402

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}

TERMINAL_BAD = {
    types_.Failed: "failed",
    types_.NSFW: "moderated (nsfw)",
    types_.Cancelled: "canceled",
}


def main() -> int:
    last = {"status": None}

    def on_update(status):
        if type(status) is not type(last["status"]):
            print(f"status: {type(status).__name__}", flush=True)
        last["status"] = status

    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGS,
            on_enqueue=lambda rid: print(f"request_id: {rid}", flush=True),
            on_queue_update=on_update,
        )
    except higgsfield_client.HiggsfieldClientError as e:  # API/HTTP errors; message never contains the key
        print(f"ERROR: request did not complete: {e}", file=sys.stderr)
        return 1

    st = last["status"]
    for cls, label in TERMINAL_BAD.items():
        if isinstance(st, cls):
            print(f"ERROR: request {label}; no video was produced.", file=sys.stderr)
            return 2

    final = str((result or {}).get("status", "")).lower()
    if final and final != "completed":
        print(f"ERROR: request ended with status '{final}'; no video was produced.", file=sys.stderr)
        return 2

    video = (result or {}).get("video") or {}
    url = video.get("url") if isinstance(video, dict) else None
    if not url:
        print(f"ERROR: no video URL in the result (keys: {sorted((result or {}).keys())}).", file=sys.stderr)
        return 3
    print(f"video_url: {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
