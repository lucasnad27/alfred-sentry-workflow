import argparse
import sys

from workflow import (
    Workflow,
    ICON_WEB,
    ICON_WARNING,
    web,
    PasswordNotFound)

BASE_URL = "https://sentry.io/"

log = None


def get_projects(api_key):
    """
    API reference
    https://docs.sentry.io/api/projects/get-project-index/
    """
    url = BASE_URL + 'api/0/projects/'
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    r = web.get(url, headers=headers)
    projects = []

    r.raise_for_status()
    projects.extend(r.json())

    while True:
        # this is terrible, please forgive me for my sins
        next_link = [x for x in r.headers['Link'].split(',') if 'next' in x][0]
        next_info = {
            k.strip(' '): v.strip(' "') for (k, v) in
            [x.split('=') for x in
             [x for x in next_link.split(';') if 'http' not in x]]}
        if next_info['results'] == 'false':
            break
        url = '{}/api/0/projects/?&cursor={}'.format(BASE_URL, next_info['cursor'])
        r = web.get(url, headers=headers)
        projects.extend(r.json())

    return projects


def search_key_for_project(project):
    elements = [
        project['name'],
        project['slug']
    ]
    return u' '.join(elements)


def main(wf):

    parser = argparse.ArgumentParser()
    parser.add_argument('--setkey', dest='apikey', nargs='?', default=None)
    parser.add_argument('--get_issues', dest='get_issues')
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    if args.apikey:
        wf.save_password('sentry_api_key', args.apikey)
        return 0

    try:
        api_key = wf.get_password('sentry_api_key')
    except PasswordNotFound:
        wf.add_item(
            'No API key set.',
            'Please use sentrysetkey to set your sentry API key',
            valid=False,
            icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    query = args.query
    get_issues = args.get_issues

    if get_issues:
        # https://docs.sentry.io/api/events/get-project-group-index/
        org_slug, project_slug, issues_url = get_issues.split(' ')
        headers = {'Authorization': 'Bearer {}'.format(api_key)}
        r = web.get(issues_url, headers=headers)

        r.raise_for_status()

        issues = r.json()
        for issue in issues:
            url = BASE_URL + '{}/{}/issues/{}'.format(
                org_slug, project_slug, issue['id'])
            wf.add_item(
                title=issue['title'],
                subtitle='last seen: {}; {} occurences'.format(issue['lastSeen'], issue['count']),
                arg=url,
                valid=True,
                icon=ICON_WEB)
        wf.send_feedback()

    def wrapper():
        return get_projects(api_key)

    projects = wf.cached_data('posts', wrapper, max_age=600)

    if query:
        projects = wf.filter(
            query,
            projects,
            key=search_key_for_project,
            min_score=20)

    if not projects:
        wf.add_item('No projects found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    for project in projects:
        org_slug = project['organization']['slug']
        project_slug = project['slug']
        url = BASE_URL + 'api/0/projects/{}/{}/issues/'.format(
            org_slug, project_slug)
        args = ' '.join([org_slug, project_slug, url])
        wf.add_item(
            title=project['name'],
            subtitle='hello',
            arg=args,
            valid=True,
            icon=ICON_WEB)

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
