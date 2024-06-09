from unittest.mock import Mock, patch

import pytest

from src.exporters.exporter import BIN_DIR, DATA_DIR, DATA_FILE_PREFIX
from src.exporters.files.file_exporter import FileExporter

FILE_NAME = "test_file.txt"
DATA_DIRECTORY = "test_dir"


@pytest.fixture(name="exporter")
def build_exporter():
    return FileExporter(FILE_NAME, data_directory=DATA_DIRECTORY)


@patch("src.exporters.files.file_exporter.create_dir")
@patch("src.exporters.files.file_exporter.does_data_exist")
def test_export_data_exists(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = True

    exporter.export()

    mock_create_dir.assert_not_called()


@patch("src.exporters.files.file_exporter.create_dir")
@patch("src.exporters.files.file_exporter.does_data_exist")
def test_export_data_does_not_exist(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = False

    exporter.write_data = Mock()

    exporter.export()

    mock_create_dir.assert_called_once()
    exporter.write_data.assert_called_once()


@patch("src.exporters.files.file_exporter.shutil")
def test_write_data(mock_shutil, exporter):
    exporter.get_file_path = Mock(return_value="path/to/file")

    exporter.write_data()

    mock_shutil.copy.assert_called_once_with(f"{DATA_DIR}/{DATA_DIRECTORY}/{FILE_NAME}", "path/to/file")


def test_get_dir_path(exporter):
    result = exporter.get_dir_path()

    assert result == f"{BIN_DIR}/{DATA_DIRECTORY}"


def test_get_file_path(exporter):
    result = exporter.get_file_path()

    assert result == f"{BIN_DIR}/{DATA_DIRECTORY}/{DATA_FILE_PREFIX} {FILE_NAME}"
