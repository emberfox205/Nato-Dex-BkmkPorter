#!usr/bin/env python3
from argparse import ArgumentParser
from os import path
from sys import exit
import json
from webdriver_process import scrape, upload, web_setup, init_web, quit_web

parser = ArgumentParser(
    description="This script migrates bookmarked titles from manganato and its sister sites to mangadex."
)
subparsers = parser.add_subparsers(dest="mode", metavar="[run|set]")

parser_run = subparsers.add_parser(
    "run", help="Execute the script with specific browser configurations."
)
parser_run.add_argument(
    "-br",
    "--browser",
    metavar="browser",
    choices=["chrome", "edge", "firefox"],
    help="Specify the browser to run the script with (chrome|edge|firefox)",
    default=None,
)
parser_run.add_argument(
    "-dir",
    "--directory",
    type=str,
    help="Specify the user's directory for the chosen browser.",
    default=None,
)
parser_run.add_argument(
    "-p",
    "--profile",
    type=str,
    help="Specify the user's profile that has both websites logged into desired accounts.",
    default=None,
)

parser_set = subparsers.add_parser(
    "set", help="Assign default values for the browser configurations."
)
parser_set.add_argument(
    "-br",
    "--browser",
    metavar="browser",
    choices=["chrome", "edge", "firefox"],
    help="Set the default browser (chrome|edge|firefox)",
    default=None,
)
parser_set.add_argument(
    "-dir",
    "--directory",
    type=str,
    help="Set the default directory for the chosen browser.",
    default=None,
)
parser_set.add_argument(
    "-p",
    "--profile",
    type=str,
    help="Set the default profile for the chosen browser.",
    default=None,
)

args = parser.parse_args()


def format_path(directory, profile) -> str:
    full_path = "\\\\".join([directory, str(profile)]).replace("\\\\", "\\")
    return full_path


def validate_config(full_path):
    if path.exists(full_path) == False:
        print("Error: profile not found")
        return False
    elif path.exists(args.directory) == False:
        print("Error: directory not found")
        return False
    else:
        print("Path to profile exists")
        return True

def mod_config(config: dict, *browser_configs):
    for br_cfg in browser_configs:
        for key in ["browser", "directory", "profile"]:
            config[br_cfg][key] = str(getattr(args, key))
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def executor(config):
    full_path = format_path(args.directory, args.profile)
    if validate_config(full_path):
        # Set initial default values
        if all(
            config["default"][key] == "" for key in ["browser", "directory", "profile"]
        ):
            mod_config(config, "default")
        else:
            mod_config(config, "default", f"{args.browser}_df")
        driver = init_web(args.browser, web_setup(args.browser, full_path, args.profile))
        #scrape(driver)
        upload(driver)
        quit_web(driver)


def main():
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    if args.mode == "set" and all(
        getattr(args, key) == None for key in ("browser", "directory", "profile")
    ):
        print("No arguments provided, run program with '-h' for help")
        exit()
    # Run with only browser specified option
    if args.browser != None and all(
        getattr(args, key) == None for key in ("directory", "profile")
    ):
        for key in ["directory", "profile"]:
            setattr(args, key, str(config[f"{args.browser}_df"][key]))
    # Fill Nonetype arguments with default values
    else:
        for key in ["browser", "directory", "profile"]:
            if getattr(args, key) == None:
                setattr(args, key, str(config["default"][key]))
    if args.mode == "run":
        executor(config)
    elif args.mode == "set":
        mod_config(config, "default")


if __name__ == "__main__":
    main()
