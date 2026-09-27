"""GameMaker bytecode 17 (GMS 2.3+) disassembler for data.win.

usage: python gmdis.py <data.win> [name-regex] [--out DIR]
  - resolves variable/function references via VARI/FUNC occurrence chains
  - writes one .asm per code entry (child functions share their parent's blob)
"""
import struct, sys, re, os

OPS = {0x07:'conv',0x08:'mul',0x09:'div',0x0A:'rem',0x0B:'mod',0x0C:'add',0x0D:'sub',
       0x0E:'and',0x0F:'or',0x10:'xor',0x11:'neg',0x12:'not',0x13:'shl',0x14:'shr',0x15:'cmp',
       0x45:'pop',0x86:'dup',0x9C:'ret',0x9D:'exit',0x9E:'popz',0xB6:'b',0xB7:'bt',0xB8:'bf',
       0xBA:'pushenv',0xBB:'popenv',0xC0:'push',0xC1:'pushloc',0xC2:'pushglb',0xC3:'pushbltn',
       0x84:'pushi',0xD9:'call',0x99:'callv',0xFF:'break'}
T = {0:'d',1:'f',2:'i',3:'l',4:'b',5:'v',6:'s',7:'inst',0xF:'e'}
CMP = {1:'LT',2:'LE',3:'EQ',4:'NEQ',5:'GE',6:'GT'}
BRK = {-1:'chkindex',-2:'pushaf',-3:'popaf',-4:'pushac',-5:'setowner',-6:'isstaticok',
       -7:'setstatic',-8:'savearef',-9:'restorearef',-10:'chknullish',-11:'pushref'}
INST = {-1:'self',-2:'other',-3:'all',-4:'noone',-5:'global',-6:'builtin',-7:'local',
        -9:'stacktop',-15:'arg',-16:'static'}


class Data:
    def __init__(self, path):
        self.d = d = open(path, 'rb').read()
        self.chunks = {}
        p = 8
        while p < len(d):
            n = d[p:p+4].decode('latin1'); s = struct.unpack_from('<I', d, p+4)[0]
            self.chunks[n] = (p+8, s); p += 8 + s
        self.strings = self._list('STRG', lambda q: self.rawstr(q+4))
        self._refs()

    def u32(self, o): return struct.unpack_from('<I', self.d, o)[0]
    def i32(self, o): return struct.unpack_from('<i', self.d, o)[0]

    def rawstr(self, q):
        n = self.u32(q-4); return self.d[q:q+n].decode('utf8', 'replace')

    def _list(self, ch, f):
        o, _ = self.chunks[ch]; n = self.u32(o)
        return [f(self.u32(o+4+4*i)) for i in range(n)]

    def _refs(self):
        """Map instruction address -> name by walking VARI/FUNC occurrence chains."""
        self.var_at, self.fn_at = {}, {}
        o, s = self.chunks['VARI']; end = o + s; p = o + 12
        self.vars = []
        while p + 20 <= end:
            name, it, vid, occ, first = struct.unpack_from('<IiiIi', self.d, p); p += 20
            nm = self.rawstr(name); self.vars.append((nm, it, vid))
            a = first
            for k in range(occ):
                if a < 0 or a + 8 > len(self.d): break
                self.var_at[a] = nm
                a += self.u32(a+4) & 0x07FFFFFF
        o, s = self.chunks['FUNC']; n = self.u32(o); p = o + 4
        for _ in range(n):
            name, occ, first = struct.unpack_from('<IIi', self.d, p); p += 12
            nm = self.rawstr(name); a = first - 4  # FUNC firstAddress points at the operand
            for k in range(occ):
                if a < 0 or a + 8 > len(self.d): break
                self.fn_at[a] = nm
                a += self.u32(a+4) & 0x07FFFFFF

    def code_entries(self):
        o, _ = self.chunks['CODE']; n = self.u32(o); out = []
        for i in range(n):
            e = self.u32(o+4+4*i)
            name = self.rawstr(self.u32(e)); ln = self.u32(e+4)
            loc, args = struct.unpack_from('<HH', self.d, e+8)
            rel = self.i32(e+12); off = self.u32(e+16)
            out.append(dict(name=name, len=ln, locals=loc, args=args & 0x7FFF,
                            blob=e+12+rel, off=off))
        return out

    def dis(self, start, length):
        d = self.d; p = start; end = start + length; lines = []
        while p < end:
            w = self.u32(p); op = w >> 24; t1 = (w >> 16) & 0xF; t2 = (w >> 20) & 0xF
            lo = w & 0xFFFF; slo = struct.unpack('<h', struct.pack('<H', lo))[0]
            nm = OPS.get(op, '?%02X' % op); a = p; p += 4; arg = ''
            if op in (0xB6, 0xB7, 0xB8, 0xBA, 0xBB):
                off = w & 0x7FFFFF
                if off & 0x400000: off -= 0x800000
                arg = 'L%X' % (a + off*4 - start) if not (op == 0xBB and w & 0x800000) else '<drop>'
            elif op in (0xC0, 0xC1, 0xC2, 0xC3, 0x84):
                if t1 == 5:
                    arg = '%s.%s' % (INST.get(slo, str(slo)), self.var_at.get(a, '?'))
                    kind = (self.u32(p) >> 24) & 0xF8
                    if kind == 0: arg += '[]'
                    p += 4
                elif t1 == 0xF: arg = str(slo)
                elif t1 == 2:
                    arg = ('[function]' + self.fn_at[a]) if a in self.fn_at else str(self.i32(p)); p += 4
                elif t1 == 1: arg = repr(struct.unpack_from('<f', d, p)[0]); p += 4
                elif t1 == 0: arg = repr(struct.unpack_from('<d', d, p)[0]); p += 8
                elif t1 == 3: arg = str(struct.unpack_from('<q', d, p)[0]); p += 8
                elif t1 == 4: arg = str(self.u32(p)); p += 4
                elif t1 == 6:
                    si = self.u32(p); p += 4
                    arg = repr(self.strings[si]) if si < len(self.strings) else '#%d' % si
                nm += '.' + T.get(t1, str(t1))
            elif op == 0x45:
                if t1 == 5 or t2 == 5 or True:
                    if w & 0xFFFF == 0xF5F5 or self.var_at.get(a) is None and t1 == 0xF:
                        arg = 'swap %d' % lo  # pop.e.v swap form
                    else:
                        arg = '%s.%s' % (INST.get(slo, str(slo)), self.var_at.get(a, '?')); p += 4
                nm += '.%s.%s' % (T.get(t1, t1), T.get(t2, t2))
            elif op == 0xD9:
                arg = '%s(argc=%d)' % (self.fn_at.get(a, '?'), lo); p += 4
            elif op == 0x15:
                arg = CMP.get((w >> 8) & 0xFF, '?'); nm += '.%s.%s' % (T.get(t1, t1), T.get(t2, t2))
            elif op == 0xFF:
                arg = BRK.get(slo, str(slo))
                if t1 == 2: arg += ' ' + (self.fn_at.get(a) or str(self.i32(p))); p += 4
            elif op == 0x86:
                arg = str(lo & 0xFF) + (' swap' if lo & 0xFF00 else ''); nm += '.' + T.get(t1, str(t1))
            elif op == 0x99:
                arg = 'argc=%d' % lo
            else:
                nm += '.%s' % T.get(t1, t1) + ('.%s' % T.get(t2, t2) if op in (0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x13,0x14) else '')
            lines.append('L%-6X %-16s %s' % (a - start, nm, arg))
        return lines


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    out = sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else None
    if out: a = [x for x in a if x != out]
    D = Data(a[0]); rx = re.compile(a[1]) if len(a) > 1 else None
    ents = D.code_entries()
    blobs = {}
    for e in ents:
        if e['off'] == 0: blobs[e['blob']] = e
    for e in ents:
        if rx and not rx.search(e['name']): continue
        if e['off'] != 0: continue  # child function: shown inside parent
        kids = [k['name'] + '@L%X' % k['off'] for k in ents if k['blob'] == e['blob'] and k['off']]
        txt = '; %s  len=%d locals=%d args=%d\n' % (e['name'], e['len'], e['locals'], e['args'])
        if kids: txt += '; children: ' + ', '.join(kids) + '\n'
        txt += '\n'.join(D.dis(e['blob'], e['len'])) + '\n'
        if out:
            os.makedirs(out, exist_ok=True)
            open(os.path.join(out, e['name'][:150] + '.asm'), 'w', encoding='utf8').write(txt)
        else:
            sys.stdout.write(txt + '\n')


if __name__ == '__main__':
    main()
