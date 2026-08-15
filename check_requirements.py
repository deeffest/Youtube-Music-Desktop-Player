import os
import re
import sys
import json
import urllib.error
import urllib.request
from importlib import metadata

try:
    from packaging.markers import default_environment
    from packaging.requirements import InvalidRequirement, Requirement
    from packaging.version import InvalidVersion, Version
except ImportError:
    sys.exit("Missing 'packaging'. Install with: pip install packaging")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_FILE = os.path.join(SCRIPT_DIR, "requirements.txt")
PYPI_URL = "https://pypi.org/pypi/{name}/json"
TIMEOUT = 5
VCS_PREFIXES = ("git+", "hg+", "svn+", "bzr+")
USE_COLOR = sys.stdout.isatty()


def color(t, c):
    return f"\033[{c}m{t}\033[0m" if USE_COLOR else t


def green(t):
    return color(t, "32")


def yellow(t):
    return color(t, "33")


def red(t):
    return color(t, "31")


def dim(t):
    return color(t, "2")


def parse_requirements(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-"):
                items.append({"kind": "option"})
                continue
            if line.startswith(VCS_PREFIXES) or re.match(
                r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", line
            ):
                m = re.search(r"/([^/]+?)(?:\.git)?(?:@[^@/]+)?$", line)
                items.append({"kind": "vcs", "name": m.group(1) if m else line})
                continue
            try:
                req = Requirement(line)
            except InvalidRequirement as e:
                items.append({"kind": "error", "raw": line, "error": str(e)})
                continue
            items.append(
                {
                    "kind": "pkg",
                    "name": req.name,
                    "specifier": req.specifier,
                    "marker": req.marker,
                }
            )
    return items


def get_installed_version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def get_latest_pypi_version(name):
    url = PYPI_URL.format(name=name)
    req = urllib.request.Request(url, headers={"User-Agent": "check_requirements.py"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
        return data["info"]["version"], None
    except urllib.error.HTTPError as e:
        return (
            (None, "not found on PyPI") if e.code == 404 else (None, f"HTTP {e.code}")
        )
    except urllib.error.URLError as e:
        return None, f"no network ({e.reason})"
    except Exception as e:
        return None, f"error ({e})"


def safe_version(v):
    try:
        return Version(v)
    except InvalidVersion:
        return None


def fmt(s, width):
    s = str(s)
    return (s[: width - 1] + "…") if len(s) > width else s.ljust(width)


def print_row(name, required, installed, latest, status):
    print(
        fmt(name, 28)
        + fmt(required, 14)
        + fmt(installed, 14)
        + fmt(latest, 12)
        + status
    )


def process_pkg(item, env):
    name, specifier, marker = item["name"], item["specifier"], item["marker"]
    required_str = str(specifier) if str(specifier) else "any"

    if marker is not None and not marker.evaluate(env):
        print_row(
            name, required_str, "-", "-", dim("skipped (marker not met on this system)")
        )
        return

    installed = get_installed_version(name)
    latest, latest_err = get_latest_pypi_version(name)

    if installed is None:
        local_msg = red("not installed")
    else:
        inst_v = safe_version(installed)
        if specifier and str(specifier):
            satisfied = inst_v is not None and specifier.contains(
                inst_v, prereleases=True
            )
            local_msg = (
                green("OK") if satisfied else red(f"mismatch (needs {required_str})")
            )
        else:
            local_msg = green("OK")

    if latest is None:
        remote_msg = dim(f"PyPI: {latest_err}")
    else:
        latest_v = safe_version(latest)
        inst_v = safe_version(installed) if installed else None
        if inst_v is not None and latest_v is not None:
            remote_msg = (
                yellow(f"newer on PyPI: {latest}")
                if latest_v > inst_v
                else green("up to date")
            )
        else:
            remote_msg = dim(f"on PyPI: {latest}")

    print_row(
        name,
        required_str,
        installed or "-",
        latest or "-",
        f"{local_msg}; {remote_msg}",
    )


def main():
    if not os.path.isfile(REQ_FILE):
        sys.exit(f"requirements.txt not found next to script: {REQ_FILE}")

    items = parse_requirements(REQ_FILE)
    env = default_environment()

    print(f"File: {REQ_FILE}")
    print(f"Python {env['python_full_version']} | platform: {env['sys_platform']}\n")

    header = (
        fmt("Package", 28)
        + fmt("Required", 14)
        + fmt("Installed", 14)
        + fmt("PyPI", 12)
        + "Status"
    )
    print(header)
    print("-" * (len(header) + 20))

    for item in items:
        kind = item["kind"]
        if kind == "option":
            continue
        if kind == "error":
            print(f"{item['raw']!r}: {red('could not parse')} ({item['error']})")
            continue
        if kind == "vcs":
            installed = get_installed_version(item["name"])
            print_row(
                item["name"],
                "VCS/URL",
                installed or "-",
                "-",
                dim("git/URL install - version not checked"),
            )
            continue
        if kind == "pkg":
            process_pkg(item, env)


if __name__ == "__main__":
    main()
