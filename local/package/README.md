# Frogtab Local

Frogtab Local is a version of the [Frogtab](https://frogtab.com) task manager that runs on localhost. This package provides:

  - The Frogtab Local server
  - A class `Client` for interacting with the server over HTTP
  - A class `Controller`, which extends `Client`, for configuring and starting the server
  - A command-line tool `frogtab` for managing the server using `Controller`

For details, see the [Frogtab Local docs](https://github.com/dwilding/frogtab/blob/main/local/README.md#frogtab-local).


## License

Frogtab Local is licensed under the MIT License.

Frogtab Local uses OpenPGP.js for PGP encryption. The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs. OpenPGP.js is licensed under the GNU Lesser General Public License.