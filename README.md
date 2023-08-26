# Frogtab — Private, peaceful task management

[Frogtab](https://frogtab.com) is a lightweight task manager that helps you stay focused on today's priorities.

- [Full docs](https://frogtab.com/help)
- [Dev blog](https://maybecoding.bearblog.dev/blog/)

## Data flow

Your data is stored in your browser's `localStorage`.

Frogtab can't sync data between devices. However, if you [register your main device](https://frogtab.com/help#registering-for-a-personal-link), you can send tasks to your main device from any device.
This feature uses a server to relay tasks to your main device.

More details:

 1. When you register your main device, Frogtab generates a PGP key pair in your browser.

    Frogtab then sends the public key to the server.
    The private key never leaves your main device.

    See the `register` function in [sdk.js](app/open/sdk.js).

 2. The server generates a user ID and an API key for your main device:

    - **User ID** - The public "address" of your main device
    - **API key** - A non-public "password" for your main device

    See [post-create-user.php](app/post-create-user.php).

 3. Frogtab gives you a personal link `https://frogtab.com/send#{id}`, where `{id}` is the user ID from step 2.

    You can use your personal link to send tasks to your main device.

 5. When you use your personal link to send a task, Frogtab encrypts the task using the public key from step 1.

    Frogtab then sends the encrypted task to the server.

    See the `sendMessage` function in [sdk.js](app/open/sdk.js).

 7. The server appends the encrypted task to a message queue.

    See [post-add-message.php](app/open/post-add-message.php).

  8. Frogtab on your main device periodically checks for encrypted tasks.

     The server only permits your main device to check for encrypted tasks (by requiring the API key from step 2).
     If there are encrypted tasks in the message queue, your main device downloads the encrypted tasks.

     The server clears the message queue as soon as your main device has downloaded the encrypted tasks.

     See [post-remove-messages.php](app/post-remove-messages.php).

 9. Frogtab decrypts the tasks using the private key from step 1.

    See the `fetchMessages` function in [sdk.js](app/open/sdk.js).

## JavaScript SDK

If you have [registered your main device](https://frogtab.com/help#registering-for-a-personal-link), you can use the JavaScript SDK to send messages to Frogtab on your main device.
For example:

```javascript
async function send(message) {
  const frogtab = await import("https://frogtab.com/open/sdk.js");
  await frogtab.setPublicInbox("USER ID GOES HERE");
  const success = await frogtab.sendMessage(message);
}
```

To learn more, see [this blog post](https://maybecoding.bearblog.dev/adding-a-private-feedback-box-to-bear/).