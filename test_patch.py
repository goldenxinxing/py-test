import logging
import os
from unittest.mock import patch, MagicMock

import pytest

from tasks import hi, sw


class ClassT:
    def method(self):
        f = hi("gxx")
        logging.debug(f"tttttt")
        sw("ttt")
        return f


@patch.dict(os.environ, {})
@patch("tasks.hi")
@patch("tasks.sw")
def test_patch(mock_sw: MagicMock,
               mock_hi: MagicMock):
    mock_hi.return_values = {"gxx": "66"}
    logging.debug(f"type of class:{type(mock_hi)}")


if __name__ == '__main__':
    pytest.main(['test_patch.py'])