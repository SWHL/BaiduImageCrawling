# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import shlex
import shutil
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from baidu_image_crawling.main import main


@pytest.mark.parametrize(
    "command, expected_output",
    [(f"-w 美女 -tp 1 -sp  1 -pp 2 -sd {cur_dir}", 2)],
)
def test_main(capsys, command, expected_output):
    main(shlex.split(command))
    save_img_dir = cur_dir / "美女"
    assert len(list(save_img_dir.iterdir())) == expected_output

    shutil.rmtree(save_img_dir)
