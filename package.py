# -*- coding: utf-8 -*-
name        = "binutils"
version     = "2.40"
authors     = ["GNU"]
description = "GNU Binutils"

variants = []

build_requires = [
    "gcc-11.5.0",
    "python-3.13.2",    # Rez 환경의 Python 버전에 맞춤
]

# install 단계에 rezbuild.py 실행
build_command = "python {root}/rezbuild.py install"

def commands():
    # 빌드된 바이너리가 PATH에 올라가도록
    env.PATH.prepend("{root}/bin")
    # 런타임/링크 시 필요한 라이브러리 경로
    env.LD_LIBRARY_PATH.prepend("{root}/lib")

