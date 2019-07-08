# __init__.py
# Copyright (C) 2019 Info Lab. (gnyontu39@gmail.com) and contributors
#
import inspect
import os
import sys

__version__ = '6.1905130122'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)

try:
    import convert
except ImportError as e:
    print(e," 추가할 수 없습니다.")
    exit(1)


__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]