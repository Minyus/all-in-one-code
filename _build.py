import base64
import gzip
from pathlib import Path


template = r"""
import base64
import gzip
from pathlib import Path


# base64-encoded file contents
file_data = {"file_data": ""}


for path, encoded in file_data.items():
    print("[Decoding] " + path)
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_bytes(gzip.decompress(base64.b64decode(encoded)))

print("*** Started to run ***")

!python main.py
"""


def encode_file(path: Path) -> str:
    compressed = gzip.compress(path.read_bytes(), compresslevel=9)
    return base64.b64encode(compressed).decode("utf-8")


def build_script():
    file_data = {}
    for p in Path(".").rglob("*"):
        if (
            p.is_file()
            and not str(p).startswith(".git")
            and not str(p).startswith(".vscode")
            and not str(p).startswith(".idea")
            and ".dist-info/RECORD" not in str(p)
            and p.name not in {"_one_code.py", "_build.py", ".gitignore", ".DS_Store"}
            and p.suffix
            not in {
                ".pyc",
                ".html",
                ".js",
                ".css",
                ".svg",
                ".png",
                ".jpeg",
                ".jpg",
                ".md",
                ".rst",
                ".log",
            }
        ):
            # Skip non-ascii files
            try:
                p.read_text(encoding="ascii")
            except ValueError:
                continue

            encoded = encode_file(p)
            if p.suffix not in {".py"} and len(encoded) >= 3000:
                print(
                    "[Warning] Large File: {}, Encoded length: {}".format(
                        str(p), len(encoded)
                    )
                )
            file_data[str(p)] = encoded

    Path("_one_code.py").write_text(
        template.replace('{"file_data": ""}', str(file_data)), encoding="utf8"
    )
    print("*** Completed to build all-in-one-code ***")


if __name__ == "__main__":
    build_script()
