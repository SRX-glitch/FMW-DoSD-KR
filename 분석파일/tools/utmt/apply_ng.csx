// Custom mod (ours, not in FMWCB): NG+ (Dream Mode) carry-over unit count.
// global ngUnitCount (mods/Modifiers/NGUnitCount.json, Type 2 = [Value, Min, Max]):
//   6 = vanilla, 0 = unlimited.  Confirm is allowed with 1..cap units (vanilla: exactly 6).
// Changes UI_NG_list (selection) + UI_NG_load/UI_NG_show_units (departure photo, fixed 6+Meko+Makura layout).
// Other readers of global.u_code0 only test membership.
// ⛔ 2026-10-13: the first version patched only UI_NG_list and crashed in UI_NG_load with != 6 units (user report).
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

// ---- departure "group photo" (UI_NG_load / UI_NG_show_units) assumed exactly 6 units:
//      slots 0-5 = carried units, 6 = Meko, 7 = Makura.  Fix the layout at 8 slots:
//      fewer than 6 -> empty slots (-1, already skipped by show_units), more than 6 -> first 6 shown.
string Load(string name)
{
    return new Underanalyzer.Decompiler.DecompileContext(g, Data.Code.ByName(name), Data.ToolInfo.DecompilerSettings).DecompileToString();
}

src = Load("gml_GlobalScript_UI_NG_load");
Swap("for (var i = 0; i < (ds_list_size(arg0) + 2); i += 1)",
     "for (var i = 0; i < 8; i += 1)");
Swap("        if (!debug)\n",
     "        if (i < 6 && i >= ds_list_size(arg0))\n" +
     "        {\n" +
     "            spr = -1;\n" +
     "            spr2 = -1;\n" +
     "        }\n" +
     "        else if (!debug)\n");
File.WriteAllText(Path.Combine(W, "build", "gml_GlobalScript_UI_NG_load.patched.gml"), src);
grp.QueueReplace("gml_GlobalScript_UI_NG_load", src);

src = Load("gml_GlobalScript_UI_NG_show_units");
Swap("var i = (ds_list_size(arg0) - 1) + (2 * arg1);",
     "var i = 5 + (2 * arg1);");
File.WriteAllText(Path.Combine(W, "build", "gml_GlobalScript_UI_NG_show_units.patched.gml"), src);
grp.QueueReplace("gml_GlobalScript_UI_NG_show_units", src);

grp.Import();
Console.WriteLine("apply_ng: UI_NG_list, UI_NG_load, UI_NG_show_units patched and recompiled");
