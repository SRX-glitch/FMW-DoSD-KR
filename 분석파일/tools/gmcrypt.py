"""Port of the game's gml_Script_buffer_encode_ext (a.k.a. file_fast_crypt_ultra).

decrypt(data, key) / encrypt(data, key) — byte-exact with the GML routine:
  H(s)      = md5_unicode(s)+sha1_unicode(s)+md5_utf8(s)+sha1_utf8(s)   (hex, 144 chars)
  kh = H(key); kh2 = H(kh); kh = kh+kh2; key_arr = hex_to_dec_fast pairs of kh
  per byte: dec = ((b ^ xs ^ k) + bs - k) mod 256 ; enc = ((b + bs + k) mod 256) ^ xs ^ k
            xs: 1..5000 (then rehash keys), bs += dir*(key_arr[len-1-kp] & 1) clamp 1..255
"""
import hashlib, sys


def _H(s):
    u, a = s.encode('utf-16-le'), s.encode('utf-8')
    return (hashlib.md5(u).hexdigest() + hashlib.sha1(u).hexdigest()
            + hashlib.md5(a).hexdigest() + hashlib.sha1(a).hexdigest())


def _hex(h):
    # gml_Script_hex_to_dec_fast: ((ord+4) mod 23 - 6) & 15 — only correct for UPPERCASE,
    # but GML md5/sha1 return lowercase, so 'a'..'f' map to 3..8. Bug-compatible on purpose.
    r = 0
    for c in h: r = (r << 4) + (((ord(c) + 4) % 23 - 6) & 15)
    return r


def _arr(kh, n):
    return [_hex(kh[2*i:2*i+2]) for i in range(n)]


def crypt(data, key, encrypting):
    kh = _H(key); kh2 = _H(kh); kh = kh + kh2
    n = len(kh) // 2; arr = _arr(kh, n)
    kp, bs, xs = 0, 128, 1 % 10
    d = 1 if encrypting else -1
    out = bytearray(len(data))
    for i, b in enumerate(data):
        k = arr[kp]
        if encrypting:
            v = ((b + bs + k) % 256) ^ (xs & 0xFF) ^ k
        else:
            v = (((b ^ xs ^ k) + bs) - k) % 256
        out[i] = v & 0xFF
        xs += 1
        if xs > 5000:
            xs = 1
            kh = _H(kh2); kh2 = _H(kh); kh = kh + kh2
            arr = _arr(kh, n)
        bs += d * (arr[n-1-kp] % 2)
        if bs > 255: bs = 1
        elif bs < 1: bs = 255
        kp += 1
        if kp > n - 1: kp = 0
    return bytes(out)


def decrypt(data, key): return crypt(data, key, False)
def encrypt(data, key): return crypt(data, key, True)


if __name__ == '__main__':
    src, key = sys.argv[1], sys.argv[2]
    out = decrypt(open(src, 'rb').read(), key)
    dst = sys.argv[3] if len(sys.argv) > 3 else None
    if dst: open(dst, 'wb').write(out)
    else: sys.stdout.buffer.write(out[:400])
