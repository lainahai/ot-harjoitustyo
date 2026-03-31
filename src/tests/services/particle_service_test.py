import unittest
from services.particle_service import ParticleService

class TestParticleService(unittest.TestCase):
    def setUp(self):
      self.particle_service = ParticleService()


    def test_get_tomo_names_finds_correct_names_from_vll_string(self):
      test_string = "/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_2.mrc\n/mnt/data/project/Tomograms/job006/tomograms/rec_Position_10_3.mrc"

      tomo_names = self.particle_service._get_tomo_names(test_string)

      self.assertEqual(len(tomo_names), 2)
      self.assertEqual(tomo_names[0], "Position_10_2")
      self.assertEqual(tomo_names[1], "Position_10_3")
