<script>
$(document).ready(function(){
    $(".more_context").click(function() {
        var context_link = $(this).text();
        if (context_link == 'Show more context') {
            $(this).prevAll('.philologic_context:last').children('.begin_concordance').show()
            $(this).prevAll('.philologic_context:last').children('.end_concordance').show()
            $(this).empty().fadeIn().append('Hide')
        } 
        else {
            $(this).prevAll('.philologic_context:last').children('.begin_concordance').hide()
            $(this).prevAll('.philologic_context:last').children('.end_concordance').hide()
            $(this).empty().fadeIn().append('Show more context')
        }
    });
});
</script>