import re

CYR_SYM = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANS_L = ("a","b","v","g","d","e","e","j","z","i","j","k","l","m","n","o","p","r","s","t","u","f","h","ts","ch","sh",
    "sch","","y","","e","yu","u","ja","je","ji","g",)

TRANS = {}
for c, l in zip(CYR_SYM, TRANS_L):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'(?![.])\W', "_", t_name)
    return t_name

import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP4_VIDEO = []
AVI_VIDEO = []
MKV_VIDEO = []
DOC_DOCS = []
DOCX_DOCS = []
PDF_DOCS = []
MP3_AUDIO = []
OGG_AUDIO = []
MY_OTHERS = []
ARCHIVES = []


REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "JPG": JPG_IMAGES,
    "PNG": PNG_IMAGES,
    "SVG": SVG_IMAGES,
    "MP4": MP4_VIDEO,
    "AVI": AVI_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCS,
    "DOCX": DOCX_DOCS,
    "PDF": PDF_DOCS,
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "ZIP": ARCHIVES
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHERS'):
                FOLDERS.append(item)
                scan(item)

            continue

        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            MY_OTHERS.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHERS.append(fullname)


# if __name__ == "__main__":
#     folder_to_scan = sys.argv[1]
#     print(f"Start in folder {folder_to_scan}")
#     scan(Path(folder_to_scan)) 

from pathlib import Path
import shutil
import sys
# import parser_2 as parser_2
# from normalize import normalize

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name)) 

# def handle_archive(filename: Path, target_folder: Path) -> None:
#     target_folder.mkdir(exist_ok=True, parents=True)
#     filename.replace(target_folder / normalize(filename.name))
#     folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
#     folder_for_file.mkdir(exist_ok=True, parents=True)
#     try:
#         shutil.unpack_archive(filename, folder_for_file)
#     except shutil.ReadError:
#         print("It is not archive")
#         folder_for_file.rmdir()
#     filename.unlink()

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename = filename.replace(target_folder / normalize(filename.name))
    folder_for_file = target_folder / filename.stem
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
        filename.unlink()
    except shutil.ReadError:
        print("It is not archive")
        folder_for_file.rmdir()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main_2(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in DOC_DOCS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in PDF_DOCS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in MY_OTHERS:
        handle_media(file, folder)
    for file in ARCHIVES:
        handle_archive(file, folder / 'archives')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

def main():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main_2(folder_for_scan.resolve())   