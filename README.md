# Frogtab — Private, peaceful task management

[Frogtab](https://frogtab.com) is a lightweight task manager that helps you stay focused on today's priorities.

<p><img alt="The Today view in Frogtab" src="app/help-today-light.png" width="480"></p>

In this README:

  - [Technical overview of Frogtab](#technical-overview-of-frogtab)
  - [How your personal link works](#how-your-personal-link-works)
  - [Using your personal link from JavaScript](#using-your-personal-link-from-javascript)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Technical overview of Frogtab

Frogtab runs in your browser and stores your data in [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
You can export your data at any time.
If your browser supports [`showSaveFilePicker()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker), you can also enable automatic backups.

Frogtab can't sync your data between devices.
However, if you [register your main device](https://frogtab.com/help#registering-for-a-personal-link),
the frogtab.com server creates a personal link that you can use to send tasks to your main device.

If you prefer to self-host Frogtab, you can use [Frogtab Local](https://github.com/dwilding/frogtab/releases).
Frogtab Local supports personal links, but your device will be registered with frogtab.com.
Frogtab Local does not include a self-hostable registration server.

## How your personal link works

 1. When you register your device, Frogtab generates a PGP key pair in your browser.
    Your device then sends the public key to the server.
    The private key never leaves your device.

    See the `register` function in [help.html](app/help.html).

 2. The server generates a user ID and an API key for your device:

      - **User ID** - The public "address" of your device
      - **API key** - A non-public "password" for your device

    See [post-create-user.php](app/open/post-create-user.php).

    Your personal link is `https://frogtab.com/send#{id}`, where `{id}` is the user ID.

 3. When you use your personal link to send a task, Frogtab first encrypts the task using the public key from step 1.
    Frogtab then sends the encrypted task to the server.

    See the `encryptAndSend` function in [send.html](app/send.html).

 4. The server queues the encrypted task.

    See [post-add-message.php](app/open/post-add-message.php).

 5. Your device periodically checks for encrypted tasks.

    The server requires the API key from step 2. This ensures that other devices cannot check for encrypted tasks.
    If there are encrypted tasks in the queue, your device downloads the encrypted tasks.

    The server clears the queue as soon as your device has downloaded the encrypted tasks.

    See [post-remove-messages.php](app/open/post-remove-messages.php).

 6. Your device decrypts the tasks using the private key from step 1.

    See the `verifyUserAndAppendMessages` function in [main.js](app/main.js).

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

Replace `USER ID GOES HERE` by the ID from the URL of your personal link.

To learn more, see [this blog post](https://maybecoding.bearblog.dev/adding-a-private-feedback-box-to-bear/).

## Acknowledgments

  - [Simple.css](https://simplecss.org)
  - [OpenPGP.js](https://openpgpjs.org)
  - [ramsey/uuid](https://uuid.ramsey.dev)
  - [iconnoir](https://iconoir.com)
  - [mackwhyte](https://www.fiverr.com/mackwhyte)

## License

Frogtab is licensed under the MIT License.
For details, see [LICENSE](LICENSE).

Frogtab uses OpenPGP.js for PGP encryption and decryption.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see [LICENSE_openpgp](LICENSE_openpgp).
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.