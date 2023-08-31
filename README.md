# GuardDuty Runbook Generator

Create a runbook for all available GuardDuty finding types found on the [GuardDuty docs website](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html) using the information documented for each finding.

This project is a kick-start to generate a base set of runbooks when GuardDuty is enabled in an organization. Runbooks will need to be customized to fit organizational incident response procedures and add contextual information.

## Generating Runbooks

This tool can be installed from [PyPI](https://pypi.org/)

```
pip install guardduty-runbooks
```

It can also be installed locally. After cloning the directory, run in the folder:

```
pip install .
```

The tool can then be run with optional flags:
```
guardduty-runbooks [--outdir outdir] [--overwrite]
```
If `outdir` is not specified, it will write all runbooks to the local directory.
```
guardduty-runbooks --outdir ./my-runbook-directory
```
This tool can be run multiple times to create runbooks for new finding types. Run the tool again over the directory where runbooks are stored and it will write new runbooks only, unless `--overwrite` is specified. Overwrite is a destructive command and will erase any customization made to the runbook.
```
guardduty-runbooks --outdir ./my-runbook-directory --overwrite
```

Runbook filenames are written using the "finding type" specified by GuardDuty. Because finding types include non alphanumeric characters like `:, /, !,` and `.`, those characters are replaced with dashes `-` and all other characters are made lowercase. This is for ease of programatically locating runbooks for tools like [Panther](https://panther.com/) and [Matano](https://www.matano.dev/).

For example:
`CryptoCurrency:EC2/BitcoinTool.B!DNS` becomes `cryptocurrency-ec2-bitcointool-b-dns`

## License
Runbook content generated from [docs.aws.amazon.com](docs.aws.amazon.com) are licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) per [AWS Site Terms](https://aws.amazon.com/terms/).

## Related projects/links
* [GuardDuty Documentation home](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
* [GuardDuty Finding Types](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html)
* [AWS Incident Response Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks)
* [Panther](https://panther.com/)
* [Matano](https://www.matano.dev/)

