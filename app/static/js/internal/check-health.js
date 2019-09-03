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
    const checkHealthBtn = document.getElementById('checkHealthBtn')
    checkHealthBtn.disabled = true;
    checkHealthBtn.innerHTML = '<i class="fa fa-heart"></i>Loading...'
    checkHealthBtn.innerHTML += '&nbsp;&nbsp;<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true">'
    checkHealth().then(function (results) {
        for (const [hostname, details] of Object.entries(results)) {
            if (details.status === 'ERROR') {
                document.getElementById(hostname + "-status-entry").innerHTML = '<i class="fa fa-times"></i>'
                const modalBody = document.getElementById( hostname + 'ModalBody');
                details.errors.forEach(function(error) {
                    modalBody.innerHTML += '--> ' + error + '<br />'
                });
            } else if (details.status === 'OK') {
                document.getElementById(hostname + "-status-entry").innerHTML = '<i class="fa fa-check"></i>'
            }
        }
        checkHealthBtn.disabled = false;
        checkHealthBtn.innerHTML = '<i class="fa fa-heart"></i>Check Health'
    })
}

function openDetailsModal(hostname) {
    $('#' + hostname + 'Modal').modal('show')
}
