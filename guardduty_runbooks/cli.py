"""GuardDuty Runbook Generator
Usage:
    guardduty-runbooks [--outdir outdir] [--overwrite]

Options:
    -h --help                               Show this screen.
    --version                               Show version.
    --outdir outdir                         Directory to write runbooks [Default: ./]
    -o --overwrite                          Overwrite runbooks if found in directory

Examples:
    guardduty-runbooks
    guardduty-runbooks --outdir ./myfolder
"""

from docopt import docopt
from .guardduty import get_guardduty_html, parse_guardduty_html, GuardDutyFinding
from .utils import write_runbook


def main():
    arguments = {
        k.lstrip('-'): v for k, v in docopt(__doc__, version='AWS GuardDuty Runbook Generator v0.01').items()
    }
    run(**arguments)


def run(**arguments):
    soup = get_guardduty_html(
        link="https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html")
    findings = parse_guardduty_html(soup=soup)

    for finding in findings:
        write_runbook(content=finding.markdown, filename=finding.finding_type,
                      directory=arguments.get("outdir"), overwrite=arguments.get("overwrite"))

    # Test a single finding
    # g = GuardDutyFinding(finding_type="hello_backdoor",
    #                      finding_url="https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-ec2.html#backdoor-ec2-ccactivityb",
    #                      resource_type="resource",
    #                      data_source="the cloud",
    #                      severity="pretty high")
    # print(g.markdown)


if __name__ == '__main__':
    main()
