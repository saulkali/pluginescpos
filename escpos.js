const apiRouter = "127.0.0.1:5656";
const getPrinter = ()=> {
    $.ajax({
        type: "GET",
        url: "url",
        contentType:"application/json",
        success: function (response) {
            if(response.status == "OK"){
            }else if(response.status == "ERROR"){
                M.toast({
                    html:"error: " + response.error
                });
            }
        }
    });
};