from unittest import TestCase, mock
from unittest.mock import MagicMock, mock_open, patch

from src.assistants.assistant_service import AssistantService
from src.exporters.exporter import DATA_FILE_PREFIX


class TestAssistantService(TestCase):
    service: AssistantService
    assistant_name = "Test Assistant"

    def setUp(self):
        self.mock_client = MagicMock()

        self.service = AssistantService(self.mock_client, self.assistant_name)

    def test_get_assistant_id_exists(self):
        mock_assistant = MagicMock(id="456")
        mock_assistant.name = self.assistant_name
        self.mock_client.assistants_list = MagicMock(
            return_value=[
                mock_assistant,
            ]
        )

        result = self.service.get_assistant_id()

        assert result == "456"
        self.mock_client.assistants_list.assert_called_once()
        self.mock_client.assistants_create.assert_not_called()

    @patch("src.assistants.assistant_service.get_prompt")
    def test_get_assistant_id_create(self, mock_get_prompt):
        self.mock_client.assistants_list = MagicMock(return_value=[])
        self.mock_client.assistants_create = MagicMock(return_value=MagicMock(id="789"))
        self.mock_client.vector_stores_list = MagicMock(
            return_value=[
                MagicMock(filename=f"{DATA_FILE_PREFIX} vector store", id="654"),
            ]
        )
        result = self.service.get_assistant_id()

        assert result == "789"
        self.mock_client.assistants_list.assert_called_once()
        self.mock_client.assistants_create.assert_called_once_with(
            self.assistant_name,
            mock_get_prompt.return_value,
            ["654"],
        )

    def test_get_vector_store_ids_exists(self):
        self.mock_client.vector_stores_list = MagicMock(
            return_value=[
                MagicMock(filename=f"{DATA_FILE_PREFIX} vector store", id="654"),
            ]
        )

        result = self.service.get_vector_store_ids()

        assert result == ["654"]
        self.mock_client.vector_stores_list.assert_called_once()
        self.mock_client.create_vector_stores.assert_not_called()

    def test_create_vector_stores(self):
        expected_vector_store_id = "vector_store_id"
        expected_file_ids = ["file1_id", "file2_id"]
        self.mock_client.vector_stores_create.return_value = expected_vector_store_id
        self.mock_client.vector_stores_files.return_value = [
            MagicMock(status="completed"),
        ]

        self.service.get_retrieval_file_ids = lambda: expected_file_ids

        vector_store_ids = self.service.create_vector_stores()

        assert vector_store_ids == [expected_vector_store_id]
        self.mock_client.vector_stores_create.assert_called_with(mock.ANY, expected_file_ids)
        self.mock_client.vector_stores_files.assert_called_with(expected_vector_store_id)

    def test_create_vector_stores_with_failed_files(self):
        expected_vector_store_id = "vector_store_id"
        expected_file_ids = ["file1_id", "file2_id"]
        self.mock_client.vector_stores_create.return_value = expected_vector_store_id
        self.mock_client.vector_stores_files.side_effect = [
            [MagicMock(status="failed", id="abc")],
            [MagicMock(status="completed", id="def")],
        ]
        self.mock_client.files_get.return_value = MagicMock(filename="file_name")
        self.service.get_retrieval_file_ids = lambda: expected_file_ids

        mock_os_walk = [("root", None, ["file_name"])]

        with patch("os.walk", return_value=mock_os_walk), patch("builtins.open", mock_open(read_data="data")):
            vector_store_ids = self.service.create_vector_stores()

        assert vector_store_ids == [expected_vector_store_id]
        self.mock_client.vector_stores_file_delete.assert_called_with(expected_vector_store_id, "abc")
        self.mock_client.vector_stores_create.assert_called_with(mock.ANY, expected_file_ids)
        self.mock_client.vector_stores_files.assert_called_with(expected_vector_store_id)

    def test_validate_vector_stores(self):
        expected_vector_store_id = "vector_store_id"

        self.mock_client.vector_stores_files.return_value = [
            MagicMock(status="completed"),
        ]

        vector_store_id = self.service._validate_vector_stores(expected_vector_store_id)

        assert vector_store_id == expected_vector_store_id

    def test_get_retrieval_file_ids_exists(self):
        self.mock_client.files_list = MagicMock(
            return_value=[
                MagicMock(filename=f"{DATA_FILE_PREFIX} blogs.json", id="456"),
            ]
        )

        result = self.service.get_retrieval_file_ids()

        assert result == ["456"]
        self.mock_client.files_list.assert_called_once()
        self.mock_client.files_create.assert_not_called()

    def test_create_retrieval_files(self):
        self.mock_client.files_create.return_value.id = "file_id"

        mock_os_walk = [("root", None, ["file1", "file2"])]
        expected_file_ids = ["file_id", "file_id"]

        with patch("os.walk", return_value=mock_os_walk), patch("builtins.open", mock_open(read_data="data")):
            actual_file_ids = self.service.create_retrieval_files()

        assert actual_file_ids == expected_file_ids
        self.mock_client.files_create.assert_called_with(mock.ANY, "assistants")

    # pylint: disable=protected-access
    def test_delete_assistant_with_existing_assistant_and_files(self):
        self.service._find_existing_assistant = MagicMock(return_value="assistant_id")
        self.service._find_existing_vector_stores = MagicMock(return_value=["vs1_id", "vs2_id"])
        self.service._find_existing_retrieval_files = MagicMock(return_value=["file1_id", "file2_id"])

        self.service.delete_assistant()

        self.service._find_existing_assistant.assert_called_once()
        self.service._find_existing_vector_stores.assert_called_once()
        self.service._find_existing_retrieval_files.assert_called_once()
        self.mock_client.assistants_delete.assert_called_once_with("assistant_id")
        self.mock_client.vector_stores_delete.assert_any_call("vs1_id")
        self.mock_client.vector_stores_delete.assert_any_call("vs2_id")
        self.mock_client.files_delete.assert_any_call("file1_id")
        self.mock_client.files_delete.assert_any_call("file2_id")

    def test_delete_assistant_with_no_existing_assistant_and_files(self):
        self.service._find_existing_assistant = MagicMock(return_value=None)
        self.service._find_existing_retrieval_files = MagicMock(return_value=None)

        self.service.delete_assistant()

        self.service._find_existing_assistant.assert_called_once()
        self.service._find_existing_retrieval_files.assert_called_once()
        self.mock_client.assistants_delete.assert_not_called()
        self.mock_client.files_delete.assert_not_called()

    # pylint: enable=protected-access
