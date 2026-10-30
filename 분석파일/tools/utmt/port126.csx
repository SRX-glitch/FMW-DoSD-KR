// Port the EN 1.2.4 -> 1.2.6 game update onto the FMWCB-modded data.win (Data = mod applied to EN 1.2.4).
// Inputs: survey/merge126b/*.gml  (3-way merged base=EN1.2.4 / ours=mod / theirs=EN1.2.6, conflicts resolved by
//         tools/resolve_126.py).  Also copies the FEAT chunk (feature flags) from EN 1.2.6.
using System.IO;
using System.Linq;
using System.Reflection;

string W = Environment.GetEnvironmentVariable("FMW_W");
var grp = new UndertaleModLib.Compiler.CodeImportGroup(Data);
int n = 0;
foreach (var f in Directory.GetFiles(Path.Combine(W, "survey", "merge126b"), "*.gml"))
{
    var name = Path.GetFileNameWithoutExtension(f);
    var src = File.ReadAllText(f);
    if (src.Contains("<<<<<<<")) throw new Exception("unresolved conflict in " + name);
    grp.QueueReplace(name, src);
    n++;
}
grp.Import();
Console.WriteLine($"port126: {n} scripts recompiled");

UndertaleData E6;
using (var s = new FileStream(Path.Combine(W, "orig_en_new", "data.win"), FileMode.Open, FileAccess.Read))
    E6 = UndertaleIO.Read(s);
var prop = typeof(UndertaleData).GetProperty("FEAT") ?? typeof(UndertaleData).GetProperties().FirstOrDefault(p => p.PropertyType.Name.Contains("Feature"));
if (prop != null)
{
    var dst = prop.GetValue(Data); var src = prop.GetValue(E6);
    var listProp = src.GetType().GetProperties().First(p => p.PropertyType.Name.StartsWith("UndertaleSimpleListString") || p.PropertyType.Name.Contains("List"));
    var dl = (System.Collections.IList)listProp.GetValue(dst); var sl = (System.Collections.IList)listProp.GetValue(src);
    dl.Clear();
    foreach (var x in sl) dl.Add(Data.Strings.MakeString(((UndertaleString)x).Content));
    Console.WriteLine("port126: FEAT = " + string.Join(",", sl.Cast<UndertaleString>().Select(x => x.Content)));
}
else Console.WriteLine("port126: FEAT property not found (skipped)");
