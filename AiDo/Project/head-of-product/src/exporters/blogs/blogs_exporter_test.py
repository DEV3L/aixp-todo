from unittest.mock import Mock, mock_open, patch

import pytest
from ai_assistant_manager.env_variables import DATA_FILE_PREFIX

from src.exporters.blogs.blogs_exporter import BlogsExporter
from src.exporters.content_data import ContentData


@pytest.fixture(name="exporter")
def build_exporter():
    return BlogsExporter()


@patch("src.exporters.blogs.blogs_exporter.create_dir")
@patch("src.exporters.blogs.blogs_exporter.does_data_exist")
def test_export_data_exists(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = True

    exporter.export()

    mock_create_dir.assert_not_called()


@patch("src.exporters.blogs.blogs_exporter.create_dir")
@patch("src.exporters.blogs.blogs_exporter.does_data_exist")
def test_export_data_does_not_exist(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = False

    exporter.write_data = Mock()

    exporter.export()

    mock_create_dir.assert_called_once()
    exporter.write_data.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
@patch("json.dumps")
def test_write_data(mock_json_dumps, mock_open_file, exporter):
    exporter.load = Mock(return_value=[])
    mock_json_dumps.return_value = "{}"

    exporter.write_data()

    exporter.load.assert_called_once()
    mock_open_file.assert_called_once_with(exporter.get_file_path(), "w", encoding="utf-8")
    mock_open_file().write.assert_called_once_with(mock_json_dumps.return_value)


@patch("os.listdir")
def test_load(mock_listdir, exporter):
    exporter.file_load = Mock(return_value=ContentData(id="1", title="Test", body="Test body", date="2022-01-01"))
    mock_listdir.return_value = ["01 We Call It Saw Time.txt"]

    result = exporter.load()

    assert len(result) == 1
    assert all(isinstance(item, ContentData) for item in result)


def test_file_load(exporter):
    filename = "001 Code Smarter, Not Harder: Unleashing AI in Agile Development.txt"
    blog_data = exporter.file_load(filename)

    assert blog_data.id == "001"
    assert blog_data.title == "Code Smarter, Not Harder: Unleashing AI in Agile Development"
    assert isinstance(blog_data.body, str)
    assert blog_data.date == "2024-05-02"


def test_get_dir_path(exporter):
    result = exporter.get_dir_path()

    assert result == "bin/Blogs"


def test_get_file_path(exporter):
    result = exporter.get_file_path()

    assert result == f"bin/Blogs/{DATA_FILE_PREFIX} Blogs.json"


def test_get_data_dir_path(exporter):
    result = exporter.get_data_dir_path()

    assert result == "data/Blogs"
