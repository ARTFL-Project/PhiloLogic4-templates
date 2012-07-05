<script>
$(document).ready(function(){
    $("#toggle_frequency").click(function() {
        toggle_frequency()
    });
    $("#frequency_field").change(function() {
        toggle_frequency()
    });
    $(".hide_frequency").click(function() {
        hide_frequency()
    });
});

function toggle_frequency() {
    var field = $("#frequency_field").val()
    if ($("#toggle_frequency").hasClass('show_frequency')) {
        $(".results_container").animate({
            "margin-right": "330px"},
            50);
        $("#freq").empty()
        $.getJSON("/philo4/${dbname}/scripts/get_frequency.py?term=${q['q']}&field=" + field, function(data) {
            $.each(data, function(index, item) {
                $("#freq").append('<p><li>' + item[0] + '<span style="float:right;padding-right:20px;">' + item[1] + '</li></p>');
            });
        });
        $(".hide_frequency").show()
        $("#freq").show()
    }
}
function hide_frequency() {
    $(".hide_frequency").fadeOut()
    $("#freq").hide()
    $(".results_container").animate({
        "margin-right": "0px"},
        50);
}
</script>
<div class="frequency_display">
<span class="hide_frequency" style="display:none;">X</span>
<span id="toggle_frequency" class="show_frequency">
Click to show frequency by:<select id='frequency_field' style="float:right;">
% for facet in db.locals["metadata_fields"]:
    <option value='${facet}'>${facet}</option>
% endfor
</select>
</span>
<div id="freq" class="frequency_table" style="display:none;"></div>
</div>