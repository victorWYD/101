# Cape redesign (`mt010131` / `mt010133`)

WYD (With Your Destiny) mantle assets redesigned to a crimson / gold dragon cape.

| File | Role |
| --- | --- |
| `mt010131.msh` | Original cape mesh (geometry unchanged) |
| `mt010133.wys` | Rebuilt diffuse texture (WS10 + BC3/DXT5 mip chain) |
| `mt010133_original.wys` | Backup of the pre-edit texture |
| `mt010133_diffuse_redesign.png` | Editable 512×512 source for the new look |
| `mt010133_original_diffuse.png` | Decoded original texture (reference) |

Rebuild the `.wys` after editing the PNG:

```bash
python3 tools/rebuild_wys_from_png.py \
  --png mesh/mt010133_diffuse_redesign.png \
  --template-wys mesh/mt010133_original.wys \
  --out mesh/mt010133.wys
```
