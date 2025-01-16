import csv
import json
from pathlib import Path
from typing import Optional

import requests
from loguru import logger

from src.classes import GazetteInfo
from src.constants import HEADER, LY_CSV_API, SESSION_PERIOD, TERM_PERIOD
from src.utils import DownloadHelper


class GazetteDownloader:
    def __init__(self, term: str = "11", sessionPeriod: Optional[str | None] = None, download_path: Path = Path("./downloads")):
        assert term in TERM_PERIOD, f"Invalid term: {term}"

        self.term = term
        self.sessionPeriod = sessionPeriod
        self.download_path = download_path

        self.result: list[GazetteInfo] = []
        self.url_list: list[str] = []

        self.downloaded_files = [x.stem for x in Path("downloads").iterdir()]

    def _createGazetteParams(self, session):
        return {"id": "41", "type": "CSV", "fname": f"41_{self.term}{session}CSV-1.csv"}

    def getGazetteList(self):
        session_period = [self.sessionPeriod] if self.sessionPeriod else SESSION_PERIOD
        for session in session_period:
            params = self._createGazetteParams(session=session)
            try:
                response = requests.get(url=LY_CSV_API, params=params, headers=HEADER)
            except Exception:
                logger.error("Error in request")
                logger.error(f"Request detail: params={params}")
                return

            data = response.content.decode("utf-8-sig").splitlines()
            csvReader = csv.DictReader(data)
            self.result += [GazetteInfo(**{k: v for k, v in row.items() if k}) for row in csvReader]

    def run(self):
        logger.info("Downloading gazette information...")
        self.getGazetteList()
        self.url_list = set([x.docUrl for x in self.result if x.docUrl.split("/")[-1].split(".")[0] not in self.downloaded_files])
        logger.info("Done downloading gazette information.")

        logger.info(f"Downloading {len(self.url_list)} gazette documents...")
        dl_helper = DownloadHelper(path=self.download_path, url_list=self.url_list, max_concurrent_tasks=10, timeout=120, max_retries=3)
        dl_helper.run()
        logger.info("Done downloading gazette documents.")

        logger.info("Saving GazetteInfo to json...")
        with open(file=f"{self.term}_gazette_info.json", mode="w", encoding="utf-8") as f:
            data = json.dumps([x.model_dump() for x in self.result], indent=4, ensure_ascii=False)
            f.write(data)
