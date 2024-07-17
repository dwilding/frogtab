# Frogtab — Private, peaceful task management

[Frogtab](https://frogtab.com) is a lightweight task manager that helps you stay focused on today's priorities.

<p><img alt="The Today view in Frogtab" src="app/help-today-light.png" width="480"></p>

In this README:

  - [Technical overview of Frogtab](#technical-overview-of-frogtab)
  - [How your personal link works](#how-your-personal-link-works)
  - [Customizing the placeholder text of your personal link](#customizing-the-placeholder-text-of-your-personal-link)
  - [Using your personal link from JavaScript](#using-your-personal-link-from-javascript)
  - [Self-hosting Frogtab](#self-hosting-frogtab)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Technical overview of Frogtab

Frogtab runs in your browser and stores your data in [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
You can export your data at any time.
If your browser supports [`showSaveFilePicker()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker), you can also enable automatic backups.

You can use Frogtab offline by running Frogtab Local on your computer.
Frogtab Local also enables automatic backups in any browser.
If you use Linux, you can [install Frogtab Local from the Snap Store](https://snapcraft.io/frogtab).
Otherwise, you can [download and run the latest release](https://github.com/dwilding/frogtab/releases).

Frogtab can't sync your data between devices.
However, if you [register your main device](https://frogtab.com/help#registering-for-a-personal-link),
the frogtab.com server creates a personal link that you can use to send tasks to your main device.

## How your personal link works

 1. When you register your device, Frogtab generates a PGP key pair in your browser.
    Your device then sends the public key to the server.
    The private key never leaves your device.

    See `register()` in [help.html](app/help.html).

 2. The server generates a user ID and an API key for your device:

      - **User ID** - The public "address" of your device
      - **API key** - A non-public "password" for your device

    See [post-create-user.php](server/public/open/post-create-user.php).

    Your personal link is `https://frogtab.com/send#{id}`, where `{id}` is the user ID.

 3. When you use your personal link to send a task, Frogtab first encrypts the task using the public key from step 1.
    Frogtab then sends the encrypted task to the server.

    See `encryptAndSend()` in [send.html](app/send.html).

 4. The server queues the encrypted task.

    See [post-add-message.php](server/public/open/post-add-message.php).

 5. Your device periodically checks for encrypted tasks.

    The server requires the API key from step 2. This ensures that other devices cannot check for encrypted tasks.
    If there are encrypted tasks in the queue, your device downloads the encrypted tasks.

    The server clears the queue as soon as your device has downloaded the encrypted tasks.

    See [post-remove-messages.php](server/public/open/post-remove-messages.php).

 6. Your device decrypts the tasks using the private key from step 1.

    See `verifyUserAndAppendMessages()` in [main.js](app/main.js).

## Customizing the placeholder text of your personal link

By default, the placeholder text of your personal link is "Send to your inbox…".
You can override the default placeholder text to help you identify the device that you're sending tasks to.

To override the default placeholder text, add `/{text}` to the end of your personal link, where `{text}` is your preferred placeholder text.
Make sure that any special characters in the placeholder text are correctly [percent-encoded](https://developer.mozilla.org/en-US/docs/Glossary/Percent-encoding) in your personal link.
For example, to use "Send to Linux desktop…" as the placeholder text, add `/Send%20to%20Linux%20desktop%E2%80%A6` to the end of your personal link.

To override the default placeholder text and automatically use the correct encoding, open your personal link in your browser, then enter `setPlaceholder("Custom placeholder text")` in the web console.

## Using your personal link from JavaScript

After registering your device, you can use the JavaScript SDK to send messages to your device:

```javascript
let encryptAndSend = null;

async function send(message) {
  try {
    if (!encryptAndSend) {
      const frogtab = await import("https://frogtab.com/open/sdk.js");
      encryptAndSend = await frogtab.connectToInbox("USER ID GOES HERE");
    }
    return await encryptAndSend(message);
  }
  catch (err) {
    return false;
  }
}

send("Hello Frogtab!").then(success => {
  console.log(success);
});
```

Replace `USER ID GOES HERE` by the ID from your personal link.

To learn more, see [this blog post](https://maybecoding.bearblog.dev/adding-a-private-feedback-box-to-bear/).

## Self-hosting Frogtab

You'll need an Apache server that has PHP and [Composer](https://getcomposer.org/) installed.

To install Frogtab on your own server:

 1. Open a shell on your server, then navigate to a directory that is accessible to PHP scripts but not accessible via the web.

 2. Enter the following commands:

    ```sh
    git clone "https://github.com/dwilding/frogtab.git"
    cd frogtab
    ./dev_build_server.sh
    ```

 3. Copy the contents of *frogtab/server/public* to a directory that is accessible via the web.
    Make sure that the *.htaccess* files in *frogtab/server/public* and *frogtab/server/public/open* are copied.

Frogtab is ready!

To use Frogtab, open your browser, then navigate to the web-accessible directory from step 3.

The first time you register a device, Frogtab creates a SQLite database called *frogtab.db* in the directory from step 1.
This database stores device credentials and the queue of encrypted tasks.

## Acknowledgments

  - [Simple.css](https://simplecss.org)
  - [OpenPGP.js](https://openpgpjs.org)
  - [ramsey/uuid](https://uuid.ramsey.dev)
  - [iconnoir](https://iconoir.com)
  - [mackwhyte](https://www.fiverr.com/mackwhyte)

## License

Frogtab is licensed under the MIT License.
For details, see [LICENSE](LICENSE).

Frogtab uses OpenPGP.js for PGP encryption.
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see [LICENSE_openpgp](LICENSE_openpgp).