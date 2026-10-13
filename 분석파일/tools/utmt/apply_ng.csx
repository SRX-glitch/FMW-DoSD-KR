// Custom mod (ours, not in FMWCB): NG+ (Dream Mode) carry-over unit count.
// global ngUnitCount (mods/Modifiers/NGUnitCount.json, Type 2 = [Value, Min, Max]):
//   6 = vanilla, 0 = unlimited.  Confirm is allowed with 1..cap units (vanilla: exactly 6).
// Only gml_GlobalScript_UI_NG_list changes; every other script that reads global.u_code0 only tests membership.
using System.IO;
using System.Linq;

string W = Environment.GetEnvironmentVariable("FMW_W");
const string NAME = "gml_GlobalScript_UI_NG_list";
var g = new GlobalDecompileContext(Data);
string src = new Underanalyzer.Decompiler.DecompileContext(g, Data.Code.ByName(NAME), Data.ToolInfo.DecompilerSettings).DecompileToString();
string nl = src.Contains("\r\n") ? "\r\n" : "\n";
string N(string s) => s.Replace("\n", nl);

void Swap(string from, string to)
{
    from = N(from); to = N(to);
    int n = 0, i = 0;
    while ((i = src.IndexOf(from, i, StringComparison.Ordinal)) >= 0) { n++; i += from.Length; }
    if (n != 1) throw new Exception($"apply_ng: expected 1 match, got {n}: {from.Substring(0, Math.Min(60, from.Length))}");
    src = src.Replace(from, to);
}

Swap("function UI_NG_list(arg0, arg1, arg2)\n{\n",
     "function UI_NG_list(arg0, arg1, arg2)\n{\n" +
     "    var ngCap = optionalOf(\"ngUnitCount\", [6, 0, 99]);\n" +
     "    if (is_array(ngCap))\n    {\n        ngCap = ngCap[0];\n    }\n");
Swap("ds_list_size(global.u_code0) > 0, ds_list_size(global.u_code0) == 6], 1);",
     "ds_list_size(global.u_code0) > 0, ds_list_size(global.u_code0) >= 1], 1);");
Swap("else if (ds_list_size(global.u_code0) < 6)",
     "else if (ngCap <= 0 || ds_list_size(global.u_code0) < ngCap)");
Swap("        if (ds_list_size(global.u_code0) == 6)\n",
     "        if (ds_list_size(global.u_code0) >= 1)\n");

// selected-units strip: keep the vanilla 6 big slots up to 6, otherwise 2 rows that shrink to fit
string loop =
"    for (var i = 0; i < 6; i += 1)\n" +
"    {\n" +
"        var x1 = arg0 + 60 + (200 * i);\n" +
"        var y1 = arg1 + 485 + 10;\n" +
"        draw_sprite_ext(ef_NG_light, 0, x1 + 72, y1 + 164, 0.5, 0.15, 0, c_white, 0.6);\n" +
"        if (i < ds_list_size(global.u_code0))\n" +
"        {\n" +
"            var code = ds_list_find_value(global.u_code0, i);\n" +
"            var spr = resource_load(code + \"01\", \"sprite\", 1, 0, false, false);\n" +
"            if (spr != -1)\n" +
"            {\n" +
"                draw_sprite_outlined(spr, 0, x1 + 72, y1 + 72, 2, 2, 0, 16777215, 16777215, 1, 2);\n" +
"            }\n" +
"        }\n" +
"    }\n";
string many =
"    var ngN = ds_list_size(global.u_code0);\n" +
"    if (ngN <= 6)\n" +
"    {\n" + string.Join("\n", loop.TrimEnd('\n').Split('\n').Select(l => "    " + l)) + "\n    }\n" +
"    else\n" +
"    {\n" +
"        var ngCols = ceil(ngN / 2);\n" +
"        var ngS = 1200 / ngCols;\n" +
"        var ngSc = min(1, ngS / 100);\n" +
"        for (var i = 0; i < ngN; i += 1)\n" +
"        {\n" +
"            var x1 = arg0 + 60 + (ngS * (i mod ngCols)) + (ngS * 0.36);\n" +
"            var y1 = arg1 + 535 + (95 * (i div ngCols));\n" +
"            var code = ds_list_find_value(global.u_code0, i);\n" +
"            var spr = resource_load(code + \"01\", \"sprite\", 1, 0, false, false);\n" +
"            if (spr != -1)\n" +
"            {\n" +
"                draw_sprite_outlined(spr, 0, x1, y1, ngSc, ngSc, 0, 16777215, 16777215, 1, 1);\n" +
"            }\n" +
"        }\n" +
"    }\n";
Swap(loop, many);

File.WriteAllText(Path.Combine(W, "build", NAME + ".patched.gml"), src);
var grp = new UndertaleModLib.Compiler.CodeImportGroup(Data);
grp.QueueReplace(NAME, src);
grp.Import();
Console.WriteLine("apply_ng: " + NAME + " patched and recompiled");
