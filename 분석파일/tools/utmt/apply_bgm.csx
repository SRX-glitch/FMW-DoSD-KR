// BGM loop fix as a mod toggle (ours): global bgmLoopFix (mods/BugFixes/BGMLoopFix.json, Type 0, default OFF).
// Vanilla SBDS2 loops streams by polling the track position once per frame (end step) and seeking back
// "one frame early" -> the tail is clipped every loop, and on a frame hitch the stream ends first and is
// restarted as a new instance ("unexpected termination") -> audible cut.
// ON : infinite loops (LOOP_COUNT_MAX < 0) use the runner's native sample-accurate loop points
//      (audio_sound_loop_start/_end + audio_sound_loop); the per-frame wind-back is skipped while active.
// OFF: native loop flag is cleared -> original behaviour.  SBDS2_Update re-syncs every frame, so toggling
//      in the mod menu applies to the BGM that is already playing.
// Finite loop counts (story events: SetLoopCount 0 = play to the end) always use the original logic.
using System.IO;
using System.Linq;

string W = Environment.GetEnvironmentVariable("FMW_W");
var g = new GlobalDecompileContext(Data);
string src = "", nl = "\n";
string Load(string name)
{
    var s = new Underanalyzer.Decompiler.DecompileContext(g, Data.Code.ByName(name), Data.ToolInfo.DecompilerSettings).DecompileToString();
    nl = s.Contains("\r\n") ? "\r\n" : "\n";
    return s;
}
string N(string s) => s.Replace("\n", nl);
void Swap(string from, string to)
{
    from = N(from); to = N(to);
    int n = 0, i = 0;
    while ((i = src.IndexOf(from, i, StringComparison.Ordinal)) >= 0) { n++; i += from.Length; }
    if (n != 1) throw new Exception($"apply_bgm: expected 1 match, got {n}: {from.Substring(0, Math.Min(70, from.Length))}");
    src = src.Replace(from, to);
}
const string ON = "optionalOf(\"bgmLoopFix\", false)";
var grp = new UndertaleModLib.Compiler.CodeImportGroup(Data);

// ---------------- SBDS2_Sound ----------------
src = Load("gml_GlobalScript_SBDS2_Sound");
// loop points are always mirrored to the native side (inert unless the native loop flag is set)
Swap("function SBDS2_SoundSetLoopPoints(arg0, arg1, arg2)\n{\n" +
     "    if (arg1 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 0, arg1);\n    }\n" +
     "    if (arg2 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 1, arg2);\n    }\n" +
     "    return true;\n}",
     "function SBDS2_SoundSetLoopPoints(arg0, arg1, arg2)\n{\n" +
     "    if (arg1 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 0, arg1);\n    }\n" +
     "    if (arg2 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 1, arg2);\n    }\n" +
     "    audio_sound_loop_start(arg0.SOUND, array_get(arg0.LOOP_POINTS, 0));\n" +
     "    audio_sound_loop_end(arg0.SOUND, array_get(arg0.LOOP_POINTS, 1));\n" +
     "    return true;\n}");
Swap("    var inst_obj = SBDS2_SoundPlay(arg0, arg1);\n    inst_obj.LOOP_COUNT_MAX = -1;\n    return inst_obj;",
     "    var inst_obj = SBDS2_SoundPlay(arg0, arg1);\n    inst_obj.LOOP_COUNT_MAX = -1;\n" +
     "    audio_sound_loop_start(inst_obj.INSTANCE, array_get(inst_obj.LOOP_POINTS, 0));\n" +
     "    audio_sound_loop_end(inst_obj.INSTANCE, array_get(inst_obj.LOOP_POINTS, 1));\n" +
     "    audio_sound_loop(inst_obj.INSTANCE, " + ON + ");\n" +
     "    return inst_obj;");
Swap("            var pos = audio_sound_get_track_position(inst);\n",
     "            var bgmNative = " + ON + " && inst_obj.LOOP_COUNT_MAX < 0;\n" +
     "            if (audio_is_playing(inst) && audio_sound_get_loop(inst) != bgmNative)\n" +
     "            {\n" +
     "                audio_sound_loop(inst, bgmNative);\n" +
     "            }\n" +
     "            var pos = audio_sound_get_track_position(inst);\n");
Swap("            if ((pos + (1 / room_speed)) > array_get(inst_obj.LOOP_POINTS, 1) || !audio_is_playing(inst) || pos == 0)",
     "            if (!(bgmNative && audio_is_playing(inst)) && ((pos + (1 / room_speed)) > array_get(inst_obj.LOOP_POINTS, 1) || !audio_is_playing(inst) || pos == 0))");
Swap("                        inst_obj.INSTANCE = new_inst;\n",
     "                        inst_obj.INSTANCE = new_inst;\n" +
     "                        if (bgmNative)\n" +
     "                        {\n" +
     "                            audio_sound_loop_start(new_inst, array_get(inst_obj.LOOP_POINTS, 0));\n" +
     "                            audio_sound_loop_end(new_inst, array_get(inst_obj.LOOP_POINTS, 1));\n" +
     "                            audio_sound_loop(new_inst, true);\n" +
     "                        }\n");
File.WriteAllText(Path.Combine(W, "build", "gml_GlobalScript_SBDS2_Sound.patched.gml"), src);
grp.QueueReplace("gml_GlobalScript_SBDS2_Sound", src);

// ---------------- SBDS2_Instance ----------------
src = Load("gml_GlobalScript_SBDS2_Instance");
Swap("function SBDS2_InstanceSetLoopCount(arg0, arg1)\n{\n    arg0.LOOP_COUNT_MAX = arg1;\n",
     "function SBDS2_InstanceSetLoopCount(arg0, arg1)\n{\n    arg0.LOOP_COUNT_MAX = arg1;\n" +
     "    audio_sound_loop(arg0.INSTANCE, arg1 < 0 && " + ON + ");\n");
Swap("function SBDS2_InstanceSetLoopPoints(arg0, arg1, arg2)\n{\n" +
     "    if (arg1 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 0, arg1);\n    }\n" +
     "    if (arg2 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 1, arg2);\n    }\n" +
     "    return true;\n}",
     "function SBDS2_InstanceSetLoopPoints(arg0, arg1, arg2)\n{\n" +
     "    if (arg1 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 0, arg1);\n    }\n" +
     "    if (arg2 >= 0)\n    {\n        array_set(arg0.LOOP_POINTS, 1, arg2);\n    }\n" +
     "    audio_sound_loop_start(arg0.INSTANCE, array_get(arg0.LOOP_POINTS, 0));\n" +
     "    audio_sound_loop_end(arg0.INSTANCE, array_get(arg0.LOOP_POINTS, 1));\n" +
     "    return true;\n}");
File.WriteAllText(Path.Combine(W, "build", "gml_GlobalScript_SBDS2_Instance.patched.gml"), src);
grp.QueueReplace("gml_GlobalScript_SBDS2_Instance", src);

grp.Import();
Console.WriteLine("apply_bgm: SBDS2_Sound, SBDS2_Instance patched (toggle bgmLoopFix) and recompiled");
