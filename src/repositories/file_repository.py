import pandas as pd
import starfile

from constants import DYNAMO_TABLE_COLUMN_NAMES


class FileRepository:
    """Class responsible for reading and writing files."""

    def __init__(self, log_service):
        """Constructor for the class.

        Args:
            log_service: LogService object responsible for logging output.
        """
        self._log_service = log_service

    def read_dynamotable(self, filename):
        """Reads a Dynamo table from file.

        Args:
            filename: path to the file as a string or PathLike object.

        Returns:
            Table contents in a DataFrame object.
            None if the file couldn't be read.
        """
        try:
            particles_df = pd.read_csv(
                filename, sep="\\s+", header=None, names=DYNAMO_TABLE_COLUMN_NAMES
            )
            return particles_df
        except ValueError as err:
            self._log_service.log(f"Error parsing file {filename}: {str(err)}")
            return None
        except PermissionError:
            self._log_service.log(
                f"Couldn't read file {str(filename)}: Permission denied."
            )
            return None

    def read_vll(self, filename):
        """Reads a .vll file.

        Args:
            filename: path to the file as a string or PathLike object.

        Returns:
            File contents as a single string.
            None if the file couldn't be read.
        """
        try:
            with open(filename, encoding="utf-8") as vll_file:
                return vll_file.read()
        except ValueError as err:
            self._log_service.log(f"Error parsing file {filename}: {str(err)}")
            return None
        except PermissionError:
            self._log_service.log(
                f"Couldn't read file {str(filename)}: Permission denied."
            )
            return None

    def read_starfile(self, filename):
        """Reads a starfile.

        Args:
            filename: path to the file as a string or PathLike object.

        Returns:
            Starfile contents in a dictionary with table names as keys and DataFrames as values.
            None if the file couldn't be read.
        """
        try:
            star_dictionary = starfile.read(filename, always_dict=True)
            if len(star_dictionary) == 0:
                self._log_service.log(f"No data blocks found in starfile {filename}")
            return star_dictionary
        except ValueError as err:
            self._log_service.log(f"Error parsing file {filename}: {str(err)}")
            return None
        except PermissionError:
            self._log_service.log(
                f"Couldn't read file {str(filename)}: Permission denied."
            )
            return None

    def write_starfile(self, data_dict, filename):
        """Write a starfile.

        Args:
            data_dict:
                Dictionary tables to be written with table names as keys and DataFrames as values.
            filename:
                Path to the file to be written as a string or PathLike object.
        """
        try:
            starfile.write(data_dict, filename)
        except PermissionError:
            self._log_service.log(
                f"Couldn't write file {str(filename)}: Permission denied."
            )
