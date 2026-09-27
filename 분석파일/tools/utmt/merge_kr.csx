// Merge the Korean patch into the FMWCB-modded data.win (Data = MOD).
//   1) visual layer: take KR's texture pages + page items; remap every sprite frame / font / EMBI / TGIN
//      of MOD to the KR item of the same asset name (MOD's visual layer == EN's, KR's is a superset)
//   2) fonts: copy KR font properties + glyphs
//   3) string-only scripts: EN->KR push.s pairs aligned per script, applied to MOD's code of the same name
//   4) logic scripts (not touched by the mod): replace with KR's decompiled GML
// env: FMW_W = workspace root
using System.IO;
using System.Linq;
using UndertaleModLib.Util;
using UndertaleModLib.Models;

string W = Environment.GetEnvironmentVariable("FMW_W");
UndertaleData Load(string rel)
{
    using var s = new FileStream(Path.Combine(W, rel), FileMode.Open, FileAccess.Read);
    return UndertaleIO.Read(s);
}
var KR = Load(Path.Combine("orig", "data.win"));
var EN = Load(Path.Combine("orig_en", "data.win"));
var log = new List<string>();

// ---------- 1) texture pages / page items ----------
var newTex = new List<UndertaleEmbeddedTexture>();
foreach (var t in KR.EmbeddedTextures)
{
    var n = new UndertaleEmbeddedTexture();
    n.Name = new UndertaleString(t.Name.Content);
    n.Scaled = t.Scaled;
    n.GeneratedMips = t.GeneratedMips;
    n.TextureWidth = t.TextureWidth; n.TextureHeight = t.TextureHeight;
    n.IndexInGroup = t.IndexInGroup;
    n.TextureData.Image = t.TextureData.Image;
    newTex.Add(n);
}
var itemMap = new Dictionary<UndertaleTexturePageItem, UndertaleTexturePageItem>();
var newItems = new List<UndertaleTexturePageItem>();
foreach (var it in KR.TexturePageItems)
{
    var n = new UndertaleTexturePageItem
    {
        SourceX = it.SourceX, SourceY = it.SourceY, SourceWidth = it.SourceWidth, SourceHeight = it.SourceHeight,
        TargetX = it.TargetX, TargetY = it.TargetY, TargetWidth = it.TargetWidth, TargetHeight = it.TargetHeight,
        BoundingWidth = it.BoundingWidth, BoundingHeight = it.BoundingHeight,
        TexturePage = newTex[KR.EmbeddedTextures.IndexOf(it.TexturePage)],
    };
    n.Name = new UndertaleString(it.Name?.Content ?? "PageItem");
    itemMap[it] = n; newItems.Add(n);
}
UndertaleTexturePageItem Map(UndertaleTexturePageItem k) => k == null ? null : itemMap[k];

int spr = 0;
foreach (var s in Data.Sprites)
{
    var k = KR.Sprites.ByName(s.Name.Content);
    for (int i = 0; i < s.Textures.Count; i++)
        s.Textures[i].Texture = Map(k.Textures[i].Texture);
    s.Width = k.Width; s.Height = k.Height;
    s.MarginLeft = k.MarginLeft; s.MarginRight = k.MarginRight; s.MarginTop = k.MarginTop; s.MarginBottom = k.MarginBottom;
    s.OriginX = k.OriginX; s.OriginY = k.OriginY;
    spr++;
}
foreach (var e in Data.EmbeddedImages)
    e.TextureEntry = Map(KR.EmbeddedImages.First(x => x.Name.Content == e.Name.Content).TextureEntry);

// ---------- 2) fonts ----------
foreach (var f in Data.Fonts)
{
    var k = KR.Fonts.ByName(f.Name.Content);
    f.DisplayName = Data.Strings.MakeString(k.DisplayName.Content);
    f.EmSize = k.EmSize; f.EmSizeIsFloat = k.EmSizeIsFloat;
    f.Bold = k.Bold; f.Italic = k.Italic; f.RangeStart = k.RangeStart; f.RangeEnd = k.RangeEnd;
    f.Charset = k.Charset; f.AntiAliasing = k.AntiAliasing; f.ScaleX = k.ScaleX; f.ScaleY = k.ScaleY;
    f.AscenderOffset = k.AscenderOffset; f.Ascender = k.Ascender; f.SDFSpread = k.SDFSpread; f.LineHeight = k.LineHeight;
    f.Texture = Map(k.Texture);
    f.Glyphs.Clear();
    foreach (var g in k.Glyphs)
    {
        var ng = new UndertaleFont.Glyph
        {
            Character = g.Character, SourceX = g.SourceX, SourceY = g.SourceY,
            SourceWidth = g.SourceWidth, SourceHeight = g.SourceHeight, Shift = g.Shift, Offset = g.Offset,
        };
        foreach (var kr in g.Kerning) ng.Kerning.Add(new UndertaleFont.Glyph.GlyphKerning { Character = kr.Character, ShiftModifier = kr.ShiftModifier });
        f.Glyphs.Add(ng);
    }
    log.Add($"font {f.Name.Content}: {f.Glyphs.Count} glyphs");
}

// texture group info: KR's page list, remapped
for (int gi = 0; gi < Data.TextureGroupInfo.Count; gi++)
{
    var mg = Data.TextureGroupInfo[gi]; var kg = KR.TextureGroupInfo[gi];
    mg.TexturePages.Clear();
    foreach (var p in kg.TexturePages)
        mg.TexturePages.Add(new UndertaleResourceById<UndertaleEmbeddedTexture, UndertaleChunkTXTR> { Resource = newTex[KR.EmbeddedTextures.IndexOf(p.Resource)] });
}

Data.TexturePageItems.Clear(); foreach (var n in newItems) Data.TexturePageItems.Add(n);
Data.EmbeddedTextures.Clear(); foreach (var n in newTex) Data.EmbeddedTextures.Add(n);
log.Add($"textures={Data.EmbeddedTextures.Count} items={Data.TexturePageItems.Count} sprites remapped={spr}");

// ---------- 3) string-only scripts ----------
IEnumerable<UndertaleInstruction> PushS(UndertaleCode c) =>
    c.Instructions.Where(i => i.Kind == UndertaleInstruction.Opcode.Push && i.Type1 == UndertaleInstruction.DataType.String);

string[] logic = { "gml_GlobalScript_UI_status_weapon", "gml_Object_ObjResult_Create_0" };
var scope = System.Text.Json.JsonDocument.Parse(File.ReadAllText(Path.Combine(W, "survey", "merge_scope.json")));
foreach (var nameEl in scope.RootElement.GetProperty("kr").EnumerateArray())
{
    string name = nameEl.GetString();
    if (logic.Contains(name)) continue;
    var ec = EN.Code.ByName(name); var kc = KR.Code.ByName(name); var mc = Data.Code.ByName(name);
    var es = PushS(ec).Select(i => i.ValueString.Resource.Content).ToList();
    var ks = PushS(kc).Select(i => i.ValueString.Resource.Content).ToList();
    if (es.Count != ks.Count) { log.Add($"!! {name}: push.s count EN {es.Count} KR {ks.Count} — skipped"); continue; }
    var queues = new Dictionary<string, Queue<string>>();
    for (int i = 0; i < es.Count; i++)
    {
        if (!queues.ContainsKey(es[i])) queues[es[i]] = new Queue<string>();
        queues[es[i]].Enqueue(ks[i]);
    }
    int done = 0; var mis = PushS(mc).ToList();
    foreach (var kv in queues)
    {
        var targets = mis.Where(i => i.ValueString.Resource.Content == kv.Key).ToList();
        var repl = kv.Value.ToList();
        if (repl.All(r => r == kv.Key)) continue;
        bool uniform = repl.Distinct().Count() == 1;
        if (targets.Count != repl.Count && !uniform)
        { log.Add($"!! {name}: '{kv.Key}' EN {repl.Count}x MOD {targets.Count}x, non-uniform — skipped"); continue; }
        for (int i = 0; i < targets.Count; i++)
        {
            var r = uniform ? repl[0] : repl[i];
            targets[i].ValueString = new UndertaleResourceById<UndertaleString, UndertaleChunkSTRG> { Resource = Data.Strings.MakeString(r) };
            done++;
        }
    }
    log.Add($"{name}: {done} strings replaced");
}

// ---------- 4) logic scripts ----------
var gctx = new GlobalDecompileContext(KR);
var grp = new UndertaleModLib.Compiler.CodeImportGroup(Data);
foreach (var n in logic)
{
    var gml = new Underanalyzer.Decompiler.DecompileContext(gctx, KR.Code.ByName(n), KR.ToolInfo.DecompilerSettings).DecompileToString();
    grp.QueueReplace(n, gml);
}
grp.Import();
log.Add("logic scripts recompiled: " + string.Join(", ", logic));

File.WriteAllLines(Path.Combine(W, "build", "merge_kr.log"), log);
foreach (var l in log) Console.WriteLine(l);
