//ubiquitin is a small protein having the peptide sequence:
//MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
//It is so named because it's present in all eukaryotic cells (i.e. it is
//everywhere), and has become a model protein for experimental technique.
//
//This file is intended to be similar.

//theme: https://coolors.co/383f51-49111c-e2d4b7-5c0029-b5bec6

var colors = ['#104060','#125b94','#1f7fc1','#67add8']
var apiRoot = "http://kwisatz.hadera.ch:5001/"

// Use the browser's built-in functionality to quickly and safely escape the string
function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

$("#footer").click(function() {
    window.location.assign("/webapp/")
})

$("#footext").html("<i>All that is not saved will be lost.</i>")
