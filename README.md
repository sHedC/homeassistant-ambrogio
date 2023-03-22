# Ambrogio Robot
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Stable -
[![GitHub Release][stable-release-shield]][releases]
[![release-badge]][release-workflow]
[![codecov][codecov-shield]][codecov-link]

Latest -
[![GitHub Release][latest-release-shield]][releases]
[![validate-badge]][validate-workflow]
[![lint-badge]][lint-workflow]
[![issues][issues-shield]][issues-link]

_Integration to integrate with [Ambrogio Robot Mowers][ambrogio]._

> :warning: **In Development:** This integration is not ready yet it does nothing other than install.

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation

The preferred and easiest way to install this is from the Home Assistant Community Store (HACS).  Follow the link in the badge above for details on HACS.

Go to HACS and integraitons, then select to download Ambrogio Robot from HACS.

#### If Not Available in HACS Yet
If you do the above and Ambrogio Robot is not there it means its not yet been accepted into the default repository, hopfully this will only be a couple of weeks. In this case:

Visit the HACS _Integrations_ pane and add `https://github.com/sHedC/homeassistant-ambrogio.git` as an `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/). You'll then be able to install it through the _Integrations_ pane.

#### Manual Install
To install manually, if you really want to: I won't support this.
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `ambrogio_robot`.
1. Download _all_ the files from the `custom_components/ambrogio_robot/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Ambrogio Robot"

## Configuration is done in the UI

Go to the Home Assistant UI, go to "Configuration" -> "Integrations" click "+" and search for "Ambrogio Robot"
- Select the correct login version, if not sure try online directly to see which server you use.
- Once connected you can change the refresh time in the options


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

Or just raise a feature request, would be useful to have a use-case, what system you have and what you want to get done.

***

[ambrogio]: https://github.com/sHedC/homeassistant-ambrogio
[commits-shield]: https://img.shields.io/github/commit-activity/y/sHedC/homeassistant-ambrogio?style=for-the-badge
[commits]: https://github.com/shedc/homeassistant-ambrogio/commits/main
[license-shield]: https://img.shields.io/github/license/sHedC/homeassistant-ambrogio.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Richard%20Holmes%20%40shedc-blue.svg?style=for-the-badge

[buymecoffee_sebs]: https://www.buymeacoffee.com/sebs89
[buymecoffeebadge_sebs]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat

[buymecoffee]: https://www.buymeacoffee.com/sHedC
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/

[codecov-shield]: https://codecov.io/gh/sHedC/homeassistant-ambrogio/branch/main/graph/badge.svg?token=IANaWFnd5g
[codecov-link]: https://codecov.io/gh/sHedC/homeassistant-ambrogio

[issues-shield]: https://img.shields.io/github/issues/shedc/homeassistant-ambrogio?style=flat
[issues-link]: https://github.com/sHedC/homeassistant-ambrogio/issues

[releases]: https://github.com/shedc/homeassistant-ambrogio/releases
[stable-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-ambrogio?style=flat
[latest-release-shield]: https://img.shields.io/github/v/release/shedc/homeassistant-ambrogio?include_prereleases&style=flat

[lint-badge]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/lint.yml/badge.svg
[lint-workflow]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/lint.yml
[validate-badge]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/validate.yml/badge.svg
[validate-workflow]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/validate.yml
[release-badge]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/release.yml/badge.svg
[release-workflow]: https://github.com/sHedC/homeassistant-ambrogio/actions/workflows/release.yml
