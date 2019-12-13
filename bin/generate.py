import argparse
import datetime
import logging
import sys

from mefipy.parse import run_activity_summary

DEFAULT_TAGS = ["uspolitics", "potus45", "GOP", "plannedparenthood", "capitalism", "socialism", "whitesupremacy", "organizedlabor", "SCOTUS", "firstamendment", "usa", "americanaffairs"]

def setup_args():
    parser = argparse.ArgumentParser(description="Make an activity report for the given tags.")

    parser.add_argument("startdate",
        help="Start time YYYY-MM-DD HH:SS",
        type=datetime.datetime.fromisoformat)
    parser.add_argument("enddate",
        help="End time YYYY-MM-DD HH:SS",
        type=datetime.datetime.fromisoformat)
    parser.add_argument("report",
        nargs="?",
        help="Write report to file; default output to stdout",
        type=argparse.FileType("w"),
        default=sys.stdout)
    parser.add_argument("-t", "--tag",
        nargs="*",
        help="Use a different set of tags than the default",
        default=DEFAULT_TAGS)

    return parser.parse_args()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    args = setup_args()
    run_activity_summary(args.tag, args.startdate, args.enddate, report=args.report)
