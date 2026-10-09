#!/usr/bin/env python3
"""Minimal Kie.ai nano-banana client for Sound Out design work (key read from agent-skills-taleemabad/TOKENS.md, never printed).
  from kie_img import generate; generate(prompt, out_path, refs=[path,...], model="nano-banana-2")
"""
import base64, json, os, time, urllib.request
API = "https://api.kie.ai/api/v1"
def key():
    for l in open(os.path.expanduser("~/Documents/free_work/agent-skills-taleemabad/TOKENS.md")):
        if "KIE_API_KEY" in l and "=" in l and not l.strip().startswith("#"):
            return l.split("=", 1)[1].strip().strip('"`')
    raise SystemExit("no KIE_API_KEY")
def _req(url, body=None, host_auth=True):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=120))
_cache = {}
def upload(path):
    if path in _cache: return _cache[path]
    b = base64.b64encode(open(path, "rb").read()).decode()
    d = _req("https://kieai.redpandaai.co/api/file-base64-upload",
             {"base64Data": "data:image/png;base64," + b, "uploadPath": "soundout", "fileName": __import__("hashlib").md5(b.encode()).hexdigest()[:12] + ".png"})
    _cache[path] = d["data"]["downloadUrl"]; return _cache[path]
def generate(prompt, out, refs=(), model="nano-banana-2", aspect="1:1", res="1K", tries=3):
    for t in range(tries):
        try:
            inp = {"prompt": prompt, "aspect_ratio": aspect, "resolution": res, "output_format": "png"}
            if refs: inp["image_input"] = [upload(r) for r in refs]
            tid = _req(API + "/jobs/createTask", {"model": model, "input": inp})["data"]["taskId"]
            for _ in range(80):
                time.sleep(4)
                d = _req(API + "/jobs/recordInfo?taskId=" + tid)["data"]
                if d["state"] == "success":
                    url = json.loads(d["resultJson"])["resultUrls"][0]
                    open(out, "wb").write(urllib.request.urlopen(url, timeout=120).read()); return out
                if d["state"] == "fail": raise RuntimeError(d.get("failMsg"))
            raise RuntimeError("timeout")
        except Exception as e:
            if t == tries - 1: raise
            time.sleep(5)
if __name__ == "__main__":
    import sys; print(generate(sys.argv[1], sys.argv[2], sys.argv[3:]))
