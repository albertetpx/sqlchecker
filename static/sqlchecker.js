let logoOK = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Eo_circle_green_white_checkmark.svg/480px-Eo_circle_green_white_checkmark.svg.png";
let logoKO = "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-color/700/010_x-512.png";

window.onload = function (e) {
    let images = document.getElementsByClassName('imgClickable');
    for (let image of images){
        image.addEventListener('click',toggleResults);
    }
};

function toggleResults(e){
    let collapsable = e.target.parentElement.nextElementSibling;
    if (collapsable.style.display != "flex"){
        collapsable.style.display = "flex";
    }
    else
        collapsable.style.display = "none";
}

function checkQuery(e) {
    let query = {
        no: e.id,
        query: e.previousElementSibling.value.toLowerCase()
    };

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        result = JSON.parse(this.responseText);
        // console.log(result);

        let logo = e.nextElementSibling;
        if (result['test'] == "1") {
            if(logo.src != logoOK){
                document.getElementById("counter").value = parseInt(counter = document.getElementById("counter").value) + 1;
            } 
            logo.src = logoOK;
        }
        else if (result['test'] == "0") {
            if(logo.src == logoOK){
                document.getElementById("counter").value = parseInt(counter = document.getElementById("counter").value) - 1;

            }
            logo.src = logoKO;
        }

        //Fill tables of EXPECTED RESULTS
        dataTable = e.parentElement.nextElementSibling.children[0]
        //Clean tables
        if (dataTable.children[0] != null){
            dataTable.children[0].remove();
        }
        table = document.createElement('table')
        //Fill table caption
        caption = document.createElement('caption');
        caption.style.cssText = "text-align: center; margin-bottom: 2vh;";
        caption.innerHTML = "Expected result";          
        table.append(caption);
        //Fill headings
        tr = document.createElement('tr');
        headings = result['headersok'];
        for (let heading of headings) {
            th = document.createElement('th');
            th.innerHTML = heading;
            tr.append(th);
        }
        table.append(tr);
        //Fill rows
        for (let row of result['dataok']){
            tr = document.createElement('tr');
            for (heading of headings) {
                td = document.createElement('td');
                td.innerHTML = row[heading];
                tr.append(td);
            }
            table.append(tr);
        }
        dataTable.append(table);
        //Fill tables of CURRENT QUERY RESULTS
        dataTable = e.parentElement.nextElementSibling.children[1]
        //Clean tables
        if (dataTable.children[0] != null){
            dataTable.children[0].remove();
        }
        table = document.createElement('table')
        //Fill table caption
        caption = document.createElement('caption');
        caption.style.cssText = "text-align: center; margin-bottom: 2vh;";
        caption.innerHTML = "Current query";
        table.append(caption);
        //Fill headings
        tr = document.createElement('tr');
        headings = result['headers'];
        for (let heading of headings) {
            th = document.createElement('th');
            th.innerHTML = heading;
            tr.append(th);
        }
        table.append(tr);
        //Fill rows
        for (let row of result['data']){
            tr = document.createElement('tr');
            for (heading of headings) {
                td = document.createElement('td');
                td.innerHTML = row[heading];
                tr.append(td);
            }
            table.append(tr);
        }
        dataTable.append(table);
    }

    exercise = document.location.href.substring(document.location.href.length - 3);
    xhttp.open("POST", "/"+exercise, true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(query));
}



