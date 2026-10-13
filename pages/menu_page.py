from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class MenuPage:
    URL = "https://ultimateqa.com/automation/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _visible(self, xpath, timeout=20):
        def finder(drv):
            for el in drv.find_elements(By.XPATH, xpath):
                try:
                    if el.is_displayed():
                        return el
                except StaleElementReferenceException:
                    continue
            return False
        return WebDriverWait(self.driver, timeout).until(finder)

    def _click(self, element):
        """Klik biasa; jika terhalang elemen lain, klik lewat JavaScript."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].click();", element)

    def _follow(self, element):
        """Klik elemen, pindah ke tab baru bila ada, tahan bila link ke halaman yang sama."""
        before = set(self.driver.window_handles)
        self._click(element)
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.window_handles) > len(before)
                or d.current_url.rstrip("/") != self.URL.rstrip("/")
            )
        except TimeoutException:
            pass  # link menuju halaman yang sama (Automation Exercises)
        baru = set(self.driver.window_handles) - before
        if baru:
            self.driver.switch_to.window(baru.pop())
        self.wait.until(lambda d: d.current_url not in ("", "about:blank"))
        return self.driver.current_url

    def click_menu(self, text):
        xpath = f"//a[normalize-space(.)='{text}'][not(ancestor::footer)]"
        return self._follow(self._visible(xpath))

    def click_submenu(self, parent, child):
        parent_xpath = f"//a[normalize-space(.)='{parent}'][not(ancestor::footer)]"
        child_xpath = (
            f"{parent_xpath}/following-sibling::ul"
            f"//a[normalize-space(.)='{child}']"
        )
        # Hover diulang bila dropdown belum terbuka (menu kadang lambat siap).
        for _ in range(3):
            parent_el = self._visible(parent_xpath)
            ActionChains(self.driver).move_to_element(parent_el).perform()
            try:
                child_el = self._visible(child_xpath, timeout=5)
                return self._follow(child_el)
            except TimeoutException:
                body = self.driver.find_element(By.TAG_NAME, "body")
                ActionChains(self.driver).move_to_element(body).perform()
        # Cadangan terakhir: klik langsung elemen submenu lewat JavaScript.
        child_el = self.wait.until(
            lambda d: (d.find_elements(By.XPATH, child_xpath) or [False])[0]
        )
        return self._follow(child_el)