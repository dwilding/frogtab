<?php

$page_state = '';
$icon16 = '/favicons/icon-16.png';
$icon32 = '/favicons/icon-32.png';
$query = $_SERVER['QUERY_STRING'];
if ($query == "t0a" || $query == "t1a" || $query == "i0a" || $query == "i1a") {
  $page_state = $query;
  if ($query == "t1a" || $query == "i1a") {
    $icon16 = '/favicons/icon-16-notify.png';
    $icon32 = '/favicons/icon-32-notify.png';
  }
}

?>
<!DOCTYPE html>
<html lang="en" data-theme="system" data-state="<?= $page_state ?>">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Frogtab is a lightweight task manager that helps you stay focused on today's priorities">
    <title>Frogtab</title>
    <link rel="icon" href="<?= $icon16 ?>" sizes="16x16" type="image/png" id="icon16">
    <link rel="icon" href="<?= $icon32 ?>" sizes="32x32" type="image/png" id="icon32">
    <link rel="apple-touch-icon" sizes="180x180" href="/favicons/icon-180-apple.png">
    <link rel="manifest" href="/manifest.webmanifest">
    <link rel="stylesheet" href="/style.css?sha1=f7b3e85916bd60de3022658696e22a5a1c70a139">
  </head>
  <body>
    <div id="container" class="container">
      <div class="interface">
        <a id="welcome" class="popup" href="https://frogtab.com/help#getting-started" target="_blank">
          Welcome! Click here to get started
        </a>
        <div class="tabs">
          <div class="tab">
            <span id="tab-today" class="tab-name selected">Today</span>
            <span id="tab-inbox" class="tab-name">Inbox</span>
            <span class="tab-icon">⬤</span>
          </div>
          <div class="tab info">
            <span id="tab-info" class="info-message">Your inbox is all set!</span>
            <span id="fetch-connected" class="info-message" title="Ready to receive tasks from any device"><svg width="20px" height="20px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor"><path d="M12 4c-6 0-6 4-6 6-1.667 0-5 1-5 5s3.333 5 5 5h12c1.667 0 5-1 5-5s-3.333-5-5-5c0-2 0-6-6-6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"></path></svg></span>
          </div>
        </div>
        <div class="main">
          <textarea id="editor-today" class="display"></textarea>
          <textarea id="editor-inbox"></textarea>
        </div>
        <div class="actions">
          <div class="action">
            <span id="menu-button" class="action-instruction display" title="Menu"><svg width="20px" height="20px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor"><path d="M3 5h18M3 12h18M3 19h18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg></span>
            <span id="enable-save" class="action-instruction">Enable Auto-Backup</span>
          </div>
          <div id="menu" class="action-menu">
            <a id="achievements" class="action-menu-item clickable" href="/achievements" target="_blank">Achievements</a>
            <a class="action-menu-item display clickable" href="/help" target="_blank">Help &amp; Privacy</a>
            <a id="export-data" class="action-menu-item display clickable" href="#" download="Frogtab_backup.json">Export My Data</a>
            <div class="action-menu-item display spacer"></div>
            <a class="action-menu-item display clickable" href="/send" target="_blank">Send to Frogtab</a>
            <a class="action-menu-item display clickable" href="/week" target="_blank">Weekly Routine</a>
            <div class="action-menu-item display spacer"></div>
            <span id="snap-to-bottom" class="action-menu-item display clickable">Snap to Bottom</span>
            <span id="snap-to-center" class="action-menu-item clickable">Snap to Center</span>
          </div>
        </div>
      </div>
    </div>
    <script>
      async function storeIcons() {
        const fetched = await Promise.all([
          fetch("/favicons/icon-16.png"),
          fetch("/favicons/icon-32.png"),
          fetch("/favicons/icon-16-notify.png"),
          fetch("/favicons/icon-32-notify.png")
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
          dom[selectedTab].classList.remove("selected");
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
          dom.inbox.classList.add("notify");
          dom.icon16.href = storedIcons.icon16Notify;
          dom.icon32.href = storedIcons.icon32Notify;
          notifyInbox = true;
        }
        else if (!checkValue(storedInboxValue) && notifyInbox) {
          dom.inbox.classList.remove("notify");
          dom.icon16.href = storedIcons.icon16;
          dom.icon32.href = storedIcons.icon32;
          notifyInbox = false;
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
      function inboxCompleteSelected() {
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
          dom.editor.inbox.value = linesUpdated.join("\n");
          if (capturing) {
            dom.editor.inbox.value = dom.editor.inbox.value.trimEnd();
          }
          storeThenSave("value.inbox", dom.editor.inbox.value);
          dom.editor.inbox.setSelectionRange(newSelectionPos, newSelectionPos);
          updateCompleted(linesCaptured);
        }
      }
      function todayCompleteSelected() {
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
          dom.editor.today.value = linesUpdated.join("\n");
          if (capturing) {
            dom.editor.today.value = dom.editor.today.value.trimEnd();
          }
          storeThenSave("value.today", dom.editor.today.value);
          dom.editor.today.setSelectionRange(newSelectionPos, newSelectionPos);
          updateCompleted(linesCaptured);
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
      function updateCompleted(lines) {
        const dateToday = (new Date()).toDateString();
        const achievements = JSON.parse(localStorage.getItem("achievements"));
        if (achievements.length > 0 && achievements[0].date == dateToday) {
          achievements[0].tasks.unshift(...lines);
        }
        else {
          achievements.unshift({
            date: dateToday,
            tasks: lines
          });
        }
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
          openpgp = await import("/lib-openpgp.min.mjs");
        }
        lastAppend = Date.now();
        let response;
        try {
          response = await fetch("/post-remove-messages", {
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
        const messages = [];
        const pgpPrivateKeyObj = await openpgp.readKey({
          armoredKey: localStorage.getItem("user.pgpPrivateKey")
        });
        for (const encryptedMessage of result.messages) {
          const decrypted = await openpgp.decrypt({
            message: await openpgp.readMessage({
              armoredMessage: encryptedMessage
            }),
            decryptionKeys: pgpPrivateKeyObj
          });
          messages.push(decrypted.data);
        }
        let storedInboxValue = localStorage.getItem("value.inbox");
        for (const message of messages) {
          storedInboxValue = appendToTop(storedInboxValue, message);
        }
        storeThenSave("value.inbox", storedInboxValue);
        dom.fetchConnected.classList.add("display");
      }
      function setAchievements() {
        if (localStorage.getItem("achievements") !== null) {
          dom.achievements.classList.add("display");
        }
        else {
          dom.achievements.classList.remove("display");
        }
      }
      function setSnap() {
        if (localStorage.getItem("ui.snap") == "bottom") {
          dom.container.classList.add("docked");
          dom.snapToCenter.classList.add("display");
          dom.snapToBottom.classList.remove("display");
        }
        dom.snapToBottom.addEventListener("click", event => {
          toggleSnap();
        });
        dom.snapToCenter.addEventListener("click", event => {
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
      function setExportAction() {
        if ("showSaveFilePicker" in window) {
          dom.enableSave.addEventListener("click", async event => {
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
          dom.enableSave.classList.add("display");
        }
        dom.exportData.addEventListener("click", event => {
          const dataJSON = createDataJSON();
          const dataBlob = new Blob([dataJSON], {
            type: "application/json; charset=utf-8"
          });
          dom.exportData.href = URL.createObjectURL(dataBlob);
        });
      }
      function createDataJSON() {
        const data = {
          help: "To restore your data, visit https://frogtab.com/help#importing-your-data",
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
        const dataJSON = JSON.stringify(data, null, 2);
        return (new TextEncoder()).encode(dataJSON);
      }
      function storeThenSave(key, value) {
        localStorage.setItem(key, value);
        requestSave();
      }
      function requestSave() {
        if (fileHandle !== null) {
          window.clearTimeout(timeoutSave);
          timeoutSave = window.setTimeout(saveToFile, 3000);
        }
      }
      async function saveToFile() {
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
      }
      async function startApp() {
        setAchievements();
        setSnap();
        setExportAction();
        if (isNewDay()) {
          updateValues();
        }
        switchToTab("today");
        await storeIcons();
        setNotifyStatus();
        if (notifyInbox && !pageState.startsWith("t")) {
          switchToTab("inbox");
        }
        dom.editor.today.addEventListener("input", event => {
          storeThenSave("value.today", dom.editor.today.value);
        });
        dom.editor.today.addEventListener("keydown", event => {
          if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "k" && localStorage.getItem("achievements") !== null) {
            event.preventDefault();
            todayCompleteSelected();
          }
          else if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key == "/") {
            event.preventDefault();
            todaySnoozeSelected();
          }
        });
        dom.today.addEventListener("click", event => {
          switchToTab("today");
          refreshInfo();
        });
        dom.editor.inbox.addEventListener("input", event => {
          storeThenSave("value.inbox", dom.editor.inbox.value);
          setNotifyStatus();
          refreshInfo();
        });
        dom.editor.inbox.addEventListener("keydown", event => {
          if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() == "k" && localStorage.getItem("achievements") !== null) {
            event.preventDefault();
            inboxCompleteSelected();
            setNotifyStatus();
            refreshInfo();
          }
          else if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() == "enter") {
            event.preventDefault();
            inboxMoveSelected();
            setNotifyStatus();
            refreshInfo();
          }
          else if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key == "/") {
            event.preventDefault();
            inboxSnoozeSelected();
            setNotifyStatus();
            refreshInfo();
          }
        });
        dom.inbox.addEventListener("click", event => {
          switchToTab("inbox");
          refreshInfo();
        });
        dom.menuButton.addEventListener("click", event => {
          if (!dom.menu.classList.contains("display")) {
            event.stopPropagation();
            dom.menu.classList.add("display");
          }
        });
        document.addEventListener("click", event => {
          dom.menu.classList.remove("display");
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
        });
        if (localStorage.getItem("user.userID") !== null) {
          hasUserID = true;
          await verifyUserAndAppendMessages();
          if (verifiedUser) {
            setNotifyStatus();
            if (notifyInbox && !pageState.startsWith("t")) {
              switchToTab("inbox");
            }
          }
        }
        window.setInterval(async () => {
          if (isNewDay()) {
            updateValues();
            if (verifiedUser) {
              await verifyUserAndAppendMessages();
            }
            setNotifyStatus();
            if (notifyInbox) {
              switchToTab("inbox");
            }
            else {
              switchToTab("today");
            }
            refreshInfo();
          }
          else if (verifiedUser && lastAppend <= Date.now() - 600000) {
            await verifyUserAndAppendMessages();
            setNotifyStatus();
            refreshView();
          }
          if (pageState != "" && document.hidden) {
            const newPageStateTab = selectedTab.slice(0, 1);
            let newPageStateNotify = "0";
            if (notifyInbox) {
              newPageStateNotify = "1";
            }
            const newPageState = `${newPageStateTab}${newPageStateNotify}a`;
            if (newPageStateNotify != pageState.slice(1, 2)) {
              window.location.href = `https://frogtab.com/?${newPageState}`;
            }
            else if (newPageState != pageState) {
              history.replaceState(null, "", `/?${newPageState}`);
            }
          }
        }, 15000);
        window.addEventListener("storage", async event => {
          setAchievements();
          document.documentElement.setAttribute("data-theme", localStorage.getItem("ui.theme"));
          if (!hasUserID && localStorage.getItem("user.userID") !== null) {
            hasUserID = true;
            await verifyUserAndAppendMessages();
            if (verifiedUser) {
              // Since the user has probably just sent a test message,
              // we'll set the last message fetch to be 8 minutes ago.
              // Then Frogtab will do another message fetch in 2 minutes.
              lastAppend -= 480000;
            }
          }
          else if (hasUserID && localStorage.getItem("user.userID") === null) {
            hasUserID = false;
            verifiedUser = false;
            dom.fetchConnected.classList.remove("display");
          }
          setNotifyStatus();
          refreshView();
          requestSave();
        });
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
      const pageState = document.documentElement.getAttribute("data-state");
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
        achievements: document.getElementById("achievements"),
        snapToBottom: document.getElementById("snap-to-bottom"),
        snapToCenter: document.getElementById("snap-to-center"),
        exportData: document.getElementById("export-data"),
        enableSave: document.getElementById("enable-save")
      };
      if (showWelcome) {
        dom.welcome.classList.add("display"); 
        dom.welcome.addEventListener("click", event => {
          dom.welcome.classList.remove("display");
        });
      }
      const storedIcons = {};
      let notifyInbox = false;
      let selectedTab = "today";
      let fileHandle = null;
      let timeoutSave;
      let timeoutShowInfo;
      let hasUserID = false;
      let verifiedUser = false;
      let lastAppend = 0;
      let openpgp;
      startApp();
    </script>
  </body>
</html>