"""GSWA archive reader for Fantasy Maiden Wars DoSD (GameMaker, GSWA2 loader).

layout (from gml_Script_GSWA2_init / GSWA2_find / *_load_buffer):
  meta/data{ID}.meta  = buffer_encode_ext(JSON, key=global.passwd)   -> {name: entry}
  data/<DATFILE>      = blob; entry POSITION/SIZE slice
  type per ID (GSWA_type):  -1 LEGACY(zlib raw file -> temp_dir random name)
                             0 sprite (zlib -> RGBA surface; buffer_encode only if arg2)
                             1 GRID (zlib -> ds_grid_write hex) / JSON (zlib -> text)
                             2 audio (raw ogg -> temp_dir random name)
  lookup key for type 0 = filename_key(): filename_name() cut at first '.' or '('
usage:
  python gswa.py GAME_DIR list            # per-group summary
  python gswa.py GAME_DIR dump ID OUTDIR  # extract one group
"""
import json, os, struct, sys, zlib
sys.path.insert(0, os.path.dirname(__file__))
from gmcrypt import decrypt, encrypt

PASSWD = 'Fp1OUltT6n'   # gml_Script_launch_set_test: global.passwd
TYPES = {'2-2': 0, '2-3': 0, '3': 0, '4': 1, '5-1': -1, '5-2': 1, '5-3': 1, '5-4': 1,
         '6-1': 2, '6-2': 2, '6-3': 2, '7': 0, '8': 0, '9': 0, '10': -1, '11': -1,
         '12': -1, '13': 2, '14': 0, '15': 0}


def buffer_encode(b, encoding):
    """gml_Script_buffer_encode: running additive shift 128±1 (enc/dec are inverse)."""
    out = bytearray(len(b)); bs = 128; d = 1 if encoding else -1
    for i, x in enumerate(b):
        out[i] = (x + bs) & 0xFF
        bs += d
        if bs > 255: bs = 1
        elif bs < 1: bs = 255
    return bytes(out)


def load_meta(game, did):
    raw = open(os.path.join(game, 'meta', 'data%s.meta' % did), 'rb').read()
    dec = decrypt(raw, PASSWD)
    z = dec.find(b'\0')
    return json.loads(dec[:z if z >= 0 else None].decode('utf8')), len(dec) - (z if z >= 0 else len(dec))


def save_meta(game, did, meta, pad_to=None):
    js = json.dumps(meta, ensure_ascii=False, separators=(',', ':')).encode('utf8')
    if pad_to: js = js + b'\0' * (pad_to - len(js))
    open(os.path.join(game, 'meta', 'data%s.meta' % did), 'wb').write(encrypt(js, PASSWD))


def read_entry(game, e, cache={}):
    p = os.path.join(game, 'data', e['DATFILE'])
    if p not in cache: cache.clear(); cache[p] = open(p, 'rb').read()
    pos, size = int(e['POSITION']), int(e['SIZE'])
    return cache[p][pos:pos+size]


def ds_grid_decode(s):
    """ds_grid_write hex string -> (w, h, rows). GM layout: u32 magic(0x25B), u32 w, u32 h,
    then column-major values: u32 kind (0=real f64, 1=string u32 len + bytes)."""
    b = bytes.fromhex(s.strip('\0'))
    magic, w, h = struct.unpack_from('<III', b, 0); p = 12
    cols = []
    for x in range(w):
        col = []
        for y in range(h):
            k = struct.unpack_from('<I', b, p)[0]; p += 4
            if k == 0:
                col.append(struct.unpack_from('<d', b, p)[0]); p += 8
            elif k == 1:
                n = struct.unpack_from('<I', b, p)[0]; p += 4
                col.append(b[p:p+n].decode('utf8', 'replace')); p += n
            else:
                # 13 = undefined etc.; keep raw
                col.append(None); p += 8
        cols.append(col)
    rows = [[cols[x][y] for x in range(w)] for y in range(h)]
    return magic, w, h, rows, p == len(b)


def decode(did, e, blob):
    t = TYPES[did]
    if t == 2: return 'ogg', blob
    if t == -1: return 'raw', zlib.decompress(blob)
    if t == 0:  # GSWA2_find passes encode=false: plain zlib; keep the encoded path as fallback
        return 'rgba', zlib.decompress(blob if blob[:1] == b'x' else buffer_encode(blob, False))
    if e.get('TYPE') == 'JSON': return 'json', zlib.decompress(blob).rstrip(b'\0')
    return 'grid', zlib.decompress(blob).rstrip(b'\0')


def main():
    game, cmd = sys.argv[1], sys.argv[2]
    if cmd == 'list':
        for did in TYPES:
            m, pad = load_meta(game, did)
            print('%-4s type %2d  %5d entries  pad %6d' % (did, TYPES[did], len(m), pad))
    elif cmd == 'dump':
        did, out = sys.argv[3], sys.argv[4]
        os.makedirs(out, exist_ok=True)
        m, _ = load_meta(game, did)
        for name, e in m.items():
            kind, data = decode(did, e, read_entry(game, e))
            fn = os.path.join(out, name)
            if kind == 'rgba':
                from PIL import Image
                w, h = int(e['SURFACE_WIDTH']), int(e['SURFACE_HEIGHT'])
                Image.frombytes('RGBA', (w, h), data[:w*h*4]).save(fn + '.png')
            elif kind == 'grid':
                mg, w, h, rows, ok = ds_grid_decode(data.decode('latin1'))
                with open(fn + '.tsv', 'w', encoding='utf8', newline='') as f:
                    for r in rows:
                        f.write('\t'.join('' if v is None else (repr(v) if isinstance(v, float) else
                                v.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r'))
                                for v in r) + '\n')
                if not ok: print('WARN grid trailing', name)
            else:
                ext = {'ogg': '', 'json': '.json', 'raw': ''}[kind]
                open(fn + ext if not name.endswith(ext) else fn, 'wb').write(data)
        print('dumped', len(m), 'entries to', out)


if __name__ == '__main__':
    main()
