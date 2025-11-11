function selectStop() {
            const stop = document.getElementById('stop-select').value;
            // Redirect to the same view but with a query parameter
            window.location.href = `/?stop=${stop}`;
        }