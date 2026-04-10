import re

import pandas as pd
import starfile

TABLE_COLUMN_NAMES = [
  "tag",
  "aligned",
  "averaged",
  "dx",
  "dy",
  "dz",
  "tdrot",
  "tilt",
  "narot",
  "cc",
  "cc2",
  "cpu",
  "ftype",
  "ymintilt",
  "ymaxtilt",
  "xmintilt",
  "xmaxtilt",
  "fs1",
  "fs2",
  "tomo",
  "reg",
  "class",
  "annotation",
  "x",
  "y",
  "z",
  "dshift",
  "daxis",
  "dnarot",
  "dcc",
  "otag",
  "npar",
  "ref",
  "sref",
  "apix",
  "def",
  "eig1",
  "eig2",
]


class ParticleService:
  def read_dynamo_particles(self, table_filename, vll_filename):
    particles_df = self._read_dynamotable(table_filename)
    vll_contents = self._read_vll(vll_filename)
    tomogram_names = self._get_tomo_names(vll_contents)

    tomo_name_column = [tomogram_names[i - 1] for i in particles_df["tomo"]]
    particles_df["tomo name"] = tomo_name_column

    return particles_df

  def _read_dynamotable(self, filename):
    particles_df = pd.read_csv(
      filename, sep="\\s+", header=None, names=TABLE_COLUMN_NAMES
    )
    return particles_df

  def _read_vll(self, filename):
    try:
      with open(filename) as vll_file:
        return vll_file.read()
    except FileNotFoundError:
      return None
    except PermissionError:
      return None

  def _read_starfile(self, filename):
    star_dictionary = starfile.read(filename, always_dict=True)
    return star_dictionary

  def _get_tomo_names(self, vll_contents):
    tomo_name_pattern = re.compile(r"rec_(\w+).mrc")
    return tomo_name_pattern.findall(vll_contents)
