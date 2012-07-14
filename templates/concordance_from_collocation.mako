<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_response'>
  <div class='initial_report'>
   <p class='description'>
    <%
     colloc_results = fetch_colloc_concordance(results, path, q)
     start, end, n = f.link.page_interval(results_per_page, colloc_results, q["start"], q["end"])
    %>
    Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(colloc_results)}
   </p>
  </div>
<%include file="show_frequency.mako"/>
 <div class="results_container">
 <ol class='philologic_concordance'>
  % for i in colloc_results[start - 1:end]:
   <li class='philologic_occurrence'>
    <%
     n += 1
    %>
    <span class='hit_n'>${n}.</span> ${f.cite.make_div_cite(i)}
    <a href="javascript:void(0)" class="more_context">Show more context</a>
    <div class='philologic_context'>${fetch_concordance(i, path, q)}</div>
   </li>
  % endfor
 </ol>
 </div>
 <div class="more">
  <%
   prev, next = f.link.page_links(start, end, results_per_page, q, len(colloc_results))
  %>
   % if prev:
    <a href="${prev}" class="previous"> Back </a>
   % endif
   % if next:
    <a href="${next}" class="next"> Next </a>
   % endif
   <div style='clear:both;'></div>
 </div>
</div>
<%include file="footer.mako"/>