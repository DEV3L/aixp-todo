import json
import os
from dataclasses import asdict

from ai_assistant_manager.encoding import UTF_8
from ai_assistant_manager.env_variables import BIN_DIR, DATA_DIR, DATA_FILE_PREFIX
from ai_assistant_manager.exporters.exporter import (
    create_dir,
    does_data_exist,
)
from loguru import logger

from src.exporters.content_data import ContentData


class BlogsExporter:
    def export(self):
        if does_data_exist(self.get_file_path()):
            logger.info("Blogs data exits. Skipping export.")
            return

        logger.info("Exporting Blogs data")
        create_dir(self.get_dir_path(), self.get_file_path())
        self.write_data()

    def write_data(self):
        data = self.load()

        data_as_dicts = {data.title: asdict(data) for data in data}
        json_data = json.dumps(data_as_dicts)

        with open(self.get_file_path(), "w", encoding=UTF_8) as file:
            file.write(json_data)

        logger.info(f"Blogs data written to file: {self.get_file_path()}")

    def load(self):
        files = os.listdir(self.get_data_dir_path())
        return [self.file_load(filename) for filename in files]

    def file_load(self, filename: str):
        file_id = filename[:3]
        title = filename[3:-4].strip()

        with open(
            os.path.join(self.get_data_dir_path(), filename),
            "r",
            encoding=UTF_8,
        ) as file:
            lines = file.readlines()

        body = "\n".join([line.strip() for line in lines[1:]])

        date = lines[0].strip()

        return ContentData(
            id=file_id,
            title=title,
            body=body,
            date=date,
        )

    def get_dir_path(self):
        return os.path.join(
            BIN_DIR,
            "Blogs",
        )

    def get_file_path(self):
        return os.path.join(
            self.get_dir_path(),
            f"{DATA_FILE_PREFIX} Blogs.json",
        )

    def get_data_dir_path(self):
        return os.path.join(DATA_DIR, "Blogs")
