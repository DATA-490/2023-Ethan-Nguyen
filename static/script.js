document.addEventListener('htmx:afterRequest', function() {
    loading();
});

document.getElementById("subreddit").addEventListener("keypress", function(event) {
    if(event.key == "Enter") {
        document.getElementById("searchterm").focus();
    }
});

document.getElementById("searchterm").addEventListener("keypress", function(event) {
    if(event.key === "Enter") {
        document.getElementById("searchbtn").focus();
    }
});

function sentOverTime() {
    var subreddit = document.getElementById("subreddit").value;
    var searchterm = document.getElementById("searchterm").value;

    xhttpObj = new XMLHttpRequest();
    
    xhttpObj.onload = function() {
        
        if(this.responseText == -1) {
            return;
        }
        
        var response = JSON.parse(this.responseText);
        
        let chartStatus = Chart.getChart("overTimeGraph");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }

        var loadingGraph = document.getElementById("loading-graph");
        loadingGraph.style.display = "none";

        var overTimeGraph = document.getElementById("overTimeGraph");
        
        new Chart(overTimeGraph, {
            type: 'line',
            data: {
                labels: response.years,
                datasets: [{
                    label: "Subreddit Sentiment by Year",
                    data: response.sentiment,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        min: -1,
                        max: 1,
                        ticks: {
                            stepSize: 0.25,
                            callback: function(value, index, values) {
                                if(value === 0) {
                                    return "neutral";
                                }
                                else if(value === -0.25) {
                                    return "negative";
                                }
                                else if(value === 0.25) {
                                    return "positve";
                                }
                                else if(value === -0.75) {
                                    return "very negative";
                                }
                                else if(value === 0.75) {
                                    return "very positive";
                                }
                                else {
                                    return "";
                                } 
                            }
                        }
                    }
                }
            }
        });
    };
    xhttpObj.open("GET", "/sentovertime?subreddit=" + subreddit + "&searchterm=" + searchterm);
    xhttpObj.send();
}

function loading() {
    var searchbtn = document.getElementById("searchbtn");
    
    if(window.pJSDom[0].pJS.particles.move.speed == 10) {
        window.pJSDom[0].pJS.particles.move.speed = 3;
        searchbtn.disabled = false;
        searchbtn.classList.add('btn-outline-secondary');
        searchbtn.classList.remove('btn-secondary');
    }
    else {
        window.pJSDom[0].pJS.particles.move.speed = 10;
        searchbtn.disabled = true;
        searchbtn.classList.remove('btn-outline-secondary');
        searchbtn.classList.add('btn-secondary');
    }
}

function subCorrection(subLink) {
    var subredditInput = document.getElementById("subreddit");
    var searchbtn = document.getElementById("searchbtn");
    var subreddit = subLink.innerHTML.slice(2);
    
    subredditInput.value = subreddit;
    searchbtn.click();
}