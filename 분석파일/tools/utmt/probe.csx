// Probe: decompile KR logic-changed scripts, check sprite/font coverage between MOD (Data) and KR.
using System.IO;
using System.Linq;
using UndertaleModLib.Util;

string W = Environment.GetEnvironmentVariable("FMW_W");
UndertaleData KR;
using (var s = new FileStream(Path.Combine(W, "orig", "data.win"), FileMode.Open, FileAccess.Read))
    KR = UndertaleIO.Read(s);

var outDir = Path.Combine(W, "survey", "kr_gml");
Directory.CreateDirectory(outDir);
var g = new GlobalDecompileContext(KR);
foreach (var n in new[] { "gml_GlobalScript_UI_status_weapon", "gml_Object_ObjResult_Create_0" })
{
    var c = KR.Code.ByName(n);
    File.WriteAllText(Path.Combine(outDir, n + ".gml"),
        new Underanalyzer.Decompiler.DecompileContext(g, c, KR.ToolInfo.DecompilerSettings).DecompileToString());
}
var gm = new GlobalDecompileContext(Data);
foreach (var n in new[] { "gml_GlobalScript_UI_status_weapon", "gml_Object_ObjResult_Create_0" })
{
    var c = Data.Code.ByName(n);
    File.WriteAllText(Path.Combine(outDir, n + ".mod.gml"),
        new Underanalyzer.Decompiler.DecompileContext(gm, c, Data.ToolInfo.DecompilerSettings).DecompileToString());
}

int miss = 0, frameMismatch = 0;
foreach (var sp in Data.Sprites)
{
    var k = KR.Sprites.ByName(sp.Name.Content);
    if (k == null) { miss++; Console.WriteLine("missing in KR: " + sp.Name.Content); continue; }
    if (k.Textures.Count != sp.Textures.Count) { frameMismatch++; Console.WriteLine("frames differ: " + sp.Name.Content); }
}
Console.WriteLine($"sprites MOD={Data.Sprites.Count} KR={KR.Sprites.Count} missing={miss} frameMismatch={frameMismatch}");
foreach (var f in Data.Fonts) Console.WriteLine($"font {f.Name.Content} KR={(KR.Fonts.ByName(f.Name.Content) != null)}");
Console.WriteLine($"EMBI MOD={Data.EmbeddedImages?.Count} KR={KR.EmbeddedImages?.Count}; TGIN MOD={Data.TextureGroupInfo?.Count} KR={KR.TextureGroupInfo?.Count}");
foreach (var t in KR.TextureGroupInfo) Console.WriteLine($"TGIN {t.Name?.Content}: pages={t.TexturePages.Count} sprites={t.Sprites.Count} fonts={t.Fonts.Count}");
foreach (var t in Data.TextureGroupInfo) Console.WriteLine($"TGIN(MOD) {t.Name?.Content}: pages={t.TexturePages.Count} sprites={t.Sprites.Count} fonts={t.Fonts.Count}");
foreach (var e in Data.EmbeddedImages) Console.WriteLine($"EMBI {e.Name.Content}");
