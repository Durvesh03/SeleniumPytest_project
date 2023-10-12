from selenium import webdriver
import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from pathlib import Path

Base_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
UserName = "Admin"
Password = "admin123"
#driver = None


@pytest.fixture(scope='class', autouse=True)
def browser_setup(request):
    request.cls.driver = webdriver.Chrome()
    #new code =====
    global driver
    driver = request.cls.driver
    #================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" or report.when == 'setup':
        # always add url to report
        #extras.append(pytest_html.extras.url("http://www.example.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace('::', '_') + ".png"
            _capture_screenshot(file_name)
            # only add additional html on failure
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
            report.extra = extra


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    today = datetime.now()
    report_dir = Path("Reports", today.strftime("%Y%m%d"))
    # parents True means dont need to create parent folder 'Reports'
    # as it is already present. exist_ok true means today.strftime("%Y%m%d")
    # this folder is if present then use otherwise create new
    report_dir.mkdir(parents=True, exist_ok=True)
    pytest_html = report_dir / f"Report_{today.strftime('%Y%m%d%H%M')}.html"
    config.option.htmlpath = pytest_html
    config.option.self_contained_html = True


def pytest_html_report_title(report):
    report.title = "Duru Automation"


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)