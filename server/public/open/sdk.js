import * as openpgp from "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs";


// v2 interface

const apiBase = import.meta.url.replace(/sdk\.js.*$/, "");

export async function connectToInbox(userID) {
  const userDetails = await getUserDetails(userID);
  return userDetails.encryptAndSend;
}

export async function getUserDetails(userID) {
  let responseGetUser;
  try {
    responseGetUser = await fetch(`${apiBase}get-user?user_id=${encodeURIComponent(userID)}`);
  }
  catch (err) {
    throw new Error("Unable to get user details");
  }
  if (!responseGetUser.ok) {
    throw new Error("Unable to get user details");
  }
  const resultGetUser = await responseGetUser.json();
  if (!resultGetUser.success) {
    throw new Error("Unable to get user details");
  }
  const pgpPublicKeyObj = await openpgp.readKey({
    armoredKey: resultGetUser.user.pgp_public_key
  });
  return {
    pgpPublicKeyID: pgpPublicKeyObj.getUserIDs()[0],
    encryptAndSend: async plainMessage => {
      const encryptedMessage = await openpgp.encrypt({
        message: await openpgp.createMessage({
          text: plainMessage
        }),
        encryptionKeys: pgpPublicKeyObj
      });
      let responseAddMessage;
      try {
        responseAddMessage = await fetch(`${apiBase}post-add-message`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            user_id: userID,
            message: encryptedMessage
          })
        });
      }
      catch (err) {
        return false;
      }
      if (!responseAddMessage.ok) {
        return false;
      }
      const resultAddMessage = await responseAddMessage.json();
      return resultAddMessage.success;
    }
  };
}


// v1 interface

let encryptAndSend = null;

export async function setPublicInbox(userID) {
  try {
    encryptAndSend = await connectToInbox(userID);
    return true;
  }
  catch (err) {
    return false;
  }
}

export async function sendMessage(plainMessage) {
  if (encryptAndSend === null) {
    return false;
  }
  try {
    return await encryptAndSend(plainMessage);
  }
  catch (err) {
    return false;
  }
}