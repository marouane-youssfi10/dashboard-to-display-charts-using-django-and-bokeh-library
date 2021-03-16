function myFunction_city() {
    var search = document.querySelector('#search_city');
    var results = document.querySelector('#searchresults_city');
    var templateContent = document.querySelector('#resultstemplate_city').content;
        search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var clonedOptions = templateContent.cloneNode(true);
    var set = Array.prototype.reduce.call(clonedOptions.children, function searchFilter(frag, el) {
        if (inputVal.test(el.textContent) && frag.children.length < 5) frag.appendChild(el);
        return frag;
        }, document.createDocumentFragment());
        results.appendChild(set);
        });
}