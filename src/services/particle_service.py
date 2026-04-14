import re

import eulerangles
import pandas as pd

from repositories.file_repository import file_repository


class ParticleService:
    def __init__(self, repository=file_repository):
        self._repository = repository

    def convert_dynamo_star(
        self,
        dynamo_table_filename,
        tomograms_star_filename,
        vll_filename,
        output_filename=None,
    ):

        particles_dynamo_df = self._read_dynamo_particles(
            dynamo_table_filename, vll_filename
        )
        particles_dynamo_df = self._filter_unaveraged_particles(particles_dynamo_df)

        tomograms_star_df = self._repository.read_starfile(tomograms_star_filename)[
            "global"
        ]

        eulers_dynamo_df = particles_dynamo_df[["tdrot", "tilt", "narot"]]
        eulers_relion_df = self._convert_eulers_dynamo_relion(eulers_dynamo_df)

        particles_dynamo_df = particles_dynamo_df.merge(
            tomograms_star_df[["rlnTomoName", "rlnTomoTomogramBinning"]],
            left_on="tomo name",
            right_on="rlnTomoName",
        )

        coordinates_dynamo_df = particles_dynamo_df[
            ["x", "dx", "y", "dy", "z", "dz", "rlnTomoTomogramBinning"]
        ]
        coordinates_relion_df = self._convert_coordinates_dynamo_relion(
            coordinates_dynamo_df
        )

        particles_relion_df = pd.DataFrame()
        particles_relion_df["dynamoTag"] = particles_dynamo_df["tag"]
        particles_relion_df["rlnTomoName"] = particles_dynamo_df["tomo name"]
        particles_relion_df = particles_relion_df.join(coordinates_relion_df)
        particles_relion_df = particles_relion_df.join(eulers_relion_df)
        particles_relion_df = particles_relion_df.merge(
            tomograms_star_df[["rlnTomoName", "rlnVoltage"]], on="rlnTomoName"
        )

        converted_particles_dict = {"particles": particles_relion_df}

        if output_filename:
            self._repository.write_starfile(converted_particles_dict, output_filename)
            return

        self._repository.print_starfile(converted_particles_dict)

    def _read_dynamo_particles(self, table_filename, vll_filename):
        particles_df = self._repository.read_dynamotable(table_filename)
        vll_contents = self._repository.read_vll(vll_filename)
        tomogram_names = self._find_tomo_names(vll_contents)

        tomo_name_column = [tomogram_names[i - 1] for i in particles_df["tomo"]]
        particles_df["tomo name"] = tomo_name_column

        return particles_df

    def _find_tomo_names(self, vll_contents):
        tomo_name_pattern = re.compile(r"rec_(\w+).mrc$", re.MULTILINE)
        return tomo_name_pattern.findall(vll_contents)

    def _filter_unaveraged_particles(self, dynamo_df):
        return dynamo_df[dynamo_df["averaged"] == 1]

    def _convert_eulers_dynamo_relion(self, eulers_dynamo_df):
        eulers_dynamo_numpy = eulers_dynamo_df.to_numpy()
        eulers_relion_numpy = eulerangles.convert_eulers(
            eulers_dynamo_numpy, source_meta="dynamo", target_meta="relion"
        )
        eulers_relion_dict = {
            "rlnAngleRot": eulers_relion_numpy[:, 0],
            "rlnAngleTilt": eulers_relion_numpy[:, 1],
            "rlnAnglePsi": eulers_relion_numpy[:, 2],
        }
        return pd.DataFrame.from_dict(eulers_relion_dict)

    def _convert_coordinates_dynamo_relion(self, coordinates_dynamo_df):
        binning_level = coordinates_dynamo_df["rlnTomoTomogramBinning"]
        coordinates_relion_dict = {
            "rlnCoordinateX": (coordinates_dynamo_df["x"] + coordinates_dynamo_df["dx"])
            * binning_level,
            "rlnCoordinateY": (coordinates_dynamo_df["y"] + coordinates_dynamo_df["dy"])
            * binning_level,
            "rlnCoordinateZ": (coordinates_dynamo_df["z"] + coordinates_dynamo_df["dz"])
            * binning_level,
        }
        return pd.DataFrame.from_dict(coordinates_relion_dict)
