from re import sub
from typing import Dict, List

from pydantic import BaseModel


def camel_case(s):
    s = sub(r"([_\-])+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


class Level(BaseModel):
    level_dir: str
    hash: str

    name: str
    sub_name: str
    author_name: str
    mapper_name: str

    characteristics: Dict[str, List[str]]

    song_filename: str
    cover_filename: str

    class Config:
        alias_generator = camel_case
        allow_population_by_field_name = True
