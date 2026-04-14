import unittest
from io import StringIO

import pandas as pd

from repositories.file_repository import FileRepository
from services.particle_service import ParticleService


class MockRepository(FileRepository):
    def __init__(self):
        self.write_star_called = False
        self.print_star_called = False
        self.write_star_filename = None
        self.converted_dict = None

    def read_dynamotable(self, filename):
        f = StringIO(
            "28305 1 1 -1.1886 4.2668 7.2758 1.7338 71.75 -100.85 0.34028 0 0 1 -60 60 -60 60 0 0 1 22 0 0 627.5 467.5 175.5 0 0 0 0 0 1 0 1 0\n28300 1 1 -0.70233 -6.8471 5.0457 142.67 61.828 5.2757 0.24052 0 0 1 -60 60 -60 60 0 0 1 22 0 0 613.5 442.5 187.5 0 0 0 0 0 1 0 1 0"
        )
        read_table = super().read_dynamotable(f)
        return read_table

    def read_vll(self, filename):
        return "/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_2.mrc"

    def read_starfile(self, filename):
        mock_dict = {
            "rlnTomoName": ["Position_10_2"],
            "rlnTomoTiltSeriesStarFile": [
                "Tomograms/job006/tilt_series/Position_10_2.star"
            ],
            "rlnVoltage": [300.00000],
            "rlnSphericalAberration": [2.700000],
            "rlnAmplitudeContrast": [0.100000],
            "rlnMicrographOriginalPixelSize": [1.517000],
            "rlnTomoHand": [-1.00000],
            "rlnTomoTiltSeriesPixelSize": [1.517000],
            "rlnEtomoDirectiveFile": [
                "AlignTiltSeries/job005/external/Position_10_2/Position_10_2.edf"
            ],
            "rlnIMODResidualErrorMean": [0.835000],
            "rlnIMODResidualErrorStddev": [0.596000],
            "rlnIMODLeaveOutError": [0.000000],
            "rlnTomoTomogramBinning": [6.008299],
            "rlnTomoSizeX": [4000],
            "rlnTomoSizeY": [4000],
            "rlnTomoSizeZ": [2000],
            "rlnTomoReconstructedTomogram": [
                "Tomograms/job006/projections/rec_Position_10_2.mrc"
            ],
            "rlnTomogramProjection": [
                "Tomograms/job006/tomograms/rec_Position_10_2.mrc"
            ],
        }
        return {"global": pd.DataFrame.from_dict(mock_dict)}

    def write_starfile(self, data_dict, filename):
        self.converted_dict = data_dict
        self.write_star_called = True
        self.write_star_filename = filename

    def print_starfile(self, data_dict):
        self.converted_dict = data_dict
        self.print_star_called = True


class TestParticleService(unittest.TestCase):
    def setUp(self):
        self.particle_service = ParticleService()

    def test_find_tomo_names_finds_correct_names_from_vll_string(self):
        test_string = "/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_2.mrc\n/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_3.mrc"

        tomo_names = self.particle_service._find_tomo_names(test_string)

        self.assertEqual(len(tomo_names), 2)
        self.assertEqual(tomo_names[0], "Position_10_2")
        self.assertEqual(tomo_names[1], "Position_10_3")

    def test_find_tomo_names_ignores_folders_containing_dot_mrc(self):
        test_string = "/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_2.mrc\n/mnt/data/project/Tomograms/job006/tomograms/ignore_this.mrc/rec_Position_10_3.mrc"
        tomo_names = self.particle_service._find_tomo_names(test_string)

        self.assertEqual(len(tomo_names), 2)
        self.assertEqual(tomo_names[0], "Position_10_2")
        self.assertEqual(tomo_names[1], "Position_10_3")

    def test_convert_coordinates_calculates_new_coordinates_correctly(self):
        correct_dict = {
            "rlnCoordinateX": [0, 150],
            "rlnCoordinateY": [0, 69],
            "rlnCoordinateZ": [3, 12],
        }
        correct_df = pd.DataFrame.from_dict(correct_dict)

        test_data_dict = {
            "x": [0, 20],
            "dx": [0, 5],
            "y": [0, 10],
            "dy": [0, 1.5],
            "z": [1, 2],
            "dz": [0.5, 0],
            "rlnTomoTomogramBinning": [2, 6],
        }
        test_df = pd.DataFrame.from_dict(test_data_dict)

        converted_df = self.particle_service._convert_coordinates_dynamo_relion(test_df)

        # check_dtype=False to ignore integer and float type mistmatch.
        pd.testing.assert_frame_equal(converted_df, correct_df, check_dtype=False)

    def test_convert_prints_if_output_file_is_not_given(self):
        tablefile = "../../test_data/test_table.tbl"
        vllfile = "../../test_data/test_vll.vll"
        tomogramfile = "../../test_data/test_tomograms.star"

        test_repository = MockRepository()
        pservice = ParticleService(test_repository)
        pservice.convert_dynamo_star(tablefile, vllfile, tomogramfile)

        self.assertTrue(test_repository.print_star_called)
        self.assertFalse(test_repository.write_star_called)
