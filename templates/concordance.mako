<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_response'>
  <div class='initial_report'>
   <p class='description'>
    <%
     start, end, n = f.link.page_interval(results_per_page, results, q["start"], q["end"])
     r_status = "."
     if not results.done:
     	r_status += " Still working.  Refresh for a more accurate count of the results."
    %>
    Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)}${r_status}
   </p>
  </div>
<%include file="show_frequency.mako"/>
 <div class="results_container">
 <ol class='philologic_concordance'>
  % for i in results[start - 1:end]:
   <li class='philologic_occurrence'>
    <%
     n += 1
    %>
    <span class='hit_n'>${n}.</span> ${f.cite.make_div_cite(i)}
    <a href="javascript:void(0)" class="more_context">More</a>
    <div class='philologic_context'>${fetch_concordance(i, path, q)}</div>
   </li>
  % endfor
 </ol>
 </div>
 <div class="more">
 <%include file="pages.mako" args="start=start,results_per_page=results_per_page,q=q,results=results"/> 
   <div style='clear:both;'></div>
 </div>
</div>
<%include file="footer.mako"/>