import pytest

from pages.menu_page import MenuPage

# (teks menu, potongan URL tujuan yang diharapkan)
MENU_UTAMA = [
    ("Services", ["ultimateqa.com/consulting"]),
    ("Projects", ["projects.ultimateqa.com", "ultimateqaportfolio.vercel.app"]),
    ("Case Studies", ["ultimateqa.com/case-studies"]),
    ("Blog", ["ultimateqa.com/blog"]),
    ("Newsletter", ["ck.page", "kit.com"]),
]

SUBMENU_EDUCATION = [
    ("Free Courses", ["courses.ultimateqa.com/collections"]),
    ("Selenium Java", ["selenium-java-bootcamp", "academy.ultimateqa.com"]),
    ("Video courses", ["udemy.com"]),
    ("Selenium C#", ["courses.ultimateqa.com/courses/selenium-with-c"]),
    ("Selenium Resources", ["best-selenium-webdriver-resources"]),
    ("Automation Exercises", ["ultimateqa.com/automation"]),
]


def url_sesuai(url, kandidat):
    return any(k in url for k in kandidat)


@pytest.mark.parametrize("menu,harapan", MENU_UTAMA)
def test_menu_utama(driver, menu, harapan):
    page = MenuPage(driver)
    page.open()
    url = page.click_menu(menu)
    assert url_sesuai(url, harapan), f"{menu} membuka {url}"


@pytest.mark.parametrize("submenu,harapan", SUBMENU_EDUCATION)
def test_submenu_education(driver, submenu, harapan):
    page = MenuPage(driver)
    page.open()
    url = page.click_submenu("Education", submenu)
    assert url_sesuai(url, harapan), f"{submenu} membuka {url}"