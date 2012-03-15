<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<%namespace file="citation.mako" import="make_cite"/>
<div class='philologic_response'>
 <div class='philologic_concordance'>
  <div class='initial_report'>
  <p class='description'>Ranked relevance Report</p>
  <%
  biblio = set()
  n = 0
  %>
 ${hitnum} hits for query "${q['q'].decode("utf-8", "ignore")}"
  </div>
  % for i in results:
   <div class='philologic_occurence'>
   <%
   n += 1
   biblio.add(i)
   %>
   ${make_cite(i, make_object_link, n)}, ${i.score}
   <div class='philologic_context'>${report_function(i, path, q)}</div>
   </div>
  % endfor
 </div>
</div>
<hr class="separation"/>
<div class='bibliography'>
<p class='description'>Results Bibliography</p>
${bibliography(biblio, 'author', 'title', form=false)}
</div>
<%include file="footer.mako"/>