#!/usr/bin/env python3
"""Generate 6 Catan resource tiles in storybook style via HF FLUX.1-schnell."""
import io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image

SPACE = "black-forest-labs/FLUX.1-schnell"
HOST = "https://black-forest-labs-flux-1-schnell.hf.space"
OUTDIR = "/Users/lapame10/.hermes/workspace/catan/arte"
os.makedirs(OUTDIR, exist_ok=True)

STYLE = (
    "Children's storybook illustration, cozy gouache and watercolour painting, "
    "soft rounded brush lines, warm saturated colours, gentle friendly medieval-fantasy world, "
    "cheerful cartoon style, warm golden late-afternoon light, soft shadows, "
    "slightly elevated three-quarter aerial view looking down at a tabletop diorama, painterly textures. "
    "Square composition that completely fills the entire frame edge to edge, full bleed, "
    "no border, no frame, no margin, no vignette, no white edges. "
    "Strictly no text, no letters, no numbers, no writing, no signs, no watermark, no signature. "
    "Main subject centred in the middle of the image so it survives a hexagonal crop. "
)

TILES = [
    ("bosque.png", 101,
     "A lush cozy forest clearing with deep vivid greens. Big round-canopy trees, "
     "a small wooden cabin with a steep gabled roof in the centre of the scene, "
     "a cheerful cartoon lumberjack chopping firewood with an axe, red mushrooms with white dots, "
     "an axe stuck in a tree stump, a winding dirt path."),
    ("pasto.png", 202,
     "A sunny bright green pasture on soft rolling hills with light green and yellow tones. "
     "Several fluffy round white sheep grazing, a friendly cartoon shepherd wearing a hat "
     "holding a wooden shepherd's crook in the centre, a rustic wooden fence, a single lone tree, "
     "colourful wildflowers, a blue sky with puffy clouds."),
    ("trigo.png", 303,
     "A golden field of ripe wheat swaying in waves, rich golds and ochres. "
     "A friendly cartoon farmer wearing a straw hat holding a scythe in the centre, "
     "tied sheaves of wheat bundles, a small windmill in the background, a warm glowing sky."),
    ("ladrillo.png", 404,
     "A red clay quarry with reds and terracotta tones. Big lumps and mounds of red clay, "
     "stacks of bricks drying in the sun, a cheerful cartoon mason with a shovel and a wheelbarrow "
     "in the centre, a small brick kiln, reddish earthy ground."),
    ("mineral.png", 505,
     "Grey rocky mountains with snowy white peaks, cool grey and blue tones. "
     "A mine entrance supported by wooden beams in the centre of the scene, "
     "a mine cart full of glittering sparkling ore, a pickaxe leaning against a rock, "
     "a friendly cartoon miner wearing a helmet with a lamp, scattered rocks and crystals."),
    ("desierto.png", 606,
     "Golden sand dunes under a bright shining sun, warm sands and a warm sky. "
     "A green cactus with pink flowers, an old round stone well in the centre of the scene, "
     "a palm tree, a distant camel caravan silhouette, glowing warm sky."),
]


def call_infer(prompt, seed, width=1024, height=1024, steps=4, retries=4):
    payload = {"data": [prompt, seed, False, width, height, steps]}
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                HOST + "/gradio_api/call/infer",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                eid = json.load(r)["event_id"]
            url = f"{HOST}/gradio_api/call/infer/{eid}"
            for _ in range(150):
                try:
                    with urllib.request.urlopen(url, timeout=120) as r:
                        buf = r.read().decode(errors="replace")
                except urllib.error.HTTPError as e:
                    print("  poll HTTP", e.code, flush=True)
                    break
                got = None
                for line in buf.splitlines():
                    if line.startswith("data: "):
                        try:
                            got = json.loads(line[6:])
                        except Exception:
                            pass
                if got is not None:
                    return got
                time.sleep(2)
        except Exception as e:
            last = e
            print("  attempt %d failed: %s" % (attempt + 1, e), flush=True)
            time.sleep(5)
    raise RuntimeError("infer failed: %s" % last)


def download(url, retries=4):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read()
        except Exception as e:
            print("  dl attempt %d failed: %s" % (attempt + 1, e), flush=True)
            time.sleep(4)
    raise RuntimeError("download failed")


results = []
import os as _os
for name, seed, body in TILES:
    out = os.path.join(OUTDIR, name)
    if _os.path.exists(out) and _os.path.getsize(out) > 100000:
        print("=== %s === YA EXISTE, se salta" % name, flush=True)
        continue
    print("=== %s ===" % name, flush=True)
    prompt = STYLE + body
    t0 = time.time()
    res = call_infer(prompt, seed)
    if not isinstance(res, list) or not res or not isinstance(res[0], dict):
        print("  unexpected result:", json.dumps(res)[:400], flush=True)
        continue
    raw = download(res[0]["url"])
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("  saved %s  %dx%d  %d bytes  (%.1fs)" % (out, img.size[0], img.size[1], size, time.time() - t0), flush=True)
    results.append((out, img.size, size))

print("\nDONE")
for r in results:
    print(r[0], r[1], r[2])
