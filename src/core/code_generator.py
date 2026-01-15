
from jinja2 import Template
from typing import Dict, Any
from loguru import logger
import black 

class SeleniumGenerator:
    TEST_TEMPLATE = """
import pytest
from selenium import webdriver

class GeneratedPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "{{ url }}"
    def load(self):
        self.driver.get(self.url)

    {% for action in actions %}
    def {{ action.func_name }}(self):
        # {{ action.description }}
        pass 
    {% endfor %}

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_scenario(driver):
    page = GeneratedPage(driver)
    page.load()
    {% if steps %}
    # Manual Steps from AI:
    {% for step in steps %}
    # - {{ step }}
    {% endfor %}
    {% endif %}
    assert "Title" in driver.title
"""

    def generate_test_script(self, test_plan: Dict[str, Any]) -> str:
        try:
            template = Template(self.TEST_TEMPLATE)
            raw_code = template.render(
                url=test_plan.get("url", "https://example.com"),
                actions=test_plan.get("actions", []),
                steps=test_plan.get("steps", [])
            )
            try:
                return black.format_str(raw_code, mode=black.Mode())
            except Exception:
                return raw_code
        except Exception as e:
            logger.error(f"Gen Error: {e}")
            return f"# Error generating code: {e}"
