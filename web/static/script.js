 $(document).ready(function(){
    $("#switch").change(function(){
        if($(this).is(":checked")) {
            $.get("/on", function(){
                console.log("on");
            });
        }else{
            $.get("/off", function(){
                console.log("off");
            });
        }
    });
 });