NUM_RELAY_PORTS = 16;

// Update relay visual status
function updateRelayStatus(relay, isOn) {
    const indicator = document.getElementById(`status-indicator-${relay}`);
    const text = document.getElementById(`status-text-${relay}`);

    if (indicator && text) {
        if (isOn) {
            indicator.className = 'status-indicator on';
            text.className = 'status-text on';
            text.textContent = 'مُشغل';
        } else {
            indicator.className = 'status-indicator off';
            text.className = 'status-text off';
            text.textContent = 'مُطفأ';
        }
    }
}

// Set loading state for relay
function setRelayLoading(relay, loading) {
    const card = document.getElementById(`relay-card-${relay}`);
    if (card) {
        if (loading) {
            card.classList.add('loading');
        } else {
            card.classList.remove('loading');
        }
    }
}

function setRelay(relay, status) {
    console.log("Executing setRelay");
    // Add loading state
    setRelayLoading(relay, true);
    callApiWithRelay(status + '/', relay);
}

function toggleRelay(relay) {
    console.log("Executing toggleRelay");
    setRelayLoading(relay, true);
    callApiWithRelay('toggle/', relay);
}

function callApiWithRelay(url, relay) {
    console.log("Executing callApiWithRelay");
    if (relay > 0 && relay < NUM_RELAY_PORTS + 1) {
        url += relay;
        callApiForRelay(url, relay);
    } else {
        console.error("Invalid port");
        Swal.fire({
            title: "Pi Relay Controller",
            text: "Invalid relay port passed to function setRelay",
            icon: "error"
        });
    }
}

function setAll(status) {
    console.log("Executing setAll");
    var url = status ? 'all_on/' : 'all_off/';
    callApi(url);
}

function toggleAll() {
    console.log("Executing toggleAll");
    for (var i = 1; i < NUM_RELAY_PORTS + 1; i++) {
        toggleRelay(i);
    }
}

// API call for specific relay
function callApiForRelay(url, relay) {
    console.log("Executing callApiForRelay for relay " + relay);
    $.get(url, function () {
        console.log("Sent request to server");
    }).done(function () {
        console.log("Completed request for relay " + relay);
        // Remove loading state and update status for this specific relay
        setTimeout(function() {
            setRelayLoading(relay, false);
            getRelayStatus(relay);
        }, 300);
    }).fail(function () {
        console.error("Relay status failure for relay " + relay);
        // Remove loading state
        setRelayLoading(relay, false);
        Swal.fire({
            title: "Pi Relay Controller",
            text: "Failed to communicate with relay " + relay,
            icon: "error"
        });
    });
}

// API call for all relays (used by setAll function)
function callApi(url) {
    console.log("Executing callApi");
    $.get(url, function () {
        console.log("Sent request to server");
    }).done(function () {
        console.log("Completed request");
        // Remove loading state and update status for all relays
        setTimeout(function() {
            for (let i = 1; i <= NUM_RELAY_PORTS; i++) {
                setRelayLoading(i, false);
                getRelayStatus(i);
            }
        }, 500);
    }).fail(function () {
        console.error("Relay status failure");
        // Remove loading state
        for (let i = 1; i <= NUM_RELAY_PORTS; i++) {
            setRelayLoading(i, false);
        }
        Swal.fire({
            title: "Pi Relay Controller",
            text: "Server returned an error",
            icon: "error"
        });
    });
}

function getRelayStatus(relay, showAlert = false) {
    console.log("Executing getRelayStatus for relay " + relay);
    $.get('status/' + relay, function () {
        console.log("Sent request to server");
    }).done(function (res) {
        console.log("Completed request for relay " + relay + ", status: " + res);
        const isOn = parseInt(res) > 0;
        updateRelayStatus(relay, isOn);

        if (showAlert) {
            var msg = isOn ? "مُشغل" : "مُطفأ";
            var title = "الريلي " + relay;
            Swal.fire({
                title: title,
                text: msg,
                icon: isOn ? "success" : "info",
                timer: 2000,
                showConfirmButton: false
            });
        }
    }).fail(function () {
        console.error("Relay status failure for relay " + relay);
        if (showAlert) {
            Swal.fire({
                title: "Pi Relay Controller",
                text: "Server returned an error",
                icon: "error"
            });
        }
    });
}

// Show relay status with alert (for status button)
function showRelayStatus(relay) {
    getRelayStatus(relay, true);
}

// Load all relay statuses on page load
function loadAllStatuses() {
    for (let i = 1; i <= NUM_RELAY_PORTS; i++) {
        getRelayStatus(i, false);
    }
}

// Initialize when page loads
$(document).ready(function() {
    console.log("Page loaded, updating relay statuses...");
    // Load statuses after a short delay to ensure page is fully loaded
    setTimeout(loadAllStatuses, 1500);

    // Add click handlers to prevent double-clicking
    $('.control-btn').on('click', function() {
        $(this).prop('disabled', true);
        setTimeout(() => {
            $(this).prop('disabled', false);
        }, 1000);
    });
});
