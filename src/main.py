import argparse

from services.particle_service import ParticleService


def main(args):
    pservice = ParticleService()

    table_file_name = args.tablefile
    vll_file_name = args.vllfile
    tomogram_star_file_name = args.tomogramfile
    output_file_name = args.outputfile

    pservice.convert_dynamo_star(
        table_file_name, tomogram_star_file_name, vll_file_name, output_file_name
    )


parser = argparse.ArgumentParser(description="Convert metadata from Dynamo to Relion")
parser.add_argument("tablefile", help="Path to dynamo table file")
parser.add_argument("vllfile", help="Path to VLL file")
parser.add_argument("tomogramfile", help="Path to tomogram metadata starfile")
parser.add_argument(
    "outputfile",
    help="Output star file name. Print to stdout if omitted.",
    nargs="?",
    default=None,
)


parsed_args = parser.parse_args()

main(parsed_args)
