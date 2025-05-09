# Frogtab — Private, peaceful task management

Frogtab is a lightweight task manager that helps you stay focused on today's priorities.

<p><img alt="The Today view in Frogtab" src="./demo.png" width="480"></p>

Frogtab runs in your browser and stores your data in [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage). You can export your data at any time. If your browser supports [`showSaveFilePicker()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker), you can also enable automatic backups.

Frogtab can't sync your data between devices. However, if you [register your main device](https://frogtab.com/help#registering-for-a-personal-link), the frogtab.com server creates a personal link that you can use to send tasks to your main device.

In this README:

  - [Using Frogtab offline](#using-frogtab-offline)
  - [How your personal link works](#how-your-personal-link-works)
  - [Self-hosting Frogtab](#self-hosting-frogtab)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Using Frogtab offline

Frogtab Local is a version of [frogtab.com](https://frogtab.com) that you can run on your computer. With Frogab Local, you can:

  - Use Frogtab offline
  - Automatically back up your data in any browser
  - Send tasks to Frogtab via a terminal

[Install the Linux snap](https://snapcraft.io/frogtab) or [install the Python package](https://github.com/dwilding/frogtab/blob/main/local/README.md#frogtab-local).

## How your personal link works

 1. When you register your device, Frogtab generates a PGP key pair in your browser. Your device then sends the public key to the server. The private key never leaves your device.

    See `register()` in [help.html](app/help.html).

 2. The server generates a user ID and an API key for your device:

      - **User ID** - The public "address" of your device
      - **API key** - A non-public "password" for your device

    See [post-create-user.php](server/public/open/post-create-user.php).

    Your personal link is `https://frogtab.com/send#{id}`, where `{id}` is the user ID.

 3. When you use your personal link to send a task, Frogtab first encrypts the task using the public key from step 1. Frogtab then sends the encrypted task to the server.

    See `encryptAndSend()` in [send.html](app/send.html).

 4. The server queues the encrypted task.

    See [post-add-message.php](server/public/open/post-add-message.php).

 5. Your device periodically checks for encrypted tasks.

    The server requires the API key from step 2. This ensures that other devices cannot check for encrypted tasks. If there are encrypted tasks in the queue, your device downloads the encrypted tasks.

    The server clears the queue as soon as your device has downloaded the encrypted tasks.

    See [post-remove-messages.php](server/public/open/post-remove-messages.php).

 6. Your device decrypts the tasks using the private key from step 1.

    See `verifyUserAndAppendMessages()` in [main.js](app/main.js).

## Self-hosting Frogtab

You'll need an Apache server with PHP and [Composer](https://getcomposer.org/). Apache must have the following modules enabled:

  - mod_mime
  - mod_rewrite
  - mod_headers

To install Frogtab on your own server:

 1. Open a shell on your server, then navigate to a directory that is accessible to PHP scripts but not accessible via the web.

 2. Download [install_frogtab.sh](extra/install_frogtab.sh) and make it executable:

    ```
    wget https://frogtab.com/install_frogtab.sh
    chmod +x install_frogtab.sh
    ```

 3. Run the following command:

    ```
    ./install_frogtab.sh /path/to/public
    ```

    Where */path/to/public* is a directory that is accessible via the web.

To use Frogtab, open your browser, then navigate to the web-accessible directory from step 3.

The first time you register a device, Frogtab creates an SQLite database called *frogtab.db* in the directory from step 1. This database stores device credentials and the queue of encrypted tasks.

Anyone who knows the URL of your installation will be able to register their device. To reject further registration attempts after you've registered your device, set `allow_registration = false` in *frogtab.toml* (in the directory from step 1).

> [!TIP]
> To update your installation, run `./install_frogtab.sh /path/to/public` again. For information about the latest changes, see [merged pull requests](https://github.com/dwilding/frogtab/pulls?q=state%3Amerged+label%3Aserver+sort%3Acreated-desc) or the [feed](https://frogtab.com/changes.xml).

## Acknowledgments

Huge thanks to:

  - Ben Ramsey for [ramsey/uuid](https://uuid.ramsey.dev)
  - [Iconnoir](https://iconoir.com)
  - Kev Quirk for [Simple.css](https://simplecss.org)
  - Lars Kiesow for [python-feedgen](https://feedgen.kiesow.be)
  - [Mackenzie W](https://www.fiverr.com/mackwhyte) for the Frogtab logo!
  - [OpenPGP.js](https://openpgpjs.org)
  - Vano Devium for [devium/toml](https://github.com/vanodevium/toml)

## License

Frogtab is licensed under the MIT License. For details, see [LICENSE](LICENSE).

Frogtab uses OpenPGP.js for PGP encryption. The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs. OpenPGP.js is licensed under the GNU Lesser General Public License. For details, see [LICENSE_openpgp](LICENSE_openpgp).
