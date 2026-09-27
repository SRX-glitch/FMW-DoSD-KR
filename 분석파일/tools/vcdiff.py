"""Minimal VCDIFF (RFC 3284, xdelta3 w/o secondary compression) decoder.

apply(patch, source)            -> target bytes
partial(patch)                  -> (target bytearray, known mask, stats) without the source:
                                   ADD/RUN bytes and target self-copies are known, source copies unknown.
usage: python vcdiff.py PATCH [SOURCE OUT]
"""
import struct, sys


def _vi(b, p):
    r = 0
    while True:
        c = b[p]; p += 1; r = (r << 7) | (c & 0x7F)
        if not c & 0x80: return r, p


def _table():
    # default code table (RFC 3284 §5.6): entries (t1,s1,m1,t2,s2,m2); t: 0 NOOP 1 ADD 2 RUN 3 COPY
    T = [(2, 0, 0, 0, 0, 0)]
    T += [(1, s, 0, 0, 0, 0) for s in range(0, 18)]
    for m in range(9):
        T += [(3, 0, m, 0, 0, 0)] + [(3, s, m, 0, 0, 0) for s in range(4, 19)]
    for m in range(6):
        for a in range(1, 5):
            for c in range(4, 7): T.append((1, a, 0, 3, c, m))
    for m in range(6, 9):
        for a in range(1, 5): T.append((1, a, 0, 3, 4, m))
    for m in range(9): T.append((3, 4, m, 1, 1, 0))
    assert len(T) == 256
    return T


TABLE = _table()


def _decode(patch, source):
    b = patch; assert b[:4] == b'\xd6\xc3\xc4\x00'
    ind = b[4]; p = 5
    if ind & 1: raise ValueError('secondary compression not supported')
    if ind & 2: raise ValueError('custom code table not supported')
    if ind & 4:
        n, p = _vi(b, p); p += n
    out = bytearray(); known = bytearray(); st = {'add': 0, 'run': 0, 'copy_src': 0, 'copy_tgt': 0}
    while p < len(b):
        wi = b[p]; p += 1; sseg = spos = 0
        if wi & 3:
            sseg, p = _vi(b, p); spos, p = _vi(b, p)
        dl, p = _vi(b, p); tw, p = _vi(b, p); p += 1  # delta indicator
        ld, p = _vi(b, p); li, p = _vi(b, p); la, p = _vi(b, p)
        cks = struct.unpack_from('>I', b, p)[0] if wi & 4 else None
        if wi & 4: p += 4  # adler32 of this target window
        data = b[p:p+ld]; p += ld; inst = b[p:p+li]; p += li; addr = b[p:p+la]; p += la
        dp = ip = ap = 0; near = [0]*4; ni = 0; same = [0]*(3*256)
        tstart = len(out); here_base = sseg if wi & 3 else 0
        while ip < len(inst):
            code = inst[ip]; ip += 1
            e = TABLE[code]
            for t, s, m in ((e[0], e[1], e[2]), (e[3], e[4], e[5])):
                if t == 0: continue
                if s == 0: s, ip = _vi(inst, ip)
                if t == 1:
                    out += data[dp:dp+s]; known += b'\1'*s; dp += s; st['add'] += s
                elif t == 2:
                    out += bytes([data[dp]])*s; known += b'\1'*s; dp += 1; st['run'] += s
                else:
                    here = here_base + (len(out) - tstart)
                    if m == 0: a, ap = _vi(addr, ap)
                    elif m == 1: v, ap = _vi(addr, ap); a = here - v
                    elif m < 6: v, ap = _vi(addr, ap); a = near[m-2] + v
                    else: a = same[(m-6)*256 + addr[ap]]; ap += 1
                    near[ni] = a; ni = (ni + 1) % 4; same[a % 768] = a
                    for k in range(s):
                        x = a + k
                        if x < sseg and wi & 3:
                            if wi & 1 and source is not None:
                                out.append(source[spos + x]); known.append(1)
                            else:
                                out.append(0); known.append(0)
                            st['copy_src'] += 1
                        else:
                            q = tstart + x - sseg if wi & 3 else tstart + x
                            out.append(out[q]); known.append(known[q]); st['copy_tgt'] += 1
        if cks is not None and source is not None:
            import zlib
            ok = zlib.adler32(bytes(out[tstart:])) == cks
            st.setdefault('adler_ok', 0); st.setdefault('adler_bad', 0)
            st['adler_ok' if ok else 'adler_bad'] += 1
    return out, known, st


def apply(patch, source):
    o, k, st = _decode(patch, source)
    if st.get('adler_bad'): raise ValueError('adler32 mismatch: wrong source file %r' % st)
    return bytes(o), st
def partial(patch): return _decode(patch, None)


if __name__ == '__main__':
    pt = open(sys.argv[1], 'rb').read()
    if len(sys.argv) > 3:
        o, st = apply(pt, open(sys.argv[2], 'rb').read())
        open(sys.argv[3], 'wb').write(o); print(len(o), st)
    else:
        o, k, st = partial(pt)
        print(len(o), sum(k), st)
