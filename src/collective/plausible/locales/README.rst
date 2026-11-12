Adding and updating locales
---------------------------

For every language you want to translate into you need a
locales/[language]/LC_MESSAGES/collective.plausible.po
(e.g. locales/de/LC_MESSAGES/collective.plausible.po)

For German

.. code-block:: console

    $ mkdir -p de/LC_MESSAGES

To update the ``.pot`` and ``.po`` files, run from the repository root

.. code-block:: console

    $ make i18n
