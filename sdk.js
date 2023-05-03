import * as openpgp from "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs";

export const publicInbox = {};
// export const inboxOwner = {};

export function setNewUser() {
  // TODO
}

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
    message == ""
    || publicInbox.userID === undefined
    || publicInbox.pgpPublicKeyObj === undefined) {
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

export function setInboxOwner(apiKey, pgpPrivateKey) {
  // TODO
}

export function fetchMessages() {
  // TODO
}