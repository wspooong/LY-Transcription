LY_CSV_API = "https://data.ly.gov.tw/odw/usageFile.action"
LY_JSON_API = "https://data.ly.gov.tw/odw/openDatasetJson.action"

TERM_MIN = 8
TERM_MAX = 11

TERM_PERIOD = [f"{x:02}" for x in range(TERM_MIN, TERM_MAX + 1)]

SESSION_PERIOD = [f"{x:02}" for x in range(1, 9)]


HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

DOWNLOAD_MAX_THREADS = 10
