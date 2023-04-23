import fnmatch
import os
import io
import zipfile
from datetime import datetime


def compare_values(val1, val2, operand):
    if operand == 'eq':
        return val1 == val2
    if operand[0] == 'g':
        return val1 > val2 if operand[1] == 't' else val1 >= val2
    if operand[0] == 'l':
        return val1 < val2 if operand[1] == 't' else val1 <= val2
    raise ValueError("Operator in incorrect")


def search_text(file_path, text) -> bool:
    try:
        with io.open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if text in line:
                    return True
        return False
    except UnicodeDecodeError:
        return False


class FileSearcher:
    def __init__(self, search_filters: dict):
        self.text = search_filters["text"]
        self.file_mask = search_filters["file_mask"]

        if search_filters["size"]:
            self.file_size = search_filters["size"]["value"]
            self.size_op = search_filters["size"]["operator"]
        else:
            self.file_size = None

        if search_filters["creation_time"]:
            self.creation_time = datetime.strptime(search_filters["creation_time"]["value"], '%Y-%m-%dT%H:%M:%SZ')
            self.creation_op = search_filters["creation_time"]["operator"]
        else:
            self.creation_time = None

        self.result = None

    def get_result(self):
        return self.result

    def match_filters(self, file_path) -> bool:
        """
        Функция проверяет, что данный файл соответствует всем условиям
        """
        if self.file_mask and not fnmatch.fnmatch(os.path.basename(file_path), self.file_mask):
            return False
        if self.file_size and not (
                compare_values(os.path.getsize(file_path), self.file_size, self.size_op)):
            return False
        if self.creation_time and not (
                compare_values(datetime.fromtimestamp(os.path.getctime(file_path)),
                               self.creation_time, self.creation_op)):
            return False
        if self.text and not (search_text(file_path, self.text)):
            return False
        return True

    def find_paths(self) -> None:
        result = []
        for root, dirs, files in os.walk(self.search_dir):
            for file in files:
                if zipfile.is_zipfile(os.path.join(root, file)):
                    result.extend(self.find_in_zip(os.path.join(root, file)))
                    continue
                if self.match_filters(os.path.join(root, file)):
                    result.append(os.path.join(root, file))
        self.result = result

    def find_in_zip(self, zip_file_name) -> list[str]:
        result = []
        with zipfile.ZipFile(zip_file_name, mode="r") as zip_file:
            for file in zip_file.namelist():
                # print(os.path.splitext(file)[1])
                if os.path.splitext(file)[1] == ".zip":
                    continue
                file_info = zip_file.getinfo(file)
                if self.file_mask and not fnmatch.fnmatch(file, self.file_mask):
                    continue
                if self.file_size and not (compare_values(file_info.file_size, self.file_size, self.size_op)):
                    continue
                if self.creation_time and not (
                        compare_values(datetime(*file_info.date_time), self.creation_time, self.creation_op)):
                    continue
                if self.text:
                    with zip_file.open(file) as readfile:
                        found = False
                        for line in io.TextIOWrapper(readfile, "utf-8", errors="ignore"):
                            if self.text in line:
                                found = True
                                break
                        if not found:
                            continue
                result.append(os.path.join(zip_file_name, file))
        return result
