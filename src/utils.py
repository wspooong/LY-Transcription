import asyncio
from pathlib import Path

import aiohttp
import backoff
from aiohttp import ClientError, ClientTimeout
from loguru import logger
from tqdm import tqdm

from src.constants import HEADER


class DownloadHelper:
    def __init__(self, path: Path, url_list: list[str], max_concurrent_tasks: int, timeout: int = 60, max_retries: int = 3):
        self.path = path
        self.url_list = url_list
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.timeout = ClientTimeout(total=timeout)
        self.max_retries = max_retries

    @backoff.on_exception(backoff.expo, (ClientError, asyncio.TimeoutError), max_tries=3, max_time=300)
    async def _download_file_with_retry(self, session: aiohttp.ClientSession, url: str, save_path: Path):
        async with session.get(url, headers=HEADER, timeout=self.timeout) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            chunk_size = 1024 * 8  # 8 KB chunks for better performance

            with tqdm(total=total_size, unit="B", unit_scale=True, desc=url.split("/")[-1], leave=False) as pbar:
                with open(save_path.absolute(), "wb") as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        pbar.update(len(chunk))

    async def _download_document(self, url: str):
        async with self.semaphore:
            save_path = self.path / url.split("/")[-1]

            try:
                timeout = ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    await self._download_file_with_retry(session, url, save_path)
                    logger.info(f"Successfully downloaded: {url}")
            except Exception as e:
                logger.error(f"Failed to download {url}: {str(e)}")
                # Remove partially downloaded file
                if save_path.exists():
                    save_path.unlink()

    async def download_all(self):
        tasks = []
        for url in self.url_list:
            task = asyncio.create_task(self._download_document(url))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        success_count = sum(1 for r in results if r is None)
        failed_count = len(results) - success_count

        logger.info(f"Download complete. Success: {success_count}, Failed: {failed_count}")

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.download_all())
        except Exception as e:
            logger.error(f"Error in download process: {str(e)}")
        finally:
            loop.close()
