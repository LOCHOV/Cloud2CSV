import Parser_Helpers.modules as modules
from colorama import init
from termcolor import colored

init()  # required for the colors to load


def cloud2csv_title():
    return colored(
        "\n//////////////////// CLOUD2CSV " + r"\\\\\\\\\\\\\\\\\\\\", "blue"
    )


def title(id, csp):
    if csp == "aws":
        for module in modules.aws:
            if id in module:
                print(cloud2csv_title())
                print(
                    colored(
                        "\n//////////////////// Module selected -> "
                        + module
                        + r" \\\\\\\\\\\\\\\\\\\\"
                        + "\n",
                        "green",
                    )
                )

    elif csp == "azure":
        for module in modules.azure:
            if id in module:
                print(cloud2csv_title())
                print(
                    colored(
                        "\n//////////////////// Module selected -> "
                        + module
                        + r" \\\\\\\\\\\\\\\\\\\\"
                        + "\n",
                        "green",
                    )
                )

    elif csp == "gcp":
        for module in modules.gcp:
            if id in module:
                print(cloud2csv_title())
                print(
                    colored(
                        "\n//////////////////// Module selected -> "
                        + module
                        + r" \\\\\\\\\\\\\\\\\\\\"
                        + "\n",
                        "green",
                    )
                )
