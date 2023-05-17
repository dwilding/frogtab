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
  const messages = [];
  const encryptedMessages = await response.json();
  for (const encryptedMessage of encryptedMessages) {
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

export async function generateLocalCredentials() {
  const userID = crypto.randomUUID();
  const apiKey = crypto.randomUUID();
  const pgpKey = await openpgp.generateKey({
    userIDs: [{
      email: `user_${userID}@frogtab.com`
    }]
  });
  return {
    userID: userID,
    apiKey: apiKey,
    pgpPublicKey: pgpKey.publicKey,
    pgpPrivateKey: pgpKey.privateKey
  };
}