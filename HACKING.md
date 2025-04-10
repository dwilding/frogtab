# Hacking Frogtab

## Customizing the placeholder text of your personal link

By default, the placeholder text of your personal link is "Add a task to your inbox…". You can override the default placeholder text to help you identify the device that you're sending tasks to.

To override the default placeholder text, add `/{text}` to the end of your personal link, where `{text}` is your preferred placeholder text. Make sure that any special characters in the placeholder text are correctly [percent-encoded](https://developer.mozilla.org/en-US/docs/Glossary/Percent-encoding) in your personal link. For example, to use "Send to Linux desktop…" as the placeholder text, add `/Send%20to%20Linux%20desktop%E2%80%A6` to the end of your personal link.

To override the default placeholder text and automatically use the correct encoding, open your personal link in your browser, then run `setPlaceholder("Custom placeholder text")` in the web console.

## Using your personal link in JavaScript

```javascript
let encryptAndSend = null;

async function send(task) {
  try {
    if (!encryptAndSend) {
      const frogtab = await import("https://frogtab.com/open/sdk.js");
      encryptAndSend = await frogtab.connectToInbox("YOUR_ID");
    }
    return await encryptAndSend(task);
  }
  catch (err) {
    return false;
  }
}

send("Record a demo video").then(success => {
  console.log(success);
});
```

Replace `YOUR_ID` by the ID from your personal link.

For a detailed example, see [Adding a private feedback box to Bear](https://maybecoding.bearblog.dev/adding-a-private-feedback-box-to-bear/).

## Using your personal link in a terminal

 1. Download your public key:

    ```
    curl https://frogtab.com/key_YOUR_ID.asc > frogtab.asc
    ```

 2. Import your public key into GnuPG and change the trust level of the key:

    ```
    gpg --import frogtab.asc
    gpg --edit-key "KEY_ID"
    gpg> trust
    gpg> 5
    gpg> quit
    ```

 3. Use a shell script to send the task:

    ```sh
    #!/bin/sh

    ID="YOUR_ID"
    KEY="KEY_ID"

    TASK="Record a demo video"

    ENCRYPTED_TASK="$(echo "$TASK" | gpg --armor --encrypt --recipient "$KEY")"
    if [ $? -ne 0 ]; then
      echo "Error: gpg error" >&2
      exit 1
    fi

    POST_URL=https://frogtab.com/open/post-add-message
    POST_TYPE="Content-Type: application/json"
    POST_BODY="$(jq -n --arg p1 "$ID" --arg p2 "$ENCRYPTED_TASK" '{user_id: $p1, message: $p2}')"
    curl -s -X POST -H "$POST_TYPE" -d "$POST_BODY" "$POST_URL" | jq -e '.success == true' > /dev/null
    if [ $? -ne 0 ]; then
      echo "Error: Unable to send task" >&2
      exit 1
    fi
    ```

Replace `YOUR_ID` by the ID from your personal link.

For a detailed explanation, see [Making a command-line tool for your Frogtab personal link](https://maybecoding.bearblog.dev/making-a-command-line-tool-for-your-frogtab-personal-link/).
