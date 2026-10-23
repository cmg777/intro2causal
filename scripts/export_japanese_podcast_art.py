"""Preserve imagegen originals and perform only approved RGB/size export normalization."""
import hashlib
import json
from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'publishing/spotify-jpn/artwork'


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sources = json.loads((ART / 'generated-sources.json').read_text())
    directory = Path(sources['generation_directory'])
    exported = []
    for name, filename in sources['selected'].items():
        original = ART / f'{name}-original.png'
        if original.exists():
            if file_hash(original) != file_hash(directory / filename):
                raise ValueError(f'Original collision: {name}')
        else:
            shutil.copy2(directory / filename, original)
        output = ART / f'{name}.png'
        with Image.open(original) as source:
            native = list(source.size)
            if native[0] != native[1]:
                raise ValueError(f'Non-square source: {name}')
            # This is mechanical export only; conceptual/text edits use imagegen.
            final = source.convert('RGB').resize((2048, 2048), Image.Resampling.LANCZOS)
            final.save(output)
        exported.append({'id': name, 'original': str(original.relative_to(ROOT)),
                         'final': str(output.relative_to(ROOT)), 'native_size': native,
                         'export_size': [2048, 2048], 'mode': 'RGB', 'sha256': file_hash(output),
                         'normalization': 'RGB conversion and Lanczos resize; no new native detail'})
    (ART / 'exports.json').write_text(json.dumps(exported, ensure_ascii=False, indent=2) + '\n')
    print(f'Exported {len(exported)} covers, preserving native originals')


if __name__ == '__main__':
    main()
