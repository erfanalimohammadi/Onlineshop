function search() {
    var input = document.getElementById('searchinput').value.toLowerCase();
    var content = document.getElementById('content').getElementsByTagName('p');
    if (input === '') {
        searchResults.innerHTML = 'Bitte geben Sie einen Suchbegriff ein.';
        return;
    }
    var results = [];

    for (var i = 0; i < content.length; i++) {
        var text = content[i].innerText.toLowerCase();
        if (text.includes(input)) {
            results.push(content[i].innerText);
        }
    }

    displayResults(results);
    
}

function displayResults(results) {
    var searchResults = document.getElementById('searchresults');
    searchResults.innerHTML = '';

    if (results.length === 0) {
        searchResults.innerHTML = 'Keine Ergebnisse gefunden.';
    } else {
        for (var i = 0; i < results.length; i++) {
            var p = document.createElement('p');
            p.textContent = results[i];
            searchResults.appendChild(p);
        }
    }

}
