#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

def run_cmd(cmd, cwd=None, env=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True, env=env or os.environ)

def clean_build_dir(build_path):
    """build_path 내부만 삭제하되, build.rxt 마커는 보존"""
    if os.path.isdir(build_path):
        print(f"🧹 Cleaning build dir (preserve build.rxt): {build_path}")
        for name in os.listdir(build_path):
            p = os.path.join(build_path, name)
            if name.endswith(".rxt"):
                print(f"🔒 Preserving marker: {name}")
                continue
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
    else:
        os.makedirs(build_path, exist_ok=True)

def clean_install_dir(path):
    """install_path 전체를 삭제"""
    if os.path.isdir(path):
        print(f"🧹 Removing install dir: {path}")
        shutil.rmtree(path, ignore_errors=True)

def copy_package_py(source_path, install_path):
    src = os.path.join(source_path, "package.py")
    dst = os.path.join(install_path, "package.py")
    if os.path.isfile(src):
        print(f"📄 Copying package.py → {dst}")
        shutil.copy(src, dst)

def build(source_path, build_path, install_path, targets):
    # 1) 버전 결정
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", version) if (version := "2.40") else "2.40"
    src_dir = os.path.join(source_path, "source", f"binutils-{version}")
    build_dir = os.path.join(build_path, "build-binutils")
    install_dir = f"/core/Linux/APPZ/packages/binutils/{version}"

    # 2) 소스 확인
    if not os.path.isdir(src_dir):
        print(f"❌ Source not found: {src_dir}")
        sys.exit(1)
    print(f"✅ Source present: {src_dir}")

    # 3) build 디렉터리 클린업
    clean_build_dir(build_dir)

    # 4) install 타겟이면 설치 디렉터리 클린업
    if "install" in targets:
        clean_install_dir(install_dir)
        os.makedirs(install_dir, exist_ok=True)

    os.makedirs(build_dir, exist_ok=True)

    # 5) configure → make
    cfg = [
        f"{src_dir}/configure",
        f"--prefix={install_dir}",
        "--disable-multilib",
        "--enable-gold",
        "--enable-ld=default",
        "--enable-plugins",
        "--enable-shared",
        "--enable-threads",
        "--with-system-zlib",
        "--with-pic",
        "--disable-doc",
        f"--with-pkgversion='M83 Binutils {version} Toolchain'",
    ]
    run_cmd(" ".join(cfg), cwd=build_dir)
    run_cmd("make -j$(nproc)", cwd=build_dir)

    # 6) install 단계 처리
    if "install" in targets:
        run_cmd("make install", cwd=build_dir)
        copy_package_py(source_path, install_dir)
        print(f"✅ binutils-{version} installed to {install_dir}")

    # 7) 빌드 마커 남기기
    marker = os.path.join(build_dir, "build.rxt")
    open(marker, "a").close()
    print(f"📝 Touched build marker: {marker}")

if __name__ == "__main__":
    build(
        source_path  = os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path   = os.environ["REZ_BUILD_PATH"],
        install_path = os.environ["REZ_BUILD_INSTALL_PATH"],
        targets      = sys.argv[1:]
    )

