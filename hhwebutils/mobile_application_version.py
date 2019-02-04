import re


IOS_APPLICANT_USER_AGENTS = {
    'HHApplicant-Live', 'JTB-Live', 'ApplicantHH', 'ApplicantJTB', 'ApplicantJDA',
    'ApplicantHHTE', 'ApplicantJTBTE', 'ApplicantJDATE', 'HeadHunter-Live', 'JDA', 'HHTE', 'JTBTE', 'JDATE'
}
IOS_EMPLOYER_USER_AGENTS = {'JTB', 'EmployerHH', 'EmployerJTB', 'HH'}

ANDROID_APPLICANT_USER_AGENTS = {'ru.hh.android', 'by.tut.jobs.android', 'az.day.jobs.android'}
ANDROID_EMPLOYER_USER_AGENTS = {'ru.hh.employer.android', 'by.tut.jobs.employer.android'}


def regex_join(items):
    # HHApplicant-Live should match before HH
    return '|'.join(sorted(items, key=len, reverse=True))


IOS_RE = re.compile(
    '({}).*Version/([0-9.]+)'.format(regex_join(IOS_APPLICANT_USER_AGENTS.union(IOS_EMPLOYER_USER_AGENTS))), re.I
)

ANDROID_RE = re.compile(
    '({})/([0-9.]+)'.format(regex_join(ANDROID_APPLICANT_USER_AGENTS.union(ANDROID_EMPLOYER_USER_AGENTS))), re.I
)


def parse_user_agent(user_agent):
    if user_agent is None:
        return

    android_match = re.search(ANDROID_RE, user_agent)
    if android_match:
        return {
            'platform': 'android',
            'app': 'employer' if android_match.group(1) in ANDROID_EMPLOYER_USER_AGENTS else 'applicant',
            'version': android_match.group(2),
        }

    ios_match = re.search(IOS_RE, user_agent)
    if ios_match:
        return {
            'platform': 'ios',
            'app': 'employer' if ios_match.group(1) in IOS_EMPLOYER_USER_AGENTS else 'applicant',
            'version': ios_match.group(2),
        }
