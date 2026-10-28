"""Safety checks for transcript validation and publication deduplication."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from prepare_spotify import prepare, validate_artwork, validate_vtt


class PreparationTests(unittest.TestCase):
    def test_small_artwork_rejected(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'small.png'
            Image.new('RGB', (100, 100)).save(path)
            with self.assertRaisesRegex(ValueError, 'Artwork must'):
                validate_artwork(path)

    def test_overlapping_cues_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.vtt'
            path.write_text('WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nA\n\n'
                            '00:00:01.000 --> 00:00:03.000\nB\n')
            with self.assertRaisesRegex(ValueError, 'Nonmonotonic'):
                validate_vtt(path, 3)

    def test_empty_or_truncated_transcript_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.vtt'
            for text in ('WEBVTT\n', 'WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nA\n'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    validate_vtt(path, 10)

    def test_published_skip_and_changed_assets_guard(self):
        config = Path(__file__).resolve().parents[1] / 'publishing/spotify/project.json'
        with tempfile.TemporaryDirectory() as tmp, patch('prepare_spotify.validate_artwork'):
            state = Path(tmp) / 'state.json'
            manifest = prepare(config, state)
            records = {e['id']: dict(status='published', audio_sha256=e['audio_sha256'],
                       transcript_sha256=e['transcript_sha256']) for e in manifest['episodes']}
            saved = dict(project_id=manifest['project_id'], episodes=records)
            state.write_text(json.dumps(saved))
            self.assertTrue(all(e['action'] == 'skip_published' for e in prepare(config, state)['episodes']))
            from PIL import Image
            art = Path(tmp) / 'episode.png'
            Image.new('RGB', (1400, 1400)).save(art)
            changed_config = json.loads(config.read_text())
            changed_config['root'] = str(config.parents[2])
            changed_config['episodes'] = changed_config['episodes'][:1]
            changed_config['episodes'][0]['artwork'] = str(art)
            art_config = Path(tmp) / 'project.json'
            art_config.write_text(json.dumps(changed_config))
            changed = prepare(art_config, state)['episodes'][0]
            self.assertEqual(changed['action'], 'inspect_artwork_update')
            records[changed['id']]['artwork_sha256'] = changed['artwork_sha256']
            state.write_text(json.dumps(saved))
            self.assertEqual(prepare(art_config, state)['episodes'][0]['action'], 'skip_published')
            records[next(iter(records))]['audio_sha256'] = 'changed'
            state.write_text(json.dumps(saved))
            with self.assertRaisesRegex(ValueError, 'Published assets changed'):
                prepare(config, state)
            saved['project_id'] = 'another-project'
            state.write_text(json.dumps(saved))
            with self.assertRaisesRegex(ValueError, 'different project'):
                prepare(config, state)


if __name__ == '__main__':
    unittest.main()
