import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def environ() -> dict[str, str]:
    load_dotenv(".env.tests")
    return dict(os.environ)
