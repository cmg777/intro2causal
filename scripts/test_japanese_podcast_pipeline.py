import importlib.util
from pathlib import Path
import sys
import unittest
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapt_japanese_podcast import validate_translation
from transcribe_japanese_podcast import align_chunk, offset_seconds, normalized, response_words, number_flags, preserve_empty_response_for_retry
from build_japanese_reading_pages import annotated, page


class PipelineTests(unittest.TestCase):
    def test_numeric_preservation_handles_english_punctuation(self):
        validate_translation([{'id': 1, 'text': 'In2009, age26 to59, the mean was4.01.'}],
                             [{'id': 1, 'text': '2009年に26歳から59歳で、平均は4.01でした。'}])
        with self.assertRaises(ValueError):
            validate_translation([{'id': 1, 'text': 'The mean was4.01.'}], [{'id': 1, 'text': '平均は4.10でした。'}])

    def test_translation_cannot_drop_a_turn(self):
        with self.assertRaises(ValueError):
            validate_translation([{'id':1, 'text':'A'}, {'id':2, 'text':'B'}], [{'id':1,'text':'日本語です。'}])

    def test_japanese_sentence_alignment_uses_recognized_times(self):
        chunk = {'start_seconds':10, 'end_seconds':16, 'turns':[
            {'speaker':'HOST','text':'原因を考えます。','section':'問い'},
            {'speaker':'ECONOMIST','text':'保険を比べます。','section':'問い'}]}
        words = [{'word':'原因を考えます','start':0,'end':3}, {'word':'保険を比べます','start':3,'end':6}]
        segments, report = align_chunk(chunk,words)
        self.assertEqual(report['matched_characters'],1)
        self.assertEqual([(s['start'],s['end']) for s in segments],[(10,13),(13,16)])
        self.assertEqual(report['flags'],[])

    def test_unmatched_audio_does_not_get_a_fake_transcript(self):
        chunk={'start_seconds':0,'end_seconds':5,'turns':[{'speaker':'HOST','text':'保険と健康の原因を考えます。','section':'問い'}]}
        with self.assertRaises(ValueError):
            align_chunk(chunk,[{'word':'別の話題でした','start':0,'end':5}])

    def test_readings_are_selective_and_escape_html(self):
        terms=[{'term':'反実仮想','reading':'はんじつかそう'}]
        seen=set()
        result=annotated('反実仮想と反実仮想 <script>',terms,seen)
        self.assertEqual(result.count('<ruby>'),1)
        self.assertIn('&lt;script&gt;',result)
        self.assertIn('<html lang="ja">',page('題名','本文'))

    def test_time_offsets_and_normalization(self):
        self.assertEqual(offset_seconds('1.25s'),1.25)
        self.assertEqual(normalized('４．０１ 点'), '401点')
        self.assertEqual(normalized('2/3'),normalized('3分の2'))
        self.assertEqual(normalized('1万4238ドル'),normalized('14,238ドル'))
        self.assertEqual(number_flags('20,000ドルと10,000ドル','2万ドルと1万ドル'),[])
        self.assertEqual(normalized('KIPPはKnowledge Is Power Program'),normalized('切符はナレッジイズパワープログラム'))
        self.assertNotEqual(normalized('逮捕'),normalized('退学'))

    def test_isolated_bad_provider_anchor_is_documented_not_retimed(self):
        words = [{'word':'語', 'start_offset':f'{i}s', 'end_offset':f'{i+.5}s'} for i in range(101)]
        words[31]['end_offset']='4.8s'
        response={'candidates':[{'finish_reason':'STOP','content':{'parts':[{'audio_transcription':{'words':words}}]}}]}
        kept, omitted = response_words(response, 110)
        self.assertEqual(len(kept),100)
        self.assertEqual(omitted[0]['index'],31)
        self.assertEqual(omitted[0]['start'],31)
        words[31]={'word':'語','start_offset':'3.6s','end_offset':'32s'}
        kept, omitted=response_words(response,110)
        self.assertEqual(len(kept),100)
        self.assertEqual(omitted[0]['start'],3.6)
        words[32]['end_offset']='4.8s'
        with self.assertRaises(ValueError):
            response_words(response,110)

    def test_short_numeric_errors_are_flagged_even_without_long_text_mismatch(self):
        self.assertEqual(number_flags('およそ4,000人で、差は0.31点です。','およそ400人で差は0.31点です。'),['4,000'])
        self.assertEqual(number_flags('7パーセント','17パーセント'),['7'])
        self.assertEqual(number_flags('第1章では4,000人です。','第一章では4000人です。'),[])

    def test_empty_provider_retry_preserves_evidence_and_is_bounded(self):
        raw={'candidates':[{'finish_reason':'STOP','content':{'parts':[{'text':''}]}}]}
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/('a'*64+'.recognition-response.json')
            path.write_text('{}')
            self.assertFalse(preserve_empty_response_for_retry(path,raw,{}))
            self.assertTrue(preserve_empty_response_for_retry(path,raw,{'recognition_empty_retry_limit':1}))
            path.write_text('{}')
            with self.assertRaises(ValueError):
                preserve_empty_response_for_retry(path,raw,{'recognition_empty_retry_limit':1})


if __name__=='__main__':
    unittest.main()
