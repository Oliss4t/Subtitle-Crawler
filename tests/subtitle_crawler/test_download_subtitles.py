import unittest
import os
import json
from unittest.mock import patch
from src.openSubtitleCrawler import OpenSubtitleCrawler
from tests.subtitle_crawler.fixtures import mock_download_result, mock_download_result_wrong, mock_search_result, mock_search_result_wrong, mock_meta_subtitles, mock_success_result_save_json
from src.utils.command_response import CommandResponse
from src.errorClasses.open_subtitle_errors import OpenSubtitleSearchError
from pathlib import Path


class TestSubtitleCrawler(unittest.TestCase):

    def setUp(self):
        self.subtitle_crawler = OpenSubtitleCrawler('username', 'password', 'agent', './data/downloads/', 'eng')

    @patch('src.openSubtitleCrawler.OpenSubtitleCrawler.download_subtitle_from_proxy')
    def test_download_subtitles(self, download_proxy_mock):
        _success_result = CommandResponse(_successful=True, _message="Subtitle download successful.")
        _meta_subtitles = mock_meta_subtitles

        download_proxy_mock.return_value = mock_download_result
        self.assertEqual(self.subtitle_crawler.download_subtitles(_meta_subtitles), _success_result)
        download_proxy_mock.assert_called_once()

    @patch('src.openSubtitleCrawler.OpenSubtitleCrawler.download_subtitle_from_proxy')
    def test_download_subtitles_endpoint_error(self, download_proxy_mock):
        _meta_subtitles = mock_meta_subtitles
        _result_error = _success_result = CommandResponse(_successful=False, _message= 'The OpenSubtitleDownloadError returned a status that is: 400')

        download_proxy_mock.return_value = mock_download_result_wrong
        self.assertEqual(self.subtitle_crawler.download_subtitles(_meta_subtitles), _result_error)
        download_proxy_mock.assert_called_once()

    @patch('src.openSubtitleCrawler.OpenSubtitleCrawler.search_subtitle_from_proxy')
    def test_search_subtitles_by_id(self, search_proxy_mock):
        _mock_id = ['816692']
        _result_subtitles = mock_meta_subtitles

        search_proxy_mock.return_value = mock_search_result
        self.assertListEqual(self.subtitle_crawler.search_subtitles_by_id(_mock_id), _result_subtitles)
        search_proxy_mock.assert_called_once()

    @patch('src.openSubtitleCrawler.OpenSubtitleCrawler.search_subtitle_from_proxy')
    def test_search_subtitles_by_id_endpoint_error(self, search_proxy_mock):
        _mock_id = ['816692']
        _result_error = OpenSubtitleSearchError('400')
        try:
            search_proxy_mock.return_value = mock_search_result_wrong
            _result_method = self.subtitle_crawler.search_subtitles_by_id(_mock_id)
        except OpenSubtitleSearchError as e:
            _result_method = e
        self.assertEqual(_result_method, _result_error)
        search_proxy_mock.assert_called_once()

    def test_save_json_format_in_directory(self):
        _mock_meta_subtitle = mock_meta_subtitles[0]
        _directory_path = Path(r"data\downloads\816692\1954509006.json")
        _working_directory = Path(r"data\downloads\816692")
        _success_result = mock_success_result_save_json

        try:
            Path(_working_directory).mkdir(parents=True, exist_ok=True)
            self.subtitle_crawler.save_json_format_in_directory(_mock_meta_subtitle, _directory_path)
            contents = json.load(open(_directory_path))
        finally:
             os.remove(_directory_path)

        self.assertEqual(contents, mock_success_result_save_json)


if __name__ == '__main__':
    unittest.main()