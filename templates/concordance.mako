<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<%namespace file="citation.mako" import="make_cite"/>
<div class='philologic_response'>
 <div class='philologic_concordance'>
  <div class='initial_report'>
  <p class='description'>Concordance Report</p>
  <%
  start, end, n = page_interval(results_per_page, len(results), q["start"], q["end"])
  biblio = set()
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${hitnum} for query "${q['q'].decode("utf-8", "ignore")}"
  </div>
  % for i in results[start - 1:end]:
   <div class='philologic_occurence'>
   <%
   n += 1
   biblio.add(i)
   %>
   ${make_cite(i, make_object_link, n)}
    <div class='philologic_context'>${report_function(i, path, q)}</div>
   </div>
  % endfor
 </div>
 <div class="more">
 <%
 prev, next = page_links(start, end, results_per_page, q, len(results))
 %>
 % if prev:
     <a href="${prev}" class="previous"> Back </a>
 % endif
 % if next:
     <a href="${next}" class="next"> Next </a>
 % endif
 </div>
</div>
<hr class="separation"/>
<div class='bibliography'>
<p class='description'>Results Bibliography</p>
${bibliography(biblio, 'author', 'title', form=false)}
</div>
<%include file="footer.mako"/>