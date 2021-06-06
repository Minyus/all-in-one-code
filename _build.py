import base64
import gzip
from pathlib import Path
import subprocess


template = r"""
'''
{GIT_INFO}
'''

# base64-encoded file contents
file_data = {"file_data": ""}


import base64
import gzip
from pathlib import Path


for path, encoded in file_data.items():
    print("[Decoding] " + path)
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_bytes(gzip.decompress(base64.b64decode(encoded)))

print("*** Started to run ***")

!bash run.sh
"""


def run(*args_list):
    out_list = []
    for args in args_list:
        r = subprocess.run(
            args,
            capture_output=True,
            encoding="utf-8",
        ).stdout
        out_list.append(r)
    return out_list


def get_git_info():

    return "\n".join(
        run(
            [
                "git",
                "log",
                "--pretty=format: %h %ad %s",
                "--date=iso",
                "-1",
            ],
            [
                "git",
                "status",
                "--porcelain",
            ],
        )
    )


def encode_file(path: Path) -> str:
    compressed = gzip.compress(path.read_bytes(), compresslevel=9)
    return base64.b64encode(compressed).decode("utf-8")


def build_script():
    git_info = get_git_info()
    print(git_info)

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
        template.replace("{GIT_INFO}", git_info).replace(
            '{"file_data": ""}', str(file_data)
        ),
        encoding="utf8",
    )
    print("*** Completed to build all-in-one-code ***")


if __name__ == "__main__":
    build_script()
