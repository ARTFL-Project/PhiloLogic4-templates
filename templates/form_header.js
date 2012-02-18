<script type="text/javascript">
function autocomplete_metadata(metadata, field) {
    $("#" + field).autocomplete({
        source: "http://pantagruel.ci.uchicago.edu/philo4/${dbname}/scripts/metadata_list.py?field=" + field,
        minLength: 2,
        dataType: "json"
    });
}
var fields = ${repr(db.locals['metadata_fields'])}
$(document).ready(function(){
    $("#q").autocomplete({
        source: "http://pantagruel.ci.uchicago.edu/philo4/${dbname}/scripts/term_list.py",
        minLength: 2,
        "dataType": "json"
    });
    for (i in fields) {
        var  metadata = $("#" + fields[i]).val();
        var field = fields[i];
        autocomplete_metadata(metadata, field)
    }
//    The following is to display the right options when using the back button
    if ($("#report option[value='concordance']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#results_per_page").show()
    }
    if ($("#report option[value='kwic']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#results_per_page").show()
    }
    if ($("#report option[value='collocation']").attr('selected')) {
        $("#frequency").hide()
        $("#results_per_page").hide()
        $("#collocation").show()
    }
    if ($("#report option[value='frequency']").attr('selected')) {
        $("#collocation").hide()
        $("#results_per_page").hide()
        $("#frequency").show()
    }
});
function showHide(value) {
    if (value == 'frequency') {
        $("#collocation").hide()
        $("#results_per_page").hide()
        $("#frequency").show()
    }
    if (value == 'collocation') {
        $("#frequency").hide()
        $("#results_per_page").hide()
        $("#collocation").show()
    }
    if (value == 'concordance' || value == 'kwic') {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#results_per_page").show()
    }
}
</script>