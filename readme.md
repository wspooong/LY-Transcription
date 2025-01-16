# LY Transcription

## 簡介

LY Transcription 可以幫您下載立法院公報，並將其轉換為JSON檔案。

由於立法院提供的電子檔案為DOC，但目前python能夠處理的Word檔案格式為docx，故需要先將其轉換為docx後，才能進行轉換。

請注意：由於doc -> docx的工具由microsoft office提供，我僅在windows上使用過，故此專案僅能在windows上使用。

## 模組說明

### GazetteDownloader

用於下載立法院公報的資訊。它會從指定的 API 下載公報的 CSV 文件，並將其轉換為 JSON 格式。

範例：

```python
from src.gazette import GazetteDownloader

download_path = Path("./downloads/11")
gazette_downloader = GazetteDownloader(term="11", sessionPeriod=None, download_path=download_path)
gazette_downloader.run()
```

### TranscriptionParser

模組用於解析會議記錄文件。它會讀取 `.docx` 文件，提取文本和頁碼，並將結果保存為 JSON 格式。

```python
from src.transcript_parser import TranscriptionParser

dir_path = Path("./downloads/11")
output_path = Path("./output/11")
transcription_parser = TranscriptionParser(dir_path=dir_path, output_path=output_path)
transcription_parser.run()
```

### WordConverter

模組用於將 `.doc` 文件轉換為 `.docx`。它使用 win32com 來進行文件格式的轉換。

```python
from src.word_converter import WordConverter

dir_path = Path("./downloads/11")
word_converter = WordConverter(dir_path=dir_path)
word_converter.run()
```

## Contribution

歡迎提交PR！
