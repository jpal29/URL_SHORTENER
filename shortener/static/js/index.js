console.log("Starting");

$(document).ready(function() {
    $(".delete-input").hide();
    $("#edit").click(function() {
        console.log("Hide event triggered.");
        $(".delete-input").toggle();
    });
});