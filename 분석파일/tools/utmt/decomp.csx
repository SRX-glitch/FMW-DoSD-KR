using System.IO; using System.Linq; using System.Text.RegularExpressions;
string W = Environment.GetEnvironmentVariable("FMW_W"); string rx = Environment.GetEnvironmentVariable("FMW_RX");
string outDir = Path.Combine(W, "survey", Environment.GetEnvironmentVariable("FMW_OUT") ?? "gml"); Directory.CreateDirectory(outDir);
var g = new GlobalDecompileContext(Data);
foreach (var c in Data.Code.Where(c => c.ParentEntry == null && Regex.IsMatch(c.Name.Content, rx)))
    File.WriteAllText(Path.Combine(outDir, c.Name.Content + ".gml"), new Underanalyzer.Decompiler.DecompileContext(g, c, Data.ToolInfo.DecompilerSettings).DecompileToString());
