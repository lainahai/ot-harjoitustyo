import re
from pathlib import Path

import eulerangles
import pandas as pd
import starfile


class ParticleService:
    """Class responsible for converting particle metadata from Dynamo to Relion."""

    def __init__(self, log_service, repository):
        """Constructor for the class.

        Args:
            log_service: LogService object responsible for logging output.
            repository: Repository object responsible for handling file operations.
        """
        self._log_service = log_service
        self._repository = repository

    def convert_dynamo_star(
        self,
        dynamo_table_filename,
        tomograms_star_filename,
        vll_filename,
        output_filename=None,
    ):
        """Converts particle metadata between Dynamo and Relion formats.

        Dynamo data should come in two files: a table file containing the particle metadata
        and a vll-file with paths to the tomogram files.
        A .star-file containing metadata for the tomograms is also required
        Output data in is written to a file if an output file is given, otherwise printed to stdout.

        Args:
            dynamo_table_filename: path to the Dynamo table file. String or PathLike object.
            tomograms_star_filename: path to the tomogram metadata file. String or PathLike object.
            vll_filename: path to the vll-file. String or PathLike object.
            output_filename:
                Optional. Path to the output file. String or PathLike object.
                If omitted, starfile-formatted data is redirected to the LogService object.
        """
        try:
            if self._validate_input_paths(
                dynamo_table_filename, tomograms_star_filename, vll_filename
            ):
                return

            particles_dynamo_df = self._read_dynamo_particles(
                dynamo_table_filename, vll_filename
            )

            tomograms_star_dict = self._repository.read_starfile(
                tomograms_star_filename
            )

            if particles_dynamo_df is None or "global" not in tomograms_star_dict:
                return
            tomograms_star_df = tomograms_star_dict["global"]

            particles_dynamo_df = self._filter_unaveraged_particles(particles_dynamo_df)

            if not self._check_no_missing_tomogram_data(
                particles_dynamo_df["tomo name"], tomograms_star_df["rlnTomoName"]
            ):
                return

            particles_dynamo_df = particles_dynamo_df.merge(
                tomograms_star_df[["rlnTomoName", "rlnTomoTomogramBinning"]],
                left_on="tomo name",
                right_on="rlnTomoName",
            )

            eulers_dynamo_df = particles_dynamo_df[["tdrot", "tilt", "narot"]]
            eulers_relion_df = self._convert_eulers_dynamo_relion(eulers_dynamo_df)

            coordinates_dynamo_df = particles_dynamo_df[
                ["x", "dx", "y", "dy", "z", "dz", "rlnTomoTomogramBinning"]
            ]
            coordinates_relion_df = self._convert_coordinates_dynamo_relion(
                coordinates_dynamo_df
            )

            particles_relion_df = self._compile_particle_data_for_relion(
                particles_dynamo_df,
                coordinates_relion_df,
                eulers_relion_df,
                tomograms_star_df,
            )

            converted_particles_dict = {"particles": particles_relion_df}

            if output_filename:
                self._repository.write_starfile(
                    converted_particles_dict, output_filename
                )
                self._log_service.log(f"Wrote {output_filename}", ui_only=True)
                return
            self._log_service.log(starfile.to_string(converted_particles_dict))
        except KeyError as err:
            self._log_service.log(f"Missing required field: {str(err)}")
        except Exception as err:
            self._log_service.log(f"An unexpected error occurred: {str(err)}")

    def _read_dynamo_particles(self, table_filename, vll_filename):
        dynamo_particles_df = self._repository.read_dynamotable(table_filename)
        vll_contents = self._repository.read_vll(vll_filename)

        if dynamo_particles_df is None or vll_contents is None:
            return None
        tomogram_names = self._find_tomo_names(vll_contents)

        if not self._validate_dynamo_table_and_vll_tomograms(
            dynamo_particles_df, tomogram_names
        ):
            return None

        tomo_name_column = [tomogram_names[i - 1] for i in dynamo_particles_df["tomo"]]
        dynamo_particles_df["tomo name"] = tomo_name_column

        return dynamo_particles_df

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

    def _compile_particle_data_for_relion(
        self,
        particles_dynamo_df,
        coordinates_relion_df,
        eulers_relion_df,
        tomograms_star_df,
    ):
        particles_relion_df = pd.DataFrame()
        particles_relion_df["dynamoTag"] = particles_dynamo_df["tag"]
        particles_relion_df["rlnTomoName"] = particles_dynamo_df["tomo name"]
        particles_relion_df = particles_relion_df.join(coordinates_relion_df)
        particles_relion_df = particles_relion_df.join(eulers_relion_df)
        particles_relion_df = particles_relion_df.merge(
            tomograms_star_df[["rlnTomoName", "rlnVoltage"]], on="rlnTomoName"
        )
        return particles_relion_df

    def _validate_file_path(self, filename_or_path):
        try:
            path_to_file = Path(filename_or_path)
            if not path_to_file.exists():
                return f"File {str(path_to_file)} does not exist."
            if path_to_file.is_dir():
                return f"File {str(path_to_file)} is a directory."
            if not path_to_file.is_file():
                return f"File {str(path_to_file)} is not a normal file."
            return None
        except TypeError:
            return f"Invalid file path {str(filename_or_path)}"

    def _validate_input_paths(self, *paths):
        errors = map(self._validate_file_path, paths)
        errors = [error for error in errors if error]
        if len(errors) > 0:
            self._log_service.log("\n".join(errors))
            return errors
        return None

    def _validate_dynamo_table_and_vll_tomograms(self, dynamo_particles_df, tomo_names):
        min_tomo_index = min(dynamo_particles_df["tomo"])
        max_tomo_index = max(dynamo_particles_df["tomo"])
        if len(tomo_names) == 0:
            self._log_service.log("No tomograms found in VLL file.")
            return False
        if len(tomo_names) < max_tomo_index:
            self._log_service.log(
                f"Dynamo table tomogram index out of bounds: found index {max_tomo_index}, "
                + f"but VLL file only contains {len(tomo_names)} tomograms."
            )
            return False
        if min_tomo_index < 1:
            self._log_service.log(
                f"Dynamo table tomogram index out of bounds: {min_tomo_index}"
            )
            return False
        return True

    def _check_no_missing_tomogram_data(self, dynamo_tomo_series, star_tomo_series):
        missing_tomos = [
            tomo for tomo in dynamo_tomo_series if tomo not in star_tomo_series.values
        ]
        if len(missing_tomos) > 0:
            self._log_service.log("Tomograms missing from tomogram data:")
            for tomo in missing_tomos:
                self._log_service.log(tomo)
            return False
        return True
