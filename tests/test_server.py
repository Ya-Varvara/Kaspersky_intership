from fastapi.testclient import TestClient
from unittest import TestCase, mock

from app import my_app


class TestServer(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(my_app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Message": "Hello World"})

    def test_get_searches(self):
        response = self.client.get("/searches")
        self.assertEqual(response.status_code, 200)

    def test_post_and_get_search(self):
        with mock.patch("files_searcher.FileSearcher.find_paths") as fs_mock:
            fs_mock.return_value = []
            response = self.client.post("/search", json={"text": "hello"})

            self.assertEqual(response.status_code, 202)
            self.assertEqual(fs_mock.call_count, 1)

    def test_get_search(self):
        s_id = None
        with mock.patch("files_searcher.FileSearcher.find_paths") as fs_mock:
            response = self.client.post("/search", json={"text": "hello"})
            search_id = response.json()
            s_id = search_id["search_id"]

        with mock.patch("files_searcher.FileSearcher.get_result") as fs_mock:
            fs_mock.return_value = None
            response = self.client.get(f"/searches/{s_id}")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"finished": False})

            fs_mock.return_value = ["path.txt"]

            response = self.client.get(f"/searches/{s_id}")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"finished": True, "paths": ["path.txt"]})

    def test_bad_search(self):
        response = self.client.get(f"/searches/1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": f"Incorrect id"})

        s_id = "899edf12-b30b-480c-9cdb-7fd0f38107ee"
        response = self.client.get(f"/searches/{s_id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": f"Search with id={s_id} is not found"})
