import argparse

from repositories.file_repository import FileRepository
from services.log_service import LogService
from services.particle_service import ParticleService
from ui.converter_app import ConverterApp


def main(args):
    log_service = LogService()
    repository = FileRepository(log_service)
    pservice = ParticleService(log_service, repository)

    table_file_name = args.tablefile
    vll_file_name = args.vllfile
    tomogram_star_file_name = args.tomogramfile
    output_file_name = args.outputfile

    if table_file_name and vll_file_name and tomogram_star_file_name:
        pservice.convert_dynamo_star(
            table_file_name, tomogram_star_file_name, vll_file_name, output_file_name
        )
    else:
        app = ConverterApp(pservice)
        log_service.ui = app
        app.run()


parser = argparse.ArgumentParser(
    description="Convert particle metadata from Dynamo to Relion"
)
parser.add_argument(
    "tablefile",
    help="Path to dynamo table file",
    nargs="?",
    default=None,
)
parser.add_argument(
    "vllfile",
    help="Path to VLL file",
    nargs="?",
    default=None,
)
parser.add_argument(
    "tomogramfile", help="Path to tomogram metadata starfile", nargs="?", default=None
)
parser.add_argument(
    "outputfile",
    help="Output star file name. Print to stdout if omitted.",
    nargs="?",
    default=None,
)


parsed_args = parser.parse_args()

main(parsed_args)
