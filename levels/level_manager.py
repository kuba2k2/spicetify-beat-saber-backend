import json
from hashlib import sha1
from os import makedirs, walk
from os.path import exists, expandvars, isdir, isfile, join
from shutil import rmtree
from typing import IO, List
from zipfile import ZipFile

from fastapi import HTTPException, status

from .level import Level


class LevelManager:
    INSTANCE: "LevelManager" = None
    levels: List[Level] = []

    @staticmethod
    def get_bs_dir() -> None:
        cfg_dir = expandvars(join("%APPDATA%", "spicetify-beat-saber"))
        bs_cfg = join(cfg_dir, "beatsaber.txt")
        makedirs(cfg_dir, exist_ok=True)
        if not isfile(bs_cfg):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Beat Saber directory not set",
            )
        with open(bs_cfg) as f:
            bs_dir = f.read().strip()
        if not isdir(bs_dir):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Beat Saber directory doesn't exist",
            )
        return bs_dir

    @staticmethod
    def set_bs_dir(bs_dir: str) -> None:
        if not isdir(bs_dir):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not a directory",
            )
        if not isdir(join(bs_dir, "Beat Saber_Data", "CustomLevels")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Beat Saber directory doesn't exist",
            )
        cfg_dir = expandvars(join("%APPDATA%", "spicetify-beat-saber"))
        bs_cfg = join(cfg_dir, "beatsaber.txt")
        makedirs(cfg_dir, exist_ok=True)
        with open(bs_cfg, "w") as f:
            f.write(bs_dir)
        LevelManager.INSTANCE = None

    @staticmethod
    def get_instance() -> "LevelManager":
        if LevelManager.INSTANCE:
            return LevelManager.INSTANCE
        LevelManager.INSTANCE = LevelManager(
            beatsaber_path=LevelManager.get_bs_dir(),
        )
        return LevelManager.INSTANCE

    def __init__(self, beatsaber_path: str) -> None:
        self.beatsaber_path = beatsaber_path
        self.levels_path = join(self.beatsaber_path, "Beat Saber_Data", "CustomLevels")
        self.cache_path = join(self.levels_path, "bs_map_cache.json")
        if not isdir(self.levels_path):
            makedirs(self.levels_path)
        self.read_cache()
        self.parse_levels()

    def read_cache(self) -> None:
        if isfile(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                levels: List[dict] = json.load(f)
            self.levels = [Level(**level) for level in levels]

    def write_cache(self) -> None:
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump([level.dict() for level in self.levels], f, indent=4)

    @staticmethod
    def read_dat(level_path: str, filename: str, hash) -> dict:
        file_path = join(level_path, filename)
        if not isfile(file_path):
            raise FileNotFoundError(f"{file_path} does not exist!")
        with open(file_path, "rb") as f:
            file_dat = f.read()
        hash.update(file_dat)
        return json.loads(file_dat)

    def save_level(self, level_dir: str, zip_data: IO[bytes]) -> Level:
        level_path = join(self.levels_path, level_dir)
        if exists(level_path):
            raise FileExistsError(f"Level {level_dir} is already downloaded")

        makedirs(level_path)
        with ZipFile(zip_data, "r") as zf:
            zf.extractall(level_path)

        level = self.parse_level(level_dir)
        self.levels.append(level)
        self.write_cache()
        return level

    def delete_level(self, level_dir: str) -> None:
        level_path = join(self.levels_path, level_dir)
        if not exists(level_path):
            return
        rmtree(level_path)
        self.parse_levels()

    def parse_level(self, level_dir: str) -> Level:
        print(f"Processing {level_dir}... ", end="")
        level_path = join(self.levels_path, level_dir)

        hash = sha1()
        characteristics = {}

        info = self.read_dat(level_path, filename="Info.dat", hash=hash)

        for beatmap_set in info["_difficultyBeatmapSets"]:
            characteristic = beatmap_set["_beatmapCharacteristicName"]
            diffs = []
            for beatmap in beatmap_set["_difficultyBeatmaps"]:
                diff_name = beatmap["_difficulty"]
                self.read_dat(
                    level_path, filename=beatmap["_beatmapFilename"], hash=hash
                )
                diffs.append(diff_name)
            characteristics[characteristic] = diffs

        print(hash.hexdigest())
        return Level(
            level_dir=level_dir,
            hash=hash.hexdigest(),
            name=info["_songName"],
            sub_name=info["_songSubName"],
            author_name=info["_songAuthorName"],
            mapper_name=info["_levelAuthorName"],
            characteristics=characteristics,
            song_filename=info["_songFilename"],
            cover_filename=info["_coverImageFilename"],
        )

    def parse_levels(self) -> List[Level]:
        # actually existing levels
        level_dirs = next(walk(self.levels_path), (None, [], None))[1]
        # currently cached levels
        cached_dirs = [level.level_dir for level in self.levels]

        # list uncached levels
        uncached_dirs = [
            level_dir for level_dir in level_dirs if level_dir not in cached_dirs
        ]

        for level_dir in uncached_dirs:
            try:
                level = self.parse_level(level_dir)
            except FileNotFoundError as e:
                print(e.args)
            else:
                self.levels.append(level)

        # remove non-existing levels
        len_pre = len(self.levels)
        self.levels = [level for level in self.levels if level.level_dir in level_dirs]
        len_post = len(self.levels)
        if len_post < len_pre:
            print(f"Removed {len_pre - len_post} levels from cache")

        # save cache if new levels cached or levels removed
        if uncached_dirs or len_pre != len_post:
            self.write_cache()

        return self.levels
