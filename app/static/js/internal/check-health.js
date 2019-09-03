const checkHealth = async () => {
    const healthResponse = await fetch('http://localhost:3321/api/check-health', {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    });
    const results = await healthResponse.json();
    //console.log(results);
    return results
};

function updateStatus() {
    //const statusTable = document.getElementById('statusTable');
    checkHealth().then(function (results) {
        for (const [key, value] of Object.entries(results)) {
            if (value.status === 'ERROR') {
                document.getElementById(key + "-status-entry").innerHTML = '<i class="fa fa-times"></i>'
            } else if (value.status === 'OK') {
                document.getElementById(key + "-status-entry").innerHTML = '<i class="fa fa-check"></i>'
            }
        }
    })
}