console.log("Starting");

$(document).ready(function() {
    $(".delete-button").hide();
    $("#edit").click(function() {
        console.log("Hide event triggered.");
        $(".delete-button").toggle();
    });
});