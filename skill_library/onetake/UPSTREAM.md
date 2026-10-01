# onetake: copia local recortada

| | |
| :--- | :--- |
| Origen | https://github.com/feitangyuan/onetake |
| Commit fijado | `cf09bde3e392c9aa32c4157f80cdbe1fa556685e` (2026-09-29) |
| Autor | Patrick (feitangyuan) |
| Licencia | PolyForm Noncommercial 1.0.0 (`LICENSE`, con su línea `Required Notice`) |
| Incorporada | 2026-10-01 |

## Alcance de la licencia

Uso no comercial. La UGR, como institución educativa, entra en el uso permitido: docencia, demos de
las webs de QFDOS y Genyo Fusion, material del máster. **DestiNA Genomics no**: un vídeo de producto
para la empresa es uso comercial. Para eso están `brag` y `brag-slim`.

La licencia exige que cualquier copia lleve `LICENSE` y la línea `Required Notice`. No los borres.

## Qué se ha quitado

Se conservan 69 de los 104 ficheros (3,9 MB de unos 100 MB):

- `cases/*/*.mp4`: los diez vídeos terminados (unos 55 MB). Sí están los README de cada caso.
- `assets/`: GIF de demostración, `hero.gif` y logotipos (unos 17 MB).
- `README.md` y `.gitignore` del repositorio original. `SKILL.md` cubre todo el método.

## Cambio local

`SKILL.md` lleva un bloque añadido bajo el título con la licencia, lo que falta y las notas para
Windows. Si actualizas, vuelve a ponerlo.

## Dependencias

Ya instaladas: Node y ffmpeg. Faltan en Python 3.13 (`sync-pull` avisa):

```powershell
py -3.13 -m pip install --user playwright numpy scipy pillow matplotlib fonttools brotli
py -3.13 -m playwright install chromium
```

Opcionales: `opencv-python` (análisis de referencias), `faster-whisper` y Kokoro (`kokoro-onnx`,
`soundfile`) para narración.

## Actualizar a otro commit

Desde la raíz del repo, en Git Bash, con el SHA nuevo en `SHA`:

```bash
SHA=<commit>; DEST=skill_library/onetake
gh api "repos/feitangyuan/onetake/git/trees/$SHA?recursive=1" \
  --jq '.tree[] | select(.type=="blob") | .path' \
  | grep -vE '^(assets/|README\.md$|\.gitignore$)|^cases/.*\.mp4$' \
  | while read -r p; do mkdir -p "$DEST/$(dirname "$p")"; \
      gh api -H "Accept: application/vnd.github.raw" "repos/feitangyuan/onetake/contents/$p?ref=$SHA" > "$DEST/$p"; done
```

Después, restaura el bloque local de `SKILL.md` y actualiza el SHA de esta tabla.
