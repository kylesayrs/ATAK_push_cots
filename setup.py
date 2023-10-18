from setuptools import setup, find_packages

_deps = [
    "argparse",
    "pydantic",
    "pymap3d",
    "open3d",
]

setup(
    name="atak_cots",
    version="1.0",
    author="Kyle Sayers",
    description="",
    install_requires=_deps,
    package_dir={"": "src"},
    packages=find_packages("src", include=["atak_cots"], exclude=["*.__pycache__.*"]),
    entry_points={
        "console_scripts": [
            "atak_cots.CoTServer.serve = atak_cots.scripts.serve:main",
            "atak_cots.CoTServer.pushCot = atak_cots.scripts.push:main"
        ],
    },
)
