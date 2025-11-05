
async function refreshLuasData() {
        try {
            const response = await fetch(luasTimesUrl);
            const data = await response.json();
            const tbody = document.querySelector("#luas-table tbody");
            tbody.innerHTML = ""; // clear old rows

            data.arrivals.forEach(a => {
                const row = `<tr>
                    <td>${a.direction}</td>
                    <td>${a.destination}</td>
                    <td>${a.due_mins}</td>
                </tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            });

            const now = new Date();
            const formatted = now.toLocaleTimeString('en-IE', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            document.getElementById("last-updated").textContent = "Last updated: " + formatted;
            } catch (err) {
                console.error("Error fetching data:", err);
            }
        }

        // Refresh every 15 seconds
        setInterval(refreshLuasData, 30000);