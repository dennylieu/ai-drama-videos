#!/usr/bin/env python3
"""Higgsfield API runner (official SDK) for Seedance 2.5 reference-to-video.

Credentials: HF_KEY from git-ignored .env.local (KEY_ID:KEY_SECRET). In the cloud environment the network proxy injects
the real key for api.higgsfield.ai and .env.local holds a placeholder. The key is never printed.

Usage:
    python3 -I -B providers/higgsfield.py JOB.json OUT_DIR

JOB.json:
    {"model": "bytedance/seedance-2.5/reference-to-video",
     "prompt": "...", "duration": 15, "aspect_ratio": "9:16", "draft": true, "generate_audio": true,
     "images": ["/abs/path/vivian.png", "/abs/path/denise.png"]}      # local files, uploaded via the SDK

draft=true renders the 480p preview ($0.1177/s at the time of writing) that we upscale with SeedVR2 instead of
finalizing. Writes request.json (no secrets), result.json and the downloaded video into OUT_DIR. Exits non-zero
unless the request completed with a video.
"""
import json
import os
import pathlib
import sys
import urllib.request

from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).resolve().parent.parent / ".env.local")

import higgsfield_client  # noqa: E402


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    job = json.load(open(sys.argv[1]))
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    model = job.pop("model", "bytedance/seedance-2.5/reference-to-video")
    images = job.pop("images", [])
    urls = []
    for p in images:
        urls.append(higgsfield_client.upload_file(p))  # returns a public URL the API can read
    if urls:
        job["image_urls"] = urls
    (out / "request.json").write_text(json.dumps({"model": model, "arguments": job, "image_files": images}, indent=1))
    try:
        result = higgsfield_client.subscribe(
            model, arguments=job,
            on_enqueue=lambda rid: print(f"request_id: {rid}", flush=True),
        )
    except higgsfield_client.HiggsfieldClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    (out / "result.json").write_text(json.dumps(result, indent=1))
    status = str(result.get("status", "")).lower()
    url = (result.get("video") or {}).get("url") if isinstance(result.get("video"), dict) else None
    if (status and status != "completed") or not url:
        print(f"ERROR: request ended '{status or 'unknown'}' without a video.", file=sys.stderr)
        return 2
    dest = out / "clip.mp4"
    urllib.request.urlretrieve(url, dest)
    print(f"video_url: {url}\nsaved: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
