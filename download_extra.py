# -*- coding: utf-8 -*-
from pathlib import Path
from subprocess import run
import shutil

import requests


def stream_download(url, store_location):
    req = requests.get(url, stream=True)
    with open(store_location, "wb") as f:
        for i, block in enumerate(req.iter_content(chunk_size=1024)):
            f.write(block)
    print(store_location)


def download_from_github(repo_owner, repo, filename_end):
    url = f"https://api.github.com/repos/{repo_owner}/{repo}/releases/latest"
    data = requests.get(url).json()
    for asset in data["assets"]:
        if asset["name"].endswith(filename_end):
            stream_download(asset["browser_download_url"], Path("tools") / asset["name"])
            return


if __name__ == "__main__":
    workdir = Path("tools")
    workdir.mkdir(parents=True, exist_ok=True)
    zipper = shutil.which("7z.exe")
    if not zipper:
        raise Exception("Cannot find 7z.exe")
    download_from_github("rigaya", "NVEnc", "x64.7z")
    download_from_github("rigaya", "VCEEnc", "x64.7z")
    download_from_github("rigaya", "QSVEnc", "x64.7z")
    download_from_github("quietvoid", "hdr10plus_parser", "msvc.tar.gz")
    for archive in workdir.iterdir():
        if archive.is_file() and archive.name.endswith(".7z"):
            cmd = [zipper, "e", f"-o{archive.name.split('_')[0]}", str(archive.name)]
            extract_command = run(cmd, cwd=workdir)
            extract_command.check_returncode()
            archive.unlink()
        if archive.is_file() and "hdr10plus_parser" in archive.name:
            extract_command_1 = run([zipper, "e", str(archive.name)], cwd=workdir)
            extract_command_1.check_returncode()
            print(list(Path("tools").iterdir()))
            extract_command_2 = run([zipper, "e", f"-ohdr10plus_parser", "hdr10plus_parser.tar"], cwd=workdir)
            extract_command_2.check_returncode()
            Path("hdr10plus_parser.tar").unlink()
            archive.unlink()
