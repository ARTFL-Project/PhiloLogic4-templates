<script>
$(document).ready(function(){
    $(".more_context").click(function() {
        var context_link = $(this).text();
        var spinner = '<img style="padding-left:80px;" src="/philo4/${dbname}/js/spinner-round.gif" alt="Loading..." />'
        if (context_link == 'Show more context') {
            var num = $(this).prevAll('.hit_n:last').text().replace('.', '') - 1
            var context = this;
            $(this).empty()
            $(this).prevAll('.philologic_context:last').empty().append(spinner)
            $.get('/philo4/${dbname}/scripts/more_context.py?hit_num=' + num + '&length=2000' +'&${q["q_string"]}', function(data) {
                $(context).prevAll('.philologic_context:last').empty().hide().append(data).fadeIn();
                $(context).fadeIn().append('Hide')
            });
        } 
        else {
            var num = $(this).prevAll('.hit_n:last').text().replace('.', '') - 1
            var context = this;
            $(this).empty()
            $(this).prevAll('.philologic_context:last').empty().append(spinner)
            $.get('/philo4/${dbname}/scripts/more_context.py?hit_num=' + num + '&length=400' +'&${q["q_string"]}', function(data) {
                $(context).prevAll('.philologic_context:last').empty().hide().append(data).fadeIn();
                $(context).fadeIn().append('Show more context')
            });
        }
    });
});
</script>