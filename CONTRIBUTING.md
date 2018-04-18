# How to contribute

## Pull Requests
Good pull requests - patches, improvements, new features - are a fantastic help.
They should remain focused in scope and avoid containing unrelated commits. If
your contribution involves a significant amount of work or substantial changes
to any part of the project, please open an issue to discuss it first.

Make sure to adhere to the coding conventions used throughout a project
(indentation, accurate comments, etc.). Please update any documentation that is
relevant to the change you're making.

## Pull Request Checklist
Before you submit your PR please make sure everything is in order.

- [ ] Installed `.alfredworkflow` file from repo before making changes.
- [ ] Update the version in the VERSION file
- [ ] Update README.md with new version and any pertinent info
- [ ] Export workflow to repo folder. Right-click the workflow in Alfred, click `Export...`. Don't include the `(v1.0)` in the name.

## Releasing

Once your changes have been code reviewed, and landed:

- Create a new [release](https://github.com/lucasnad27/alfred-sentry-workflow/releases)
- Attach the alfredworkflow binary file to the release
- Submit to create tag
