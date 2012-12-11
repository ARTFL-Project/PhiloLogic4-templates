<script>
$(document).ready(function(){
    $("#toggle_frequency").click(function() {
        toggle_frequency();
    });
    $("#frequency_field").change(function() {
        toggle_frequency();
    });
    $(".hide_frequency").click(function() {
        hide_frequency();
    });
});

function toggle_frequency() {
    $(".loading").empty().hide();
    var field = $("#frequency_field").val();
    var spinner = '<img src="/philo4/${dbname}/js/spinner-round.gif" alt="Loading..." />';
    if ($("#toggle_frequency").hasClass('show_frequency')) {
        $(".results_container").animate({
            "margin-right": "330px"},
            50);
        $("#freq").empty();
        $(".loading").append(spinner).show();
        $.getJSON("/philo4/${dbname}/scripts/get_frequency.py?frequency_field=" + field + '&${q['q_string']}', function(data) {
            $(".loading").hide().empty();
            $.each(data, function(index, item) {
                if (item[0].length > 30) {
                    var url = '<a href="' + item[2] + '">' + item[0].slice(0,30) + '[...]</a>'
                } else {
                    var url = '<a href="' + item[2] + '">' + item[0] + '</a>'
                } 
                $("#freq").append('<p><li>' + url + '<span style="float:right;padding-right:20px;">' + item[1] + '</span></li></p>');
            });
        });
        $(".hide_frequency").show();
        $("#freq").show();
    }
}
function hide_frequency() {
    $(".hide_frequency").fadeOut();
    $("#freq").hide();
    $(".results_container").animate({
        "margin-right": "0px"},
        50);
}
</script>
<div class="frequency_display">
<span id="toggle_frequency" class="show_frequency">
<a href="javascript:void(0)">Click to show frequency by:</a>
</span>
<a href="javascript:void(0)" class="hide_frequency" style="display:none;">X</a>
<select id='frequency_field'>
% for facet in db.locals["metadata_fields"]:
    <option value='${facet}'>${facet}</option>
% endfor
</select>
<div class="loading" style="display:none;"></div>
<div id="freq" class="frequency_table" style="display:none;"></div>
</div>