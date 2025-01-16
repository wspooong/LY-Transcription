from pathlib import Path

from src.gazette import GazetteDownloader
from src.transcript_parser import TranscriptionParser
from src.word_converter import WordConverter

if __name__ == "__main__":
    download_path = Path("./downloads/11")
    output_path = Path("./output/11")

    gazette_downloader = GazetteDownloader(term="11", sessionPeriod=None, download_path=download_path)

    gazette_downloader.run()

    word_converter = WordConverter(dir_path=download_path)
    word_converter.run()

    transcription_parser = TranscriptionParser(dir_path=download_path, output_path=output_path)
    transcription_parser.run()
