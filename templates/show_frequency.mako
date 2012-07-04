<script>
$(document).ready(function(){
    $("#toggle_frequency").click(function() {
        if ($("#toggle_frequency").hasClass('show_frequency')) {
            $(".results_container").animate({
                "margin-right": "350px"},
                50);
            if ($("#freq").is(':empty')) {
                $.getJSON("/philo4/${dbname}/scripts/get_frequency.py?term=${q['q']}", function(data) {
                    $.each(data, function(index, item) {
                        $("#freq").append('<p><li>' + item[0] + '<span style="float:right;padding-right:20px;">' + item[1] + '</li></p>');
                    });
                });
            }
            $("#toggle_frequency").attr('class', 'hide_frequency')
            $("#toggle_frequency").empty().append('Hide frequency')
            $("#freq").show()
        }
        else {
            $("#freq").hide()
            $(".results_container").animate({
                "margin-right": "0px"},
                50);
            $("#toggle_frequency").attr('class', 'show_frequency')
            $("#toggle_frequency").empty().append('Show frequency')
        }
    });
});
</script>
<span class="frequency_display">
<span id="toggle_frequency" class="show_frequency">Show frequency by author</span>
<div id="freq" class="frequency_table" style="display:none;"></div>
</span>