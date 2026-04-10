import argparse

from services.particle_service import ParticleService


def main(args):
  pservice = ParticleService()

  table_file_name = args.tablefile
  vll_file_name = args.vllfile

  particles_df = pservice.read_dynamo_particles(table_file_name, vll_file_name)

  uniques = particles_df.groupby(["tomo", "tomo name"]).size()
  print(uniques)


parser = argparse.ArgumentParser(description="Convert metadata from Dynamo to Relion")
parser.add_argument("tablefile", help="Path to dynamo table file")
parser.add_argument("vllfile", help="Path to VLL file")

args = parser.parse_args()

main(args)
