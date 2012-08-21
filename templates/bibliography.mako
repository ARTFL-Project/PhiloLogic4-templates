<%include file="header.mako"/>
<%include file="search_boxes.mako"/>
<script>
$(document).ready(function(){
    $(".form_body").show();
    var content_width = 100 + $(".form_body").width() + $(".bibliography_results").width();
    if ($(window).width() > content_width) {
        float_left();
    }
    else {
        float_below();
    }
    $(window).resize(function() {
        if ($(window).width() > content_width) {
            float_left();
        }
        else {
            float_below();
        }
    });
});

function float_left() {
    $(".form_body").css('float', 'left');
    $(".results_container").css('float', 'left');
    $('.description').fadeIn();
    $(".bibliographic_results").fadeIn();
}
function float_below() {
    $(".results_container").css('float', 'none');
    $(".form_body").css('float', 'none');
    $('.description').show();
    $(".bibliographic_results").show();
}
</script>
<div class="results_container">
<div class='philologic_response'>
 <p class='description' style="display:none;">Bibliography Report: ${len(results)} results.</p>
 <div class='bibliographic_results'>
 <ol class='philologic_cite_list'>
 % for i in results:
  <li class='philologic_occurrence'>
  <input type="checkbox" name="philo_id" value="${i.philo_id}">
  % if i.type == 'doc':
  <span class='philologic_cite'>${f.cite.make_doc_cite(i)}</span>
  % else:
  <span class='philologic_cite'>${f.cite.make_div_cite(i)}</span>
  % endif
  </li>
 % endfor
 </ol>
</div>
</div>
</div>
<%include file="footer.mako"/>
