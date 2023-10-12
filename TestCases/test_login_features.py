import time
import pytest
from Pages.LoginPage import LoginPage
from conftest import Base_URL, UserName, Password


@pytest.mark.usefixtures("browser_setup")
class Test_Login:
    def setup_class(self):
        self.driver.get(Base_URL)
        self.login_page = LoginPage(self.driver)

    def test_valid_login(self):
        self.login_page.login(UserName, Password)
        time.sleep(5)

    def teardown_class(self):
        self.driver.quit()


