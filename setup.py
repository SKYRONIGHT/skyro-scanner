from setuptools import setup

setup(
    name="skyro",
    version="1.0.0",
    py_modules=["skyro"],
    # Logo files still ship with the package; payloads and vuln details are
    # now embedded directly in skyro.py — no external JSON files required.
    package_data={
        "": [
            "logo_data_uri.txt",
            "logo_base64.txt",
        ]
    },
    data_files=[
        ("", [
            "logo_data_uri.txt",
            "logo_base64.txt",
        ])
    ],
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "lxml>=4.9.3",
        "urllib3>=2.0.7",
    ],
    entry_points={
        "console_scripts": [
            "skyro=skyro:main",
        ],
    },
    python_requires=">=3.8",
)