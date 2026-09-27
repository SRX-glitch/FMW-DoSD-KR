// Translate mod-added strings in data.win (Data = merged MOD+KR) from translate/ko_code.json.
// Only push.s instructions inside the named script (and its child functions) are touched.
using System.IO;
using System.Linq;
using System.Text.Json;
using UndertaleModLib.Models;

string W = Environment.GetEnvironmentVariable("FMW_W");
var doc = JsonDocument.Parse(File.ReadAllText(Path.Combine(W, "translate", "ko_code.json")));
var log = new List<string>();
int total = 0;
foreach (var sc in doc.RootElement.EnumerateObject())
{
    if (sc.Name.StartsWith("_")) continue;
    var code = Data.Code.ByName(sc.Name);
    if (code == null) { log.Add("!! missing code " + sc.Name); continue; }
    var map = sc.Value.EnumerateObject().ToDictionary(p => p.Name, p => p.Value.GetString());
    var seen = new HashSet<string>();
    foreach (var ins in code.Instructions)
    {
        if (ins.Kind != UndertaleInstruction.Opcode.Push || ins.Type1 != UndertaleInstruction.DataType.String) continue;
        var s = ins.ValueString.Resource.Content;
        if (!map.TryGetValue(s, out var ko)) continue;
        ins.ValueString = new UndertaleResourceById<UndertaleString, UndertaleChunkSTRG> { Resource = Data.Strings.MakeString(ko) };
        seen.Add(s); total++;
    }
    foreach (var k in map.Keys.Where(k => !seen.Contains(k))) log.Add($"!! {sc.Name}: not found '{k}'");
    log.Add($"{sc.Name}: {seen.Count}/{map.Count} keys");
}
// integer constant patches: pushi.e <old> right after a call to string_length
if (doc.RootElement.TryGetProperty("_int_patches", out var ip))
    foreach (var sc in ip.EnumerateObject())
    {
        var ins = Data.Code.ByName(sc.Name).Instructions;
        var m = sc.Value.EnumerateObject().ToDictionary(p => short.Parse(p.Name), p => (short)p.Value.GetInt32());
        int n = 0;
        for (int i = 1; i < ins.Count; i++)
        {
            var prev = ins[i - 1]; var cur = ins[i];
            if (prev.Kind == UndertaleInstruction.Opcode.Call && prev.ValueFunction?.Name?.Content == "string_length"
                && cur.Kind == UndertaleInstruction.Opcode.PushI && cur.Type1 == UndertaleInstruction.DataType.Int16
                && cur.ValueShort is short v && m.ContainsKey(v))
            { cur.ValueShort = m[v]; n++; }
        }
        log.Add($"{sc.Name}: {n} int constants patched (expected {m.Count})");
    }
log.Add("total push.s replaced: " + total);
File.WriteAllLines(Path.Combine(W, "build", "apply_ko.log"), log);
foreach (var l in log) Console.WriteLine(l);
