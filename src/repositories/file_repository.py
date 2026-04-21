import pandas as pd
import starfile

from constants import DYNAMO_TABLE_COLUMN_NAMES


class FileRepository:
    def read_dynamotable(self, filename):
        particles_df = pd.read_csv(
            filename, sep="\\s+", header=None, names=DYNAMO_TABLE_COLUMN_NAMES
        )
        return particles_df

    def read_vll(self, filename):
        try:
            with open(filename, encoding="utf-8") as vll_file:
                return vll_file.read()
        except FileNotFoundError:
            return None
        except PermissionError:
            return None

    def read_starfile(self, filename):
        star_dictionary = starfile.read(filename, always_dict=True)
        return star_dictionary

    def write_starfile(self, data_dict, filename):
        starfile.write(data_dict, filename)


file_repository = FileRepository()
