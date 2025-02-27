
document.addEventListener("DOMContentLoaded", function () {
    fetch("{% static 'js/data.json' %}")
        .then(response => response.json())
        .then(data => {
            if (document.getElementById("surveyTable")) {
                populateTable(data);
            } else {
                generateCharts(data);
            }
        })
        .catch(error => console.error("Error loading data:", error));
});

function populateTable(data) {
    const tableBody = document.querySelector("#surveyTable tbody");
    tableBody.innerHTML = "";
    data.forEach(entry => {
        const row = `
            <tr>
                <td>${entry.name}</td>
                <td>${entry.email}</td>
                <td>${entry.gender}</td>
                <td>${entry.age}</td>
                <td>${entry.region}</td>
                <td>${entry.source}</td>
                <td>${entry.usageDuration}</td>
                <td>${entry.mattressType}</td>
                <td>${entry.comfort}</td>
                <td>${entry.quality}</td>
                <td>${entry.supportRating}</td>
                <td>${entry.purchaseLocation}</td>
                <td>${entry.shoppingExperience}</td>
                <td>${entry.priceSatisfaction}</td>
                <td>${entry.productDetails}</td>
                <td>${entry.likes}</td>
                <td>${entry.improvements}</td>
                <td>${entry.recommendation}</td>
                <td>${entry.comments}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

function generateCharts(data) {
    let comfort = {}, quality = {}, recommendation = {}, age = {}, region = {}, mattress = {}, source = {}, gender={};

    data.forEach(entry => {
        comfort[entry.comfort] = (comfort[entry.comfort] || 0) + 1;
        quality[entry.quality] = (quality[entry.quality] || 0) + 1;
        recommendation[entry.recommendation] = (recommendation[entry.recommendation] || 0) + 1;
        gender[entry.gender] = (gender[entry.gender] || 0) + 1;
        age[entry.age] = (age[entry.age] || 0) + 1;
        region[entry.region] = (region[entry.region] || 0) + 1;
        mattress[entry.mattressType] = (mattress[entry.mattressType] || 0) + 1;
        source[entry.source] = (source[entry.source] || 0) + 1;
    });

    createChart("comfortChart", "bar", comfort);
    createChart("qualityChart", "pie", quality);
    createChart("sourceChart","line", source);
    createChart("genderChart", "bar", gender)
}

function createChart(id, type, data) {
    new Chart(document.getElementById(id), { type, data: { labels: Object.keys(data), datasets: [{ data: Object.values(data) }] } });
}
