import * as openpgp from "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs";

export const publicInbox = {
  userID: null,
  pgpPublicKey: null,
  pgpPublicKeyObj: null
};

export async function setPublicInbox(userID) {
  let response;
  try {
    response = await fetch(`https://api.frogtab.com/open/get-user?user_id=${encodeURIComponent(userID)}`);
  }
  catch (error) {
    return false;
  }
  if (!response.ok) {
    return false;
  }
  const result = await response.json();
  if (!result.success) {
    return false;
  }
  publicInbox.userID = result.user.user_id;
  publicInbox.pgpPublicKey = result.user.pgp_public_key;
  publicInbox.pgpPublicKeyObj = await openpgp.readKey({
    armoredKey: publicInbox.pgpPublicKey
  });
  return true;
}

export async function sendMessage(message) {
  if (
    publicInbox.userID === null
    || publicInbox.pgpPublicKeyObj === null
  ) {
    return false;
  }
  const encryptedMessage = await openpgp.encrypt({
    message: await openpgp.createMessage({
      text: message
    }),
    encryptionKeys: publicInbox.pgpPublicKeyObj
  });
  let response;
  try {
    response = await fetch("https://api.frogtab.com/open/post-add-message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: publicInbox.userID,
        message: encryptedMessage
      })
    });
  }
  catch (error) {
    return false;
  }
  if (!response.ok) {
    return false;
  }
  const result = await response.json();
  return result.success;
}

export const inboxOwner = {
  apiKey: null,
  pgpPrivateKey: null,
  pgpPrivateKeyObj: null
};

export async function setInboxOwner(apiKey, pgpPrivateKey) {
  inboxOwner.apiKey = apiKey;
  inboxOwner.pgpPrivateKey = pgpPrivateKey;
  inboxOwner.pgpPrivateKeyObj = await openpgp.readKey({
    armoredKey: inboxOwner.pgpPrivateKey
  });
}

export async function fetchMessages() {
  if (
    publicInbox.userID === null
    || inboxOwner.apiKey === null
    || inboxOwner.pgpPrivateKeyObj === null
  ) {
    return null;
  }
  let response;
  try {
    response = await fetch("https://api.frogtab.com/post-remove-messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: publicInbox.userID,
        api_key: inboxOwner.apiKey
      })
    });
  }
  catch (error) {
    return null;
  }
  if (!response.ok) {
    return null;
  }
  const result = await response.json();
  if (!result.success) {
    return null;
  }
  const messages = [];
  for (const encryptedMessage of result.messages) {
    const decrypted = await openpgp.decrypt({
      message: await openpgp.readMessage({
        armoredMessage: encryptedMessage
      }),
      decryptionKeys: inboxOwner.pgpPrivateKeyObj
    });
    messages.push(decrypted.data);
  }
  return messages;
}

export async function register(comment) {
  if (comment == "") {
    return false;
  }
  const encryptedComment = await openpgp.encrypt({
    message: await openpgp.createMessage({
      text: `Registration: ${comment}`
    }),
    encryptionKeys: await openpgp.readKey({
      armoredKey: "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nxjMEZC0XTRYJKwYBBAHaRw8BAQdAQGn1uwsmrmyNDjJEpBItytslxrvK0Iym\nKrSeCQaWOv7NNzx1c2VyXzAzYWU2YjZmLTExMzQtNGU3Yi04M2VkLWRlYWFl\nNGI1M2FmN0Bmcm9ndGFiLmNvbT7CjAQQFgoAPgWCZC0XTQQLCQcICZDHWnmD\n1b6y2wMVCAoEFgACAQIZAQKbAwIeARYhBOsq7cBWQAUaO3W7VMdaeYPVvrLb\nAACwZQD+J8iHCcZwYwO3U/5dUu0fKR9iCInWlFk23UTgzUFkCS4BAILb2Xzy\nMORtPHGaBqUP0v7XbnnigyCwC2zg1JiJ5bIOzjgEZC0XTRIKKwYBBAGXVQEF\nAQEHQCbGVL7Nh+2kYvX2W6FTK7f/n7Fo7OclmEOS3xjUzEs0AwEIB8J4BBgW\nCAAqBYJkLRdNCZDHWnmD1b6y2wKbDBYhBOsq7cBWQAUaO3W7VMdaeYPVvrLb\nAABb/gEApI8wmO4HQ82pTMg2POA/AT85AseK3lv4ds1Mz6W5p48A/jbtMsAG\nn5seyoPf02oOSmPmNr7OhtP/19HeoY6Sj1IG\n=PY9A\n-----END PGP PUBLIC KEY BLOCK-----\n"
    })
  });
  const pgpKey = await openpgp.generateKey({
    userIDs: [{
      email: `key+${crypto.randomUUID()}@frogtab.com`
    }]
  });
  let response;
  try {
    response = await fetch("https://api.frogtab.com/post-create-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        pgp_public_key: pgpKey.publicKey,
        comment: encryptedComment
      })
    });
  }
  catch (error) {
    return false;
  }
  if (!response.ok) {
    return false;
  }
  const result = await response.json();
  console.log(result);
  if (!result.success) {
    return false;
  }
  publicInbox.userID = result.user.user_id;
  publicInbox.pgpPublicKey = pgpKey.publicKey;
  publicInbox.pgpPublicKeyObj = await openpgp.readKey({
    armoredKey: publicInbox.pgpPublicKey
  });
  await setInboxOwner(result.user.api_key, pgpKey.privateKey);
  return true;
}