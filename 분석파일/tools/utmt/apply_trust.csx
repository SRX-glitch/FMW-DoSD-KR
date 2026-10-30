// Custom mod (ours, not in FMWCB): permanent intra-unit trust for the combined units (SRX-style).
// global combinedTrust (mods/Mechanics/CombinedTrust.json, Type 0, default OFF).
// calculate_pair only counts OTHER units (8 neighbours + pair partner), so the 3 pilots riding one combined unit
// never get the trust they have with each other in Data_Trust (Sunny/Luna/Star and Lunasa/Merlin/Lyrica: L=2 each).
// ON: for the Three Fairies / Prismriver Sisters, the other pilots of the same unit are counted as companions
//     -> trust level +4 (hit/evade +18%, dmg dealt/taken & crit 3%).  Seirensen / Ichirin (also multi-pilot) excluded.
// Data_Trust values are read at runtime (ObjData.TrustCharID), so Data_Trust addOns apply too.
using System.IO;

string W = Environment.GetEnvironmentVariable("FMW_W");
const string NAME = "gml_GlobalScript_calculate_pair";
var g = new GlobalDecompileContext(Data);
string src = new Underanalyzer.Decompiler.DecompileContext(g, Data.Code.ByName(NAME), Data.ToolInfo.DecompilerSettings).DecompileToString();
string nl = src.Contains("\r\n") ? "\r\n" : "\n";
string N(string s) => s.Replace("\n", nl);

void Swap(string from, string to)
{
    from = N(from); to = N(to);
    int n = 0, i = 0;
    while ((i = src.IndexOf(from, i, StringComparison.Ordinal)) >= 0) { n++; i += from.Length; }
    if (n != 1) throw new Exception($"apply_trust: expected 1 match, got {n}: {from.Substring(0, Math.Min(60, from.Length))}");
    src = src.Replace(from, to);
}

Swap("    ds_list_destroy(list);\n    ds_list_destroy(l_uid);\n",
     "    if (optionalOf(\"combinedTrust\", false))\n" +
     "    {\n" +
     "        var ctCode = arg0.pilot_code[arg1][arg2];\n" +
     "        var ctData = array_get(array_get(arg0.pilot_data0, arg1), arg2);\n" +
     "        if (string_count(\"|\" + ctCode + \"|\", \"|Sunny|Luna|Star|Lunasa|Merlin|Lyrica|\") > 0 && ds_map_exists(ObjData.TrustCharID, ctData))\n" +
     "        {\n" +
     "            var ctList = ds_map_find_value(ObjData.TrustCharID, ctData);\n" +
     "            for (var ctK = 0; ctK < arg0.NumPilots[arg1]; ctK += 1)\n" +
     "            {\n" +
     "                if (ctK != arg2)\n" +
     "                {\n" +
     "                    for (var ctJ = 0; ctJ < ds_list_size(ctList); ctJ += 1)\n" +
     "                    {\n" +
     "                        if (array_get(ds_list_find_value(ctList, ctJ), 0) == arg0.pilot_code[arg1][ctK])\n" +
     "                        {\n" +
     "                            lv += array_get(ds_list_find_value(ctList, ctJ), 1);\n" +
     "                        }\n" +
     "                    }\n" +
     "                }\n" +
     "            }\n" +
     "        }\n" +
     "    }\n" +
     "    ds_list_destroy(list);\n    ds_list_destroy(l_uid);\n");

File.WriteAllText(Path.Combine(W, "build", NAME + ".patched.gml"), src);
var grp = new UndertaleModLib.Compiler.CodeImportGroup(Data);
grp.QueueReplace(NAME, src);
grp.Import();
Console.WriteLine("apply_trust: calculate_pair patched (toggle combinedTrust) and recompiled");
