from pathlib import Path

import win32com.client
from loguru import logger
from tqdm import tqdm

OUTPUT_FORMAT_DICT = {"docx": 16, "pdf": 17}


class WordConverter:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
        self.word = win32com.client.gencache.EnsureDispatch("Word.Application")
        # AttributeError: module 'win32com.gen_py.00020905-0000-0000-C000-000000000046x0x8x7' has no attribute 'CLSIDToClassMap'
        # python -c "import win32com; print(win32com.__gen_path__)"
        self.word.Visible = False
        self.dir_path = dir_path

    def file_convert(self, input_file: Path, output_format: str):
        assert output_format in OUTPUT_FORMAT_DICT, f"Invalid output format, must be one of {OUTPUT_FORMAT_DICT.keys()}."

        output_file = input_file.with_suffix(f".{output_format}")
        if output_file.exists():
            return

        document = self.word.Documents.Open(str(input_file.absolute()))
        document.SaveAs(str(output_file.absolute()), OUTPUT_FORMAT_DICT[output_format])
        document.Close()

    def run(self):
        logger.info("Converting .doc files...")
        doc_files = list(self.dir_path.glob("*.doc"))
        total_files = len(doc_files)

        pbar = tqdm(doc_files, total=total_files, desc="Converting")
        # for file in tqdm(doc_files, total=total_files, desc="Converting"):
        for file in doc_files:
            pbar.set_description(f"Converting {file.name}")
            self.file_convert(file, "docx")
            self.file_convert(file, "pdf")
            pbar.update(1)

        self.word.Quit()
        logger.info("Conversion complete.")
