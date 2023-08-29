from .utils import chomp_keep_single_spaces
from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup

BASE_GUARDDUTY_URL = "https://docs.aws.amazon.com/guardduty/latest/ug"


def get_guardduty_html(link):
    """
    Scrapes a webpage and returns it parsed by BeautifulSoup
    """

    response = requests.get(link, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def parse_guardduty_html(soup):
    """Parses the GuardDuty findings table on the main page

    Args:
        soup (list): Array of GuardDutyFinding types
    """
    table = soup.find_all('table')[0]
    rows = [row.findAll('td')
            for row in table.findAll('tr') if row.findAll('td')]
    findings = [GuardDutyFinding(finding_type=row[0].p.text,
                                 finding_url=f"{BASE_GUARDDUTY_URL}{row[0].a['href'][1:]}",
                                 resource_type=row[1].p.text,
                                 data_source=row[2].p.text,
                                 severity=row[3].p.text
                                 ) for row in rows]
    return findings


class GuardDutyFinding:
    """_summary_
    """
    def __init__(self, finding_type, finding_url, resource_type, data_source, severity):
        # removes non alphanumeric characters from finding_type
        self.finding_type = ''.join(c if c.isalnum() else '-' for c in finding_type.lower())
        self.finding_url = finding_url
        self.resource_type = resource_type
        self.data_source = data_source
        self.severity = severity

        self.finding_heading = self.finding_url.split("#")[-1]
        self.get_finding_html()
        self.make_html_string()


    def get_finding_html(self):
        """Gets the html for a finding between headings
        """
        soup = get_guardduty_html(link=self.finding_url)
        self.finding_info = []

        # Find the finding heading 
        s = soup.find('h2', {"id": self.finding_heading})
        self.finding_info.append(s)

        # Start looking down the tree until we get to another h2 heading and add everything in between
        for sibling in s.find_next_siblings():
            if sibling.name == 'h2':
                break
            self.finding_info.append(sibling)

        # add to url because they all start with ./
        for element in self.finding_info:
            if element.a and element.a['href'][0] == ".":
                element.a['href'] = f"{BASE_GUARDDUTY_URL}{element.a['href'][1:]}"


    def make_html_string(self):
        """
        Cleans the lines into strings and
        attempts to format them
        """
        combined = [ chomp_keep_single_spaces(str(line)) for line in self.finding_info]

        self.strings = '\n '.join(combined)


    @property
    def markdown(self):
        """Converts to markdown

        Returns:
            str : markdown in string format
        """
        return md(self.strings)