#  Copyright (c) Kuba Szczodrzyński 2023-1-14.

if __name__ == "__main__":
    import re

    import PyInstaller.__main__

    with open("pyproject.toml", "r", encoding="utf-8") as f:
        text = f.read()
        version = re.search(r"version\s?=\s?\"(.+?)\"", text).group(1)
        version_raw = re.search(r"(\d+\.\d+\.\d+)", version).group(1)
        version_tuple = ", ".join(version_raw.split("."))
        description = re.search(r"description\s?=\s?\"(.+?)\"", text).group(1)

    with open(__file__, "r") as f:
        code = f.read()
        _, _, code = code.partition("exit" + "()")
        code = code.replace("0.0.0", version)
        code = code.replace("0, 0, 0", version_tuple)
        code = code.replace("--description--", description)
    with open(__file__.replace(".py", ".txt"), "w") as f:
        f.write(code.strip())

    PyInstaller.__main__.run([__file__.replace(".py", ".spec")])

    exit()

# noinspection PyUnresolvedReferences
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(0, 0, 0, 0),
        prodvers=(0, 0, 0, 0),
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        # fmt: off
        StringFileInfo([StringTable("040904B0", [
            StringStruct("CompanyName", "kuba2k2"),
            StringStruct("FileDescription", "--description--"),
            StringStruct("FileVersion", "0.0.0"),
            StringStruct("InternalName", "spicetify-beat-saber-backend"),
            StringStruct("LegalCopyright", "© 2021 Kuba Szczodrzyński."),
            StringStruct("OriginalFilename", "spicetify-beat-saber-backend.exe"),
            StringStruct("ProductName", "spicetify-beat-saber-backend"),
            StringStruct("ProductVersion", "0.0.0"),
        ])]),
        # fmt: on
        VarFileInfo([VarStruct("Translation", [1033, 1200])]),
    ],
)
