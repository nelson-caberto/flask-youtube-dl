
function queue(data) {
    //must hardcode ip else google why computer name fails
    fetch("http://10.0.0.198:5000", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        console.log("Request complete! response:", res);
    });
}