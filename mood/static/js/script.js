function like(url)
    {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", url, false);
        xmlHttp.send(null);
        console.log(`Like ${url}`);
        return xmlHttp.responseText;
    }