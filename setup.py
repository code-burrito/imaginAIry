import subprocess
import sys
from functools import lru_cache

from setuptools import find_packages, setup

is_for_windows = len(sys.argv) >= 3 and sys.argv[2].startswith("--plat-name=win")

if is_for_windows:
    scripts = None
    entry_points = {
        "console_scripts": [
            "imagine=imaginairy.cli.main:imagine_cmd",
            "aimg=imaginairy.cli.main:aimg",
        ],
    }
else:
    scripts = ["imaginairy/bin/aimg", "imaginairy/bin/imagine"]
    entry_points = None


@lru_cache()
def get_git_revision_hash() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()


revision_hash = get_git_revision_hash()

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
    readme = readme.replace(
        '<img src="',
        f'<img src="https://raw.githubusercontent.com/brycedrennan/imaginAIry/{revision_hash}/',
    )

setup(
    name="cb-imaginAIry",
    author="Code Burrito",
    version="0.1.1",
    description="AI imagined images. Pythonic generation of stable diffusion images.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(include=("imaginairy", "imaginairy.*")),
    scripts=scripts,
    entry_points=entry_points,
    package_data={
        "imaginairy": [
            "configs/*.yaml",
            "data/*.*",
            "bin/*.*",
            "enhancers/phraselists/*.txt",
            "vendored/clip/*.txt.gz",
            "vendored/clipseg/*.pth",
            "vendored/blip/configs/*.*",
            "vendored/noodle_soup_prompts/*.*",
            "vendored/noodle_soup_prompts/LICENSE",
        ]
    },
    setup_requires=[
        "setuptools"
    ],
    install_requires=[
        "click",
        "click-help-colors",
        "click-shell",
        "protobuf != 3.20.2, != 3.19.5",
        "facexlib",
        "fairscale>=0.4.4",  # for vendored blip
        "ftfy",  # for vendored clip
        "torch>=1.13.1",
        "numpy",
        "tqdm",
        "diffusers",
        "imageio>=2.9.0",
        "Pillow>=8.0.0",
        "psutil",
        "pytorch-lightning>=1.4.2",
        "omegaconf>=2.1.1",
        "open-clip-torch",
        "opencv-python",
        "requests",
        "einops>=0.3.0",
        "safetensors",
        "timm>=0.4.12",  # for vendored blip
        "torchdiffeq",
        "transformers>=4.19.2",
        "torchmetrics>=0.6.0",
        "torchvision>=0.13.1",
        "kornia>=0.6",
        "xformers>=0.0.16; sys_platform!='darwin'",
    ],
)
