import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    grid_url = os.getenv("GRID_URL")  # contoh: http://localhost:4444
    if grid_url:
        drv = webdriver.Remote(command_executor=grid_url, options=options)
    else:
        drv = webdriver.Chrome(options=options)

    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("screenshots", exist_ok=True)
            nama = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.name)
            drv.save_screenshot(f"screenshots/{nama}.png")