import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('jp_audio', Path(__file__).with_name('japanese_podcast_audio.py'))
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


class JapaneseAudioTests(unittest.TestCase):
    def test_sentence_chunks_preserve_every_character(self):
        turns = [{'speaker': 'HOST', 'section': '一', 'text': '保険を比べます。原因を考えます。'},
                 {'speaker': 'ECONOMIST', 'section': '一', 'text': 'もとの違いに注意します。'},
                 {'speaker': 'HOST', 'section': '二', 'text': '次の話です。'}]
        plan = audio.chunk_turns(turns, 15)
        self.assertEqual(''.join(t['text'] for p in plan for t in p), ''.join(t['text'] for t in turns))
        self.assertTrue(all(sum(audio.text_units(t['text']) for t in p) <= 15 for p in plan))
        self.assertTrue(all(len({t['section'] for t in p}) == 1 for p in plan))

    def test_decimal_pronunciation_preserves_zero(self):
        self.assertEqual(audio.spoken('4.01と3.70、差は0.31。'), '4点零一と3点七零、差は0点三一。')

    def test_budget_counts_failed_and_pending_requests(self):
        config = json.loads(audio.PRODUCTION.read_text())
        with tempfile.TemporaryDirectory() as folder:
            ledger = audio.Budget(Path(folder) / 'usage.json', config)
            reservation = ledger.reserve('日本語', 8192, 'one')
            self.assertGreater(ledger.committed, 0)
            restored = audio.Budget(ledger.path, config)
            self.assertEqual(restored.committed, ledger.committed)
            restored.production['gemini_budget_usd'] = restored.committed
            with self.assertRaisesRegex(ValueError, 'exceed'):
                restored.reserve('日本語', 8192, 'two')
            self.assertEqual(len(restored.data['requests']), 1)

    def test_missing_usage_keeps_reservation(self):
        config = json.loads(audio.PRODUCTION.read_text())
        with tempfile.TemporaryDirectory() as folder:
            ledger = audio.Budget(Path(folder) / 'usage.json', config)
            reservation = ledger.reserve('日本語', 8192, 'one')
            before = ledger.committed
            ledger.settle(reservation, None, None, 60)
            self.assertEqual(ledger.committed, before)

    def test_independent_clients_preserve_each_others_reservations(self):
        config = json.loads(audio.PRODUCTION.read_text())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'usage.json'
            first, second = audio.Budget(path, config), audio.Budget(path, config)
            one = first.reserve('日本語', 8192, 'one')
            two = second.reserve('日本語', 8192, 'two')
            first.settle(one, 100, 100, 0)
            second.settle(two, 100, 100, 0)
            saved = json.loads(path.read_text())['requests']
            self.assertEqual([r['id'] for r in saved], [1, 2])
            self.assertTrue(all(r['status'] == 'completed' for r in saved))

    def test_concurrent_reservations_cannot_exceed_shared_cap(self):
        from concurrent.futures import ThreadPoolExecutor
        config = json.loads(audio.PRODUCTION.read_text())
        config['gemini_budget_usd'] = .1
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'usage.json'
            def reserve(key):
                try:
                    return audio.Budget(path, config).reserve('日本語', 8192, key)['id']
                except ValueError:
                    return 'cap_rejected'
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(reserve, ['one', 'two']))
            self.assertEqual(results.count('cap_rejected'), 1)
            self.assertEqual(len(json.loads(path.read_text())['requests']), 1)

    def test_audio_garbage_rejected(self):
        with self.assertRaises(ValueError):
            audio.normalize_audio(b'broken', 'audio/wav')
        with self.assertRaises(ValueError):
            audio.normalize_audio(b'abc', 'audio/pcm;rate=24000')

    def test_sample_text_and_characters(self):
        path = audio.ROOT / 'mindmaps-podcast/ja/voice-sample.md'
        turns = audio.parse_script(path)
        self.assertEqual(len(turns), 8)
        self.assertGreater(sum(audio.text_units(t['text']) for t in turns), 500)
        self.assertNotEqual(audio.CACHE, audio.ROOT / '.work/podcast')

    def test_stale_audits_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            script = root / 'sample.md'
            script.write_text('text')
            (root / 'content.json').write_text('{"script_sha256":"stale"}')
            with self.assertRaisesRegex(ValueError, 'Stale'):
                audio.verify_audits(script, root)

    def test_full_audio_is_held_until_sample_approval(self):
        config = json.loads(audio.PRODUCTION.read_text())
        config['voice_sample_approved'] = False
        with self.assertRaisesRegex(ValueError, 'voice-sample approval'):
            audio.build(audio.ROOT / 'mindmaps-podcast/ja/voice-sample.md', config, sample=False)


if __name__ == '__main__':
    unittest.main()
