from unittest import TestCase
from files_searcher import FileSearcher


class TestFileSearcher(TestCase):
    def setUp(self) -> None:
        FileSearcher.search_dir = r"C:\Users\varia\Documents\Projects\Kaspersky_intership\data_test"

    def test_search_without_filters(self):
        filters = {"text": None,
                   "file_mask": None,
                   "size": None,
                   "creation_time": None
                   }
        expected_result_len = 9
        searcher = FileSearcher(filters)
        searcher.find_paths()
        # print(result)
        self.assertEqual(expected_result_len, len(searcher.get_result()))

    def test_file_mask(self):
        filters = {"text": None,
                   "file_mask": "*_file.*",
                   "size": None,
                   "creation_time": None
                   }
        expected_result_len = 5
        searcher = FileSearcher(filters)
        searcher.find_paths()
        result = searcher.get_result()
        self.assertEqual(expected_result_len, len(result))

    def test_file_text(self):
        filters = {"text": "hello",
                   "file_mask": None,
                   "size": None,
                   "creation_time": None
                   }
        expected_result_len = 4
        searcher = FileSearcher(filters)
        searcher.find_paths()
        result = searcher.get_result()
        print(result)
        self.assertEqual(expected_result_len, len(result))

    def test_file_size(self):
        filters = {"text": None,
                   "file_mask": None,
                   "size": {"value": 102400,
                            "operator": "ge"},
                   "creation_time": None
                   }
        expected_result_len = 1
        searcher = FileSearcher(filters)
        searcher.find_paths()
        result = searcher.get_result()
        print(result)
        self.assertEqual(expected_result_len, len(result))

    def test_file_creation_time(self):
        filters = {"text": None,
                   "file_mask": None,
                   "size": None,
                   "creation_time": {"value": "2023-03-20T14:00:03Z",
                                     "operator": "le"}
                   }
        expected_result_len = 2
        searcher = FileSearcher(filters)
        searcher.find_paths()
        result = searcher.get_result()
        print(result)
        self.assertEqual(expected_result_len, len(result))

    def test_all_filters(self):
        filters = {"text": "file",
                   "file_mask": "*.txt",
                   "size": {"value": 872,
                            "operator": "eq"},
                   "creation_time": {"value": "2023-03-12T14:00:03Z",
                                     "operator": "ge"}
                   }
        expected_result_len = 1
        searcher = FileSearcher(filters)
        searcher.find_paths()
        result = searcher.get_result()
        print(result)
        self.assertEqual(expected_result_len, len(result))
