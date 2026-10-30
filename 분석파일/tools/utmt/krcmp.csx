// compare visual layer of Data (new KR) against old KR: sprites/fonts by rendered pixels
using System.IO; using System.Linq; using System.Security.Cryptography; using UndertaleModLib.Util;
string W = Environment.GetEnvironmentVariable("FMW_W");
UndertaleData O; using (var s = new FileStream(Path.Combine(W,"orig","data.win"), FileMode.Open, FileAccess.Read)) O = UndertaleIO.Read(s);
var tw = new TextureWorker(); var tw2 = new TextureWorker();
string H(UndertaleTexturePageItem it, TextureWorker t){ if(it==null) return "null"; using var img = t.GetTextureFor(it, "x"); return Convert.ToHexString(SHA1.HashData(img.ToByteArray(ImageMagick.MagickFormat.Rgba))).Substring(0,12); }
int diff=0, same=0; var names=new List<string>();
foreach (var sp in Data.Sprites){ var o=O.Sprites.ByName(sp.Name.Content); if(o==null){names.Add("NEW "+sp.Name.Content);continue;}
  bool d=false; for(int i=0;i<sp.Textures.Count;i++){ if(H(sp.Textures[i].Texture,tw)!=H(o.Textures[i].Texture,tw2)){d=true;break;} }
  if(d){diff++; names.Add("DIFF "+sp.Name.Content);} else same++; }
foreach (var sp in O.Sprites) if (Data.Sprites.ByName(sp.Name.Content)==null) names.Add("GONE "+sp.Name.Content);
Console.WriteLine($"sprites same={same} diff={diff}"); foreach(var n in names.Take(60)) Console.WriteLine(n);
foreach (var f in Data.Fonts){ var o=O.Fonts.ByName(f.Name.Content); bool g = f.Glyphs.Count==o.Glyphs.Count && f.Glyphs.Zip(o.Glyphs).All(p=>p.First.Character==p.Second.Character&&p.First.SourceWidth==p.Second.SourceWidth&&p.First.Shift==p.Second.Shift&&p.First.Offset==p.Second.Offset);
  Console.WriteLine($"font {f.Name.Content}: glyphs {f.Glyphs.Count}/{o.Glyphs.Count} metrics_same={g} tex={(H(f.Texture,tw)==H(o.Texture,tw2))}"); }
