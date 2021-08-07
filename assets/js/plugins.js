// place any jQuery/helper plugins in here, instead of separate, slower script files.

// makes search button have spinner
$(document).ready(function () {
    $("#btnFetch").click(function () {
        // disable button
        $(this).prop("disabled", true);
        // add spinner to button
        $(this).html(
            `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`
        );
    });
});