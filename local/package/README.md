# Frogtab Local

Frogtab Local is a version of the [Frogtab](https://frogtab.com) task manager that runs on localhost. This package provides:

  - The Frogtab Local server
  - A Python interface for configuring, starting, and interacting with the server
  - A command `frogtab`, which wraps the Python interface, for managing the server and sending tasks to Frogtab

For details, see the [Frogtab Local docs](https://github.com/dwilding/frogtab/blob/main/local/README.md#frogtab-local).

This package also provides a command `serve-frogtab /path/to/config.json`, which enables other service managers to run the server as a daemon. 

## License

Frogtab Local is licensed under the MIT License.

Frogtab Local uses OpenPGP.js for PGP encryption. The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs. OpenPGP.js is licensed under the GNU Lesser General Public License.
