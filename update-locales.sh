#!/bin/bash

package_directory=src/collective/plausible
locales_directory=$package_directory/locales

domain=collective.plausible
uvx i18ndude rebuild-pot --pot $locales_directory/$domain.pot --create $domain $package_directory
uvx i18ndude sync --pot $locales_directory/$domain.pot $locales_directory/*/LC_MESSAGES/$domain.po
