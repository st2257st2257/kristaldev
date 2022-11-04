function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
function show_user_by_id(elem){ 
    theUrl = "/url_request/";
    request_id = String(elem.id).split("_")[0];
    request = document.getElementById(request_id + "_value").value;
    res = JSON.parse(httpGet(theUrl + request));
    data = res["data"];
    cargo = document.getElementById(String(request_id) + "_cargo")
    cargo.innerHTML = "<p>Data: " + data + "</p>"
}
