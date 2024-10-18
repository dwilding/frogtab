# Code samples

In the examples below, replace `YOUR_ID` by the ID from your personal link.

## JavaScript SDK: Send a task

For a detailed example, see [Adding a private feedback box to Bear](https://maybecoding.bearblog.dev/adding-a-private-feedback-box-to-bear/).

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

send("Record a demo of the latest product features").then(success => {
  console.log(success);
});
```

## JavaScript SDK: Get the ID of your public key

```javascript
async function getKeyID(userID) {
  const frogtab = await import("https://frogtab.com/open/sdk.js");
  userDetails = await frogtab.getUserDetails(userID);
  return userDetails.pgpPublicKeyID;
}

getKeyID("YOUR_ID").then(keyID => {
  console.log(keyID);
});
```

## Terminal: Send a task

For a detailed explanation, see [Making a command-line tool for your Frogtab personal link](https://maybecoding.bearblog.dev/making-a-command-line-tool-for-your-frogtab-personal-link/).

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

  TASK="Record a demo of the latest product features"

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