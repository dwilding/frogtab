async function storeIcons() {
  const fetched = await Promise.all([
    fetch("favicons/icon-16.png"),
    fetch("favicons/icon-32.png"),
    fetch("favicons/icon-16-notify.png"),
    fetch("favicons/icon-32-notify.png")
  ]);
  const getObjectURL = async i => {
    const blob = await fetched[i].blob();
    return URL.createObjectURL(blob);
  };
  storedIcons.icon16 = await getObjectURL(0);
  storedIcons.icon32 = await getObjectURL(1);
  storedIcons.icon16Notify = await getObjectURL(2);
  storedIcons.icon32Notify = await getObjectURL(3);
}
function switchToTab(tab) {
  if (tab != selectedTab) {
    dom[tab].classList.add("selected");
    dom[tab].tabIndex = -1;
    dom[tab].blur();
    dom[selectedTab].classList.remove("selected");
    dom[selectedTab].tabIndex = 0;
    dom.editor[tab].classList.add("display");
    dom.editor[selectedTab].classList.remove("display");
    selectedTab = tab;
  }
  refreshView();
}
function checkValue(value) {
  return value.match(/^\s*[^\s#]/m) !== null;
}
function setNotifyStatus() {
  const storedInboxValue = localStorage.getItem("value.inbox");
  if (checkValue(storedInboxValue) && !notifyInbox) {
    notifyInbox = true;
    dom.inbox.classList.add("notify");
    if (requestedIcon === null) {
      dom.icon16.href = storedIcons.icon16Notify;
      dom.icon32.href = storedIcons.icon32Notify;
    }
  }
  else if (!checkValue(storedInboxValue) && notifyInbox) {
    notifyInbox = false;
    dom.inbox.classList.remove("notify");
    if (requestedIcon === null) {
      dom.icon16.href = storedIcons.icon16;
      dom.icon32.href = storedIcons.icon32;
    }
  }
}
function refreshView() {
  if (dom.editor[selectedTab].value != localStorage.getItem(`value.${selectedTab}`)) {
    dom.editor[selectedTab].value = localStorage.getItem(`value.${selectedTab}`);
    dom.editor[selectedTab].setSelectionRange(0, 0);
    dom.editor[selectedTab].scrollTop = 0;
    refreshInfo();
  }
}
function refreshInfo() {
  dom.info.classList.remove("display");
  window.clearTimeout(timeoutShowInfo);
  if (selectedTab == "inbox" && !notifyInbox) {
    timeoutShowInfo = window.setTimeout(() => {
      dom.info.classList.add("display");
    }, 30000);
  }
}
function addSpaceForCompletionOffset(editor) {
  const cursorPos = editor.selectionEnd;
  const lineStart = editor.value.lastIndexOf("\n", editor.selectionEnd - 1) + 1;
  const textToCursor = editor.value.substring(lineStart, cursorPos);
  if (!/^\s*x\s+$/i.test(textToCursor)) {
    return;
  }
  const nextChar = editor.value.substring(cursorPos, cursorPos + 1);
  if (nextChar == "" || /\s/.test(nextChar)) {
    return;
  }
  const beforeLine = editor.value.substring(0, lineStart);
  const afterCursor = editor.value.substring(cursorPos);
  editor.value = `${beforeLine}${textToCursor.toLowerCase()} ${afterCursor}`;
  editor.setSelectionRange(cursorPos, cursorPos);
}
function extractCompletionOffset(editor) {
  if (editor.selectionStart != editor.selectionEnd) {
    return null;
  }
  const cursorPos = editor.selectionEnd;
  const lineStart = editor.value.lastIndexOf("\n", editor.selectionEnd - 1) + 1;
  let lineEnd = editor.value.indexOf("\n", cursorPos);
  if (lineEnd == -1) {
    lineEnd = editor.value.length;
  }
  const lineText = editor.value.substring(lineStart, lineEnd);
  const match = lineText.match(/^(\s*x\s+((-\d+|sun|mon|tue|wed|thu|fri|sat)\s+)?)[^\s]/i);
  if (match === null) {
    return null;
  }
  if (cursorPos > lineStart + match[1].length) {
    return null;
  }
  const beforeLine = editor.value.substring(0, lineStart);
  const afterOffset = editor.value.substring(lineStart + match[1].length);
  editor.value = `${beforeLine}${afterOffset}`;
  editor.setSelectionRange(lineStart, lineStart);
  if (match[3] === undefined) {
    return "";
  }
  return match[3];
}
function completeSelected(editor, storageKey, offset) {
  const selectionStart = editor.selectionStart;
  const selectionEnd = editor.selectionEnd;
  let newSelectionPos;
  const lines = editor.value.split("\n");
  const linesUpdated = [];
  const linesCaptured = [];
  let capturing = false;
  let lineStart = 0;
  let lineEnd;
  for (const line of lines) {
    lineEnd = lineStart + line.length;
    const trimmedLine = line.trimStart();
    if (lineEnd < selectionStart) {
      linesUpdated.push(line);
    }
    else if (lineStart > selectionEnd) {
      if (!capturing) {
        linesUpdated.push(line);
      }
      else if (trimmedLine != "") {
        linesUpdated.push(line);
        capturing = false;
      }
    }
    else {
      if (capturing) {
        if (trimmedLine != "") {
          linesCaptured.push(trimmedLine.replace(/^( *#)+ */, ""));
        }
      }
      else if (trimmedLine != "") {
        linesCaptured.push(trimmedLine.replace(/^( *#)+ */, ""));
        newSelectionPos = lineStart;
        capturing = true;
      }
      else {
        linesUpdated.push(line);
      }
    }
    lineStart = lineEnd + 1;
  }
  if (linesCaptured.length > 0) {
    editor.value = linesUpdated.join("\n");
    if (capturing) {
      editor.value = editor.value.trimEnd();
    }
    storeThenSave(storageKey, editor.value);
    editor.setSelectionRange(newSelectionPos, newSelectionPos);
    updateCompleted(linesCaptured, offset);
  }
}
function inboxMoveSelected() {
  const selectionStart = dom.editor.inbox.selectionStart;
  const selectionEnd = dom.editor.inbox.selectionEnd;
  let newSelectionPos;
  const lines = dom.editor.inbox.value.split("\n");
  const linesUpdated = [];
  const linesCaptured = [];
  let capturing = false;
  let lineStart = 0;
  let lineEnd;
  for (const line of lines) {
    lineEnd = lineStart + line.length;
    const trimmedLine = line.trimStart();
    if (lineEnd < selectionStart) {
      linesUpdated.push(line);
    }
    else if (lineStart > selectionEnd) {
      if (!capturing) {
        linesUpdated.push(line);
      }
      else if (trimmedLine != "") {
        linesUpdated.push(line);
        capturing = false;
      }
    }
    else {
      if (capturing) {
        if (!trimmedLine.startsWith("#")) {
          linesCaptured.push(line);
        }
        else {
          linesCaptured.push(trimmedLine.replace(/^( *#)+ */, ""));
        }
      }
      else if (trimmedLine != "") {
        if (!trimmedLine.startsWith("#")) {
          linesCaptured.push(line);
        }
        else {
          linesCaptured.push(trimmedLine.replace(/^( *#)+ */, ""));
        }
        newSelectionPos = lineStart;
        capturing = true;
      }
      else {
        linesUpdated.push(line);
      }
    }
    lineStart = lineEnd + 1;
  }
  if (linesCaptured.length > 0) {
    dom.editor.inbox.value = linesUpdated.join("\n");
    if (capturing) {
      dom.editor.inbox.value = dom.editor.inbox.value.trimEnd();
    }
    storeThenSave("value.inbox", dom.editor.inbox.value);
    dom.editor.inbox.setSelectionRange(newSelectionPos, newSelectionPos);
    let storedTodayValue = localStorage.getItem("value.today");
    storedTodayValue = appendToBottom(storedTodayValue, linesCaptured.join("\n"));
    storeThenSave("value.today", storedTodayValue);
  }
}
function todaySnoozeSelected() {
  const selectionStart = dom.editor.today.selectionStart;
  const selectionEnd = dom.editor.today.selectionEnd;
  let newSelectionPos;
  const lines = dom.editor.today.value.split("\n");
  const linesUpdated = [];
  const linesCaptured = [];
  let capturing = false;
  let lineStart = 0;
  let lineEnd;
  for (const line of lines) {
    lineEnd = lineStart + line.length;
    const trimmedLine = line.trimStart();
    if (lineEnd < selectionStart) {
      linesUpdated.push(line);
    }
    else if (lineStart > selectionEnd) {
      if (!capturing) {
        linesUpdated.push(line);
      }
      else if (trimmedLine != "") {
        linesUpdated.push(line);
        capturing = false;
      }
    }
    else {
      if (capturing) {
        if (trimmedLine == "" || trimmedLine.startsWith("#")) {
          linesCaptured.push(line);
        }
        else {
          linesCaptured.push(`# ${trimmedLine}`);
        }
      }
      else if (trimmedLine != "") {
        if (trimmedLine.startsWith("#")) {
          linesCaptured.push(line);
        }
        else {
          linesCaptured.push(`# ${trimmedLine}`);
        }
        newSelectionPos = lineStart;
        capturing = true;
      }
      else {
        linesUpdated.push(line);
      }
    }
    lineStart = lineEnd + 1;
  }
  if (linesCaptured.length > 0) {
    dom.editor.today.value = linesUpdated.join("\n");
    if (capturing) {
      dom.editor.today.value = dom.editor.today.value.trimEnd();
    }
    storeThenSave("value.today", dom.editor.today.value);
    dom.editor.today.setSelectionRange(newSelectionPos, newSelectionPos);
    let storedInboxValue = localStorage.getItem("value.inbox");
    storedInboxValue = appendToTop(storedInboxValue, linesCaptured.join("\n"));
    storeThenSave("value.inbox", storedInboxValue);
  }
}
function inboxSnoozeSelected() {
  const selectionStart = dom.editor.inbox.selectionStart;
  const selectionEnd = dom.editor.inbox.selectionEnd;
  let newSelectionPos;
  const lines = dom.editor.inbox.value.split("\n");
  const linesUpdated = [];
  const linesCaptured = [];
  let capturing = false;
  let lineStart = 0;
  let lineEnd;
  for (const line of lines) {
    lineEnd = lineStart + line.length;
    const trimmedLine = line.trimStart();
    if (lineEnd < selectionStart) {
      linesUpdated.push(line);
    }
    else if (lineStart > selectionEnd) {
      if (!capturing) {
        linesUpdated.push(line);
      }
      else if (trimmedLine != "") {
        linesUpdated.push(line);
        capturing = false;
      }
      else {
        linesUpdated.push(line);
        linesCaptured.push(line);
      }
    }
    else {
      if (capturing) {
        if (trimmedLine == "" || trimmedLine.startsWith("#")) {
          linesUpdated.push(line);
          linesCaptured.push(line);
        }
        else {
          linesUpdated.push(`# ${trimmedLine}`);
          linesCaptured.push(`# ${trimmedLine}`);
        }
      }
      else if (trimmedLine != "") {
        if (trimmedLine.startsWith("#")) {
          linesUpdated.push(line);
          linesCaptured.push(line);
        }
        else {
          linesUpdated.push(`# ${trimmedLine}`);
          linesCaptured.push(`# ${trimmedLine}`);
        }
        newSelectionPos = lineStart;
        capturing = true;
      }
      else {
        linesUpdated.push(line);
      }
    }
    lineStart = lineEnd + 1;
  }
  if (linesCaptured.length > 0) {
    newSelectionPos += linesCaptured.join("\n").length + 1; // + 1 to account for another \n
    let newInboxValue = linesUpdated.join("\n");
    if (capturing) {
      newInboxValue = newInboxValue.trimEnd();
    }
    storeThenSave("value.inbox", newInboxValue);
    const prevScrollTop = dom.editor.inbox.scrollTop;
    dom.editor.inbox.scrollTop = 0;
    dom.editor.inbox.value = newInboxValue.substring(0, newSelectionPos);
    dom.editor.inbox.scrollTop = dom.editor.inbox.scrollHeight;
    dom.editor.inbox.value = newInboxValue;
    dom.editor.inbox.scrollTop = Math.max(prevScrollTop, dom.editor.inbox.scrollTop);
    dom.editor.inbox.setSelectionRange(newSelectionPos, newSelectionPos);
  }
}
function selectUnsnoozed() {
  const lines = dom.editor.inbox.value.split("\n");
  const linesUnsnoozed = [];
  const linesSnoozed = [];
  let afterSnoozedLine = false;
  for (const line of lines) {
    const trimmedLine = line.trimStart();
    if (trimmedLine.startsWith("#")) {
      linesSnoozed.push(line);
      afterSnoozedLine = true;
    }
    else if (afterSnoozedLine && trimmedLine == "") {
      linesSnoozed.push(line);
    }
    else {
      linesUnsnoozed.push(line);
      afterSnoozedLine = false;
    }
  }
  const unsnoozed = linesUnsnoozed.join("\n").trimEnd();
  if (linesSnoozed.length > 0) {
    const snoozed = linesSnoozed.join("\n").trimEnd();
    dom.editor.inbox.value = `${unsnoozed}\n\n${snoozed}`;
  }
  else {
    dom.editor.inbox.value = unsnoozed;
  }
  storeThenSave("value.inbox", dom.editor.inbox.value);
  dom.editor.inbox.setSelectionRange(0, unsnoozed.length);
  dom.editor.inbox.scrollTop = 0;
  dom.editor.inbox.focus();
}
function appendToBottom(original, value) {
  const valueToAppend = value.trim();
  if (valueToAppend == "") {
    return original;
  }
  let updated = original.trimEnd();
  if (updated != "") {
    updated = `${updated}\n\n`;
  }
  return `${updated}${valueToAppend}`;
}
function appendToTop(original, value) {
  const valueToAppend = value.trim();
  if (valueToAppend == "") {
    return original;
  }
  let updated = original.trimStart();
  if (updated != "") {
    updated = `\n\n${updated}`;
  }
  return `${valueToAppend}${updated}`;
}
function appendToTopAndRemoveDupes(original, value) {
  let updated = original;
  const lines = value.split("\n");
  for (const line of lines) {
    const trimmedLine = line.trim();
    if (trimmedLine != "") {
      updated = removeDupesOfLine(updated, trimmedLine);
    }
  }
  return appendToTop(updated, value);
}
function removeDupesOfLine(original, trimmedLineTest) {
  const lines = original.split("\n");
  const linesUpdated = [];
  let capturing = false;
  for (const line of lines) {
    const trimmedLine = line.trim();
    if (trimmedLine == trimmedLineTest) {
      capturing = true;
    }
    else if (trimmedLine != "" || !capturing) {
      linesUpdated.push(line);
      capturing = false;
    }
  }
  let updated = linesUpdated.join("\n");
  if (capturing) {
    updated = updated.trimEnd();
  }
  return updated;
}
function unsnoozeEverything(original) {
  return original.replaceAll(/^( *#)+ */gm, "");
}
function updateCompleted(lines, offset) {
  let offsetDays = 0;
  if (offset.startsWith("-")) {
    offsetDays = parseInt(offset);
  } else if (offset != "") {
    const weekdayToday = (new Date()).getDay();
    const weekdayKeysRotated = weekdayKeys.slice(weekdayToday + 1).concat(weekdayKeys.slice(0, weekdayToday + 1));
    offsetDays = weekdayKeysRotated.indexOf(offset) - 6;
  }
  const dateCompletedObj = new Date();
  dateCompletedObj.setTime(dateCompletedObj.getTime() + (offsetDays * 86400000));
  const dateCompleted = dateCompletedObj.toDateString();
  const achievements = JSON.parse(localStorage.getItem("achievements"));
  let testIndex;
  for (testIndex = 0; testIndex < achievements.length; testIndex++) {
    if (achievements[testIndex].date == dateCompleted) {
      achievements[testIndex].tasks.unshift(...lines);
      storeThenSave("achievements", JSON.stringify(achievements));
      return;
    }
    const testTime = (new Date(achievements[testIndex].date)).getTime();
    if (testTime < dateCompletedObj.getTime()) {
      break;
    }
  }
  achievements.splice(testIndex, 0, {
    date: dateCompleted,
    tasks: lines
  });
  storeThenSave("achievements", JSON.stringify(achievements));
}
function updateValues() {
  const weekdayToday = (new Date()).getDay();
  const key = weekdayKeys[weekdayToday];
  const routine = localStorage.getItem(`routine.${key}`);
  const storedTodayValue = unsnoozeEverything(localStorage.getItem("value.today"));
  let storedInboxValue = unsnoozeEverything(localStorage.getItem("value.inbox"));
  storedInboxValue = appendToTopAndRemoveDupes(storedInboxValue, routine);
  storedInboxValue = appendToTopAndRemoveDupes(storedInboxValue, storedTodayValue);
  storeThenSave("value.today", "");
  storeThenSave("value.inbox", storedInboxValue);
}
function isNewDay() {
  const dateToday = (new Date()).toDateString();
  if (localStorage.getItem("date") == dateToday) {
    return false;
  }
  storeThenSave("date", dateToday);
  return true;
}
async function verifyUserAndAppendMessages() {
  if (openpgp === undefined) {
    openpgp = await import("./openpgp.min.mjs?sha1=280298d02f97111053fdb1215ac5011e0c7bd4fb");
  }
  lastAppend = Date.now();
  let response;
  try {
    response = await fetch(`${serverBase}open/post-remove-messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: localStorage.getItem("user.userID"),
        api_key: localStorage.getItem("user.apiKey")
      })
    });
  }
  catch (err) {
    return;
  }
  if (!response.ok) {
    return;
  }
  const result = await response.json();
  verifiedUser = result.success;
  if (!verifiedUser) {
    dom.fetchConnected.classList.remove("display");
    return;
  }
  if (result.messages.length > 0) {
    const pgpPrivateKeyObj = await openpgp.readKey({
      armoredKey: localStorage.getItem("user.pgpPrivateKey")
    });
    let storedInboxValue = localStorage.getItem("value.inbox");
    for (const encryptedMessage of result.messages) {
      const decrypted = await openpgp.decrypt({
        message: await openpgp.readMessage({
          armoredMessage: encryptedMessage
        }),
        decryptionKeys: pgpPrivateKeyObj
      });
      storedInboxValue = appendToTop(storedInboxValue, decrypted.data);
    }
    storeThenSave("value.inbox", storedInboxValue);
  }
  dom.fetchConnected.classList.add("display");
}
async function appendLocalMessages() {
  let response;
  try {
    response = await fetch("service/post-remove-messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        instance_id: instanceID
      })
    });
  }
  catch (err) {
    return;
  }
  if (!response.ok) {
    return;
  }
  const result = await response.json();
  if (!result.success || result.messages.length == 0) {
    return;
  }
  let storedInboxValue = localStorage.getItem("value.inbox");
  for (const message of result.messages) {
    storedInboxValue = appendToTop(storedInboxValue, message);
  }
  storeThenSave("value.inbox", storedInboxValue);
}
function setSnap() {
  if (localStorage.getItem("ui.snap") == "bottom") {
    dom.container.classList.add("docked");
    dom.snapToCenter.classList.add("display");
    dom.snapToBottom.classList.remove("display");
  }
  dom.snapToBottom.addEventListener("click", event => {
    event.preventDefault();
    toggleSnap();
  });
  dom.snapToCenter.addEventListener("click", event => {
    event.preventDefault();
    toggleSnap();
  });
}
function toggleSnap() {
  if (localStorage.getItem("ui.snap") == "center") {
    dom.container.classList.add("docked");
    dom.snapToCenter.classList.add("display");
    dom.snapToBottom.classList.remove("display");
    localStorage.setItem("ui.snap", "bottom");
  }
  else {
    dom.container.classList.remove("docked");
    dom.snapToBottom.classList.add("display");
    dom.snapToCenter.classList.remove("display");
    localStorage.setItem("ui.snap", "center");
  }
}
function setConfigureSave() {
  if (localStorage.getItem("saveMethod") === null) {
    dom.configureSave.classList.add("display");
    dom.popupSavePaused.classList.remove("display");
  }
  else {
    dom.configureSave.classList.remove("display");
  }
}
function setExportAndSave() {
  dom.exportData.addEventListener("click", () => {
    const dataJSON = createDataJSON();
    const dataBlob = new Blob([dataJSON], {
      type: "application/json; charset=utf-8"
    });
    dom.exportData.href = URL.createObjectURL(dataBlob);
  });
  if (usingLocalService) {
    setConfigureSave();
    return;
  }
  if ("showSaveFilePicker" in window) {
    dom.enableSave.classList.add("display");
    dom.enableSave.addEventListener("click", async event => {
      event.preventDefault();
      try {
        fileHandle = await window.showSaveFilePicker({
          suggestedName: `Frogtab_backup.json`,
          types: [{
            description: "JSON files",
            accept: {
              "application/json": [
                ".json"
              ]
            }
          }]
        });
      }
      catch (err) {
        return;
      }
      dom.enableSave.classList.remove("display");
      requestSave();
    });
  }
}
function createData() {
  let appBase = window.location.href;
  if (!appBase.endsWith("/")) {
    appBase = appBase.substring(0, appBase.lastIndexOf("/") + 1);
  }
  const data = {
    help: `To restore your data, visit ${appBase}help#importing-your-data`,
    date: localStorage.getItem("date"),
    today: localStorage.getItem("value.today").trim(),
    inbox: localStorage.getItem("value.inbox").trim(),
    routine: {}
  };
  for (const key of weekdayKeys) {
    data.routine[key] = localStorage.getItem(`routine.${key}`).trim();
  }
  if (localStorage.getItem("achievements") !== null) {
    data.achievements = JSON.parse(localStorage.getItem("achievements"));
  }
  if (localStorage.getItem("user.userID") !== null) {
    data.device = {
      userID: localStorage.getItem("user.userID"),
      apiKey: localStorage.getItem("user.apiKey"),
      pgpPublicKey: localStorage.getItem("user.pgpPublicKey"),
      pgpPrivateKey: localStorage.getItem("user.pgpPrivateKey")
    };
  }
  return data;
}
function createDataJSON() {
  const dataJSON = JSON.stringify(createData(), null, 2);
  return (new TextEncoder()).encode(dataJSON);
}
function storeThenSave(key, value) {
  localStorage.setItem(key, value);
  requestSave();
}
function requestSave() {
  if (usingLocalService && localStorage.getItem("saveMethod") !== null) {
    window.clearTimeout(timeoutSave.id);
    timeoutSave.id = window.setTimeout(saveToService, 1500);
    timeoutSave.waiting = true;
  }
  if (!usingLocalService && fileHandle !== null) {
    window.clearTimeout(timeoutSave.id);
    timeoutSave.id = window.setTimeout(saveToFile, 1500);
    timeoutSave.waiting = true;
  }
}
async function saveToService() {
  if (localStorage.getItem("saveMethod" === null)) {
    timeoutSave.waiting = false;
    return;
  }
  const data = createData();
  const onServiceFailure = () => {
    localStorage.removeItem("saveMethod");
    dom.configureSave.classList.add("display");
    timeoutSave.waiting = false;
  };
  let response;
  try {
    response = await fetch("service/post-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        key: localStorage.getItem("saveMethod"),
        data: data
      })
    });
  }
  catch (err) {
    if (showWelcome) {
      dom.welcome.classList.remove("display");
      showWelcome = false;
    }
    dom.popupSavePaused.classList.add("display");
    timeoutSave.waiting = false;
    return;
  }
  dom.popupSavePaused.classList.remove("display");
  if (!response.ok) {
    onServiceFailure();
    return;
  }
  const result = await response.json();
  if (!result.success) {
    onServiceFailure();
    return;
  }
  timeoutSave.waiting = false;
}
async function saveToFile() {
  if (fileHandle === null) {
    timeoutSave.waiting = false;
    return;
  }
  const dataJSON = createDataJSON();
  try {
    const stream = await fileHandle.createWritable();
    await stream.write(dataJSON);
    await stream.close();
  }
  catch (err) {
    fileHandle = null;
    dom.enableSave.classList.add("display");
  }
  timeoutSave.waiting = false;
}
async function startApp() {
  setExportAndSave();
  setSnap();
  if (isNewDay()) {
    updateValues();
  }
  switchToTab("today");
  if (requestedIcon === null) {
    await storeIcons();
  }
  setNotifyStatus();
  if (startingTab == "inbox" || (startingTab === null && notifyInbox)) {
    switchToTab("inbox");
    refreshInfo();
  }
  dom.editor.today.addEventListener("input", event => {
    if (event.inputType == "insertText" && localStorage.getItem("achievements") !== null) {
      addSpaceForCompletionOffset(dom.editor.today);
    }
    storeThenSave("value.today", dom.editor.today.value);
  });
  dom.editor.today.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key == "/") {
      event.preventDefault();
      todaySnoozeSelected();
      return;
    }
    if (localStorage.getItem("achievements") !== null) {
      if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "k") {
        event.preventDefault();
        completeSelected(dom.editor.today, "value.today", "");
        return;
      }
      if (!event.ctrlKey && !event.metaKey && !event.shiftKey && event.key.toLowerCase() == "enter") {
        const offset = extractCompletionOffset(dom.editor.today);
        if (offset !== null) {
          event.preventDefault();
          completeSelected(dom.editor.today, "value.today", offset);
        }
      }
    }
  });
  dom.today.addEventListener("click", () => {
    switchToTab("today");
    refreshInfo();
  });
  dom.today.addEventListener("keydown", event => {
    if (
      (!event.ctrlKey && !event.metaKey && !event.shiftKey && event.key.toLowerCase() == "enter")
      || event.key == " "
    ) {
      event.preventDefault();
      dom.today.click();
      dom.editor.today.focus();
    }
  });
  dom.editor.inbox.addEventListener("input", event => {
    if (event.inputType == "insertText" && localStorage.getItem("achievements") !== null) {
      addSpaceForCompletionOffset(dom.editor.inbox);
    }
    storeThenSave("value.inbox", dom.editor.inbox.value);
    setNotifyStatus();
    refreshInfo();
  });
  dom.editor.inbox.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() == "enter") {
      event.preventDefault();
      inboxMoveSelected();
      setNotifyStatus();
      refreshInfo();
      return;
    }
    if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key == "/") {
      event.preventDefault();
      inboxSnoozeSelected();
      setNotifyStatus();
      refreshInfo();
      return;
    }
    if (localStorage.getItem("achievements") !== null) {
      if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "k") {
        event.preventDefault();
        completeSelected(dom.editor.inbox, "value.inbox", "");
        setNotifyStatus();
        refreshInfo();
        return;
      }
      if (!event.ctrlKey && !event.metaKey && !event.shiftKey && event.key.toLowerCase() == "enter") {
        const offset = extractCompletionOffset(dom.editor.inbox);
        if (offset !== null) {
          event.preventDefault();
          completeSelected(dom.editor.inbox, "value.inbox", offset);
          setNotifyStatus();
          refreshInfo();
        }
      }
    }
  });
  dom.inbox.addEventListener("click", () => {
    switchToTab("inbox");
    refreshInfo();
  });
  dom.inbox.addEventListener("keydown", event => {
    if (
      (!event.ctrlKey && !event.metaKey && !event.shiftKey && event.key.toLowerCase() == "enter")
      || event.key == " "
    ) {
      event.preventDefault();
      dom.inbox.click();
      dom.editor.inbox.focus();
    }
  });
  dom.menuButton.addEventListener("click", event => {
    event.preventDefault();
    if (!dom.menu.classList.contains("display")) {
      event.stopPropagation();
      dom.menu.classList.add("display");
    }
  });
  dom.menuButton.addEventListener("keydown", event => {
    if (event.key.toLowerCase() == "arrowdown") {
      event.preventDefault();
      dom.menu.classList.add("display");
      const elements = document.querySelectorAll("[data-menu-seq].display");
      elements[0].focus();
    }
    else if (event.key.toLowerCase() == "arrowup") {
      event.preventDefault();
      dom.menu.classList.add("display");
      const elements = document.querySelectorAll("[data-menu-seq].display");
      elements[elements.length - 1].focus();
    }
  });
  document.addEventListener("click", () => {
    dom.menu.classList.remove("display");
  });
  dom.editor.today.addEventListener("focusin", () => {
    dom.menu.classList.remove("display");
  });
  dom.editor.inbox.addEventListener("focusin", () => {
    dom.menu.classList.remove("display");
  });
  dom.menu.addEventListener("keydown", event => {
    if (event.target.hasAttribute("data-menu-seq") && event.key.toLowerCase() == "arrowdown") {
      event.preventDefault();
      const elements = document.querySelectorAll("[data-menu-seq].display");
      const thisIndex = parseInt(event.target.getAttribute("data-menu-seq"), 10);
      const nextIndex = (thisIndex + 1) % elements.length;
      elements[nextIndex].focus();
    }
    else if (event.target.hasAttribute("data-menu-seq") && event.key.toLowerCase() == "arrowup") {
      event.preventDefault();
      event.preventDefault();
      const elements = document.querySelectorAll("[data-menu-seq].display");
      const thisIndex = parseInt(event.target.getAttribute("data-menu-seq"), 10);
      const prevIndex = (thisIndex - 1 + elements.length) % elements.length;
      elements[prevIndex].focus();
    }
    else if (event.key.toLowerCase() == "escape") {
      dom.menuButton.focus();
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      lastActive = Date.now();
    }
  });
  document.body.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "enter") {
      event.preventDefault();
      let value = dom.editor[selectedTab].value.trimStart();
      if (value != "") {
        value = `\n\n${value}`;
      }
      dom.editor[selectedTab].value = value;
      storeThenSave(`value.${selectedTab}`, dom.editor[selectedTab].value);
      dom.editor[selectedTab].setSelectionRange(0, 0);
      dom.editor[selectedTab].scrollTop = 0;
      dom.editor[selectedTab].focus();
      refreshInfo();
    }
    else if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "u") {
      event.preventDefault();
      switchToTab("today");
      dom.editor.today.focus();
      refreshInfo();
    }
    else if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() == "i") {
      event.preventDefault();
      if (!event.shiftKey || !notifyInbox) {
        switchToTab("inbox");
        dom.editor.inbox.focus();
        refreshInfo();
      }
      else {
        switchToTab("inbox");
        selectUnsnoozed();
      }
    }
    else if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "b") {
      event.preventDefault();
      toggleSnap();
    }
    else if (event.key.toLowerCase() == "escape") {
      dom.menu.classList.remove("display");
    }
  });
  for (const element of document.querySelectorAll("a")) {
    element.addEventListener("keydown", event => {
      if (event.key == " ") {
        event.preventDefault();
        element.click();
      }
    });
  }
  if (usingLocalService && instanceID != "") {
    await appendLocalMessages();
    setNotifyStatus();
    if (selectedTab == "inbox" || (startingTab === null && notifyInbox)) {
      switchToTab("inbox");
      refreshInfo();
    }
  }
  if (localStorage.getItem("user.userID") !== null) {
    userIDTested = localStorage.getItem("user.userID");
    await verifyUserAndAppendMessages();
    if (verifiedUser) {
      setNotifyStatus();
      if (selectedTab == "inbox" || (startingTab === null && notifyInbox)) {
        switchToTab("inbox");
        refreshInfo();
      }
    }
  }
  function preferInbox() {
    setNotifyStatus();
    if (notifyInbox) {
      switchToTab("inbox");
    }
    refreshInfo();
  }
  window.setInterval(async () => {
    if (isNewDay()) {
      updateValues();
      preferInbox();
      if (usingLocalService && instanceID != "") {
        await appendLocalMessages();
        preferInbox();
      }
      if (verifiedUser) {
        await verifyUserAndAppendMessages();
        preferInbox();
      }
      if (!notifyInbox) {
        switchToTab("today");
        refreshInfo();
      }
    }
    else {
      if (usingLocalService && instanceID != "") {
        await appendLocalMessages();
        setNotifyStatus();
        refreshView();
      }
      if (verifiedUser && lastAppend <= Date.now() - 600000) {
        await verifyUserAndAppendMessages();
        setNotifyStatus();
        refreshView();
      }
    }
    if (
      document.hidden && lastActive <= Date.now() - 30000
      && requestedIcon !== null && requestedReload !== null
      && !timeoutSave.waiting
      && localStorage.getItem("restore") === null
    ) {
      let reloadIcon = "normal";
      if (notifyInbox) {
        reloadIcon = "notify";
      }
      if (reloadIcon != requestedIcon) {
        const reloadParams = new URLSearchParams(window.location.search);
        reloadParams.set("reload", Date.now().toString());
        let reloadLocation = `icon-${reloadIcon}?${reloadParams.toString()}`;
        if (usingLocalService && instanceID != "") {
          reloadLocation = `${reloadLocation}#${encodeURIComponent(instanceID)}`;
        }
        try {
          // Before committing to the reload, verify that we can load the new location
          await fetch(reloadLocation);
          localStorage.setItem("tab", selectedTab);
          window.location.href = reloadLocation;
        }
        catch {}
      }
    }
  }, 15000);
  window.addEventListener("storage", async () => {
    document.documentElement.setAttribute("data-theme", localStorage.getItem("ui.theme"));
    if (usingLocalService) {
      setConfigureSave();
    }
    if (localStorage.getItem("user.userID") !== null && userIDTested !== localStorage.getItem("user.userID")) {
      userIDTested = localStorage.getItem("user.userID");
      await verifyUserAndAppendMessages();
      if (verifiedUser) {
        // Since the user has probably just sent a test message,
        // we'll set the last message fetch to be 8 minutes ago.
        // Then Frogtab will do another message fetch in 2 minutes.
        lastAppend -= 480000;
      }
    }
    else if (localStorage.getItem("user.userID") === null && userIDTested !== null) {
      userIDTested = null;
      verifiedUser = false;
      dom.fetchConnected.classList.remove("display");
    }
    setNotifyStatus();
    refreshView();
    requestSave();
  });
  window.addEventListener("hashchange", async () => {
    if (usingLocalService) {
      instanceID = decodeURIComponent(window.location.hash.substring(1));
      await appendLocalMessages();
      setNotifyStatus();
      refreshView();
    }
  })
}

// ******** Initial setup ********
let showWelcome = false;
const weekdayKeys = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
if (localStorage.getItem("restore") !== null) {
  const backupData = JSON.parse(localStorage.getItem("restore"));
  const uiSnap = localStorage.getItem("ui.snap");
  const uiTheme = localStorage.getItem("ui.theme");
  localStorage.clear();
  localStorage.setItem("date", backupData.date);
  localStorage.setItem("value.today", backupData.today);
  localStorage.setItem("value.inbox", backupData.inbox);
  for (const key of weekdayKeys) {
    localStorage.setItem(`routine.${key}`, backupData.routine[key]);
  }
  if ("achievements" in backupData) {
    localStorage.setItem("achievements", JSON.stringify(backupData.achievements));
  }
  if ("device" in backupData) {
    localStorage.setItem("user.pgpPublicKey", backupData.device.pgpPublicKey);
    localStorage.setItem("user.pgpPrivateKey", backupData.device.pgpPrivateKey);
    localStorage.setItem("user.apiKey", backupData.device.apiKey);
    localStorage.setItem("user.userID", backupData.device.userID);
  }
  localStorage.setItem("ui.snap", uiSnap);
  localStorage.setItem("ui.theme", uiTheme);
}
if (localStorage.getItem("date") === null) {
  localStorage.setItem("date", (new Date()).toDateString());
}
if (localStorage.getItem("value.today") === null) {
  // This is the user's first time opening Frogtab
  localStorage.setItem("value.today", "");
  showWelcome = true;
}
if (localStorage.getItem("value.inbox") === null) {
  localStorage.setItem("value.inbox", "");
}
for (const key of weekdayKeys) {
  if (localStorage.getItem(`routine.${key}`) === null) {
    localStorage.setItem(`routine.${key}`, "");
  }
}
if (localStorage.getItem("ui.snap") === null) {
  localStorage.setItem("ui.snap", "center");
}
if (localStorage.getItem("ui.theme") === null) {
  localStorage.setItem("ui.theme", "system");
}
document.documentElement.setAttribute("data-theme", localStorage.getItem("ui.theme"));
const requestedIcon = document.documentElement.getAttribute("data-icon");
const requestedReload = (new URLSearchParams(window.location.search)).get('reload');
const startingTab = localStorage.getItem("tab");
localStorage.removeItem("tab");
const dom = {
  container: document.getElementById("container"),
  icon16: document.getElementById("icon16"),
  icon32: document.getElementById("icon32"),
  welcome: document.getElementById("welcome"),
  editor: {
    today: document.getElementById("editor-today"),
    inbox: document.getElementById("editor-inbox")
  },
  today: document.getElementById("tab-today"),
  inbox: document.getElementById("tab-inbox"),
  info: document.getElementById("tab-info"),
  fetchConnected: document.getElementById("fetch-connected"),
  menuButton: document.getElementById("menu-button"),
  menu: document.getElementById("menu"),
  snapToBottom: document.getElementById("snap-to-bottom"),
  snapToCenter: document.getElementById("snap-to-center"),
  exportData: document.getElementById("export-data"),
  enableSave: document.getElementById("enable-save"),
  configureSave: document.getElementById("configure-save"),
  popupSavePaused: document.getElementById("popup-save-paused")
};
if (showWelcome) {
  dom.welcome.classList.add("display");
  dom.welcome.addEventListener("click", () => {
    dom.welcome.classList.remove("display");
    showWelcome = false;
  });
}
const storedIcons = {};
let notifyInbox = false;
let selectedTab = "today";
let fileHandle = null;
let timeoutSave = {
  id: 0,
  waiting: false
};
let timeoutShowInfo;
let lastActive = Date.now();
let usingLocalService = false;
let instanceID = null;
if (document.documentElement.getAttribute("data-save") == "service") {
  usingLocalService = true;
  instanceID = decodeURIComponent(window.location.hash.substring(1));
}
const serverBase = document.documentElement.getAttribute("data-server-base");
let userIDTested = null;
let verifiedUser = false;
let lastAppend = 0;
let openpgp;
startApp();