function performAction(action) {
    fetch("/action", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ action })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}
