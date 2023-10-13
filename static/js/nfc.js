// if (!('NDEFWriter' in window)) {
//     changeStatus("portable_wifi_off", "NFC not supported on this device or browser")
// }

async function writeNfc(url) {
    try {
        const ndef = new NDEFReader();
        changeStatus("wifi_tethering", "Place NFC tag on the back of the phone")
        await ndef.write({
            records: [{recordType: "url", data: url}],
        });
        changeStatus("done", "NFC tag has been written")
    } catch (error) {
        changeStatus("warning", "Error while initializing NFC - " + error.message )
    }
}

function changeStatus(icon, text, button=true) {
    var i = document.getElementById("nfc-status-icon")
    var s = document.getElementById("nfc-status-text")
    var b = document.getElementById("nfc-status-button")
    i.innerHTML = icon
    s.innerHTML = text
    b.disabled = button
}