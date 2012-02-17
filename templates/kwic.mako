<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<div class='philologic_concordance'>
 <div class='initial_report'>
 <p class='description'>Kwic Report</p>
  <%
  start, end, n = page_interval(results_per_page, len(results), q["start"], q["end"])
  kwic_results = report_function(results, path, q, byte_query, start-1, end)
  biblio = []
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${hitnum} for query "${q['q'].decode("utf-8")}"
 </div>
  % for i, hit in kwic_results:
   <div class="kwic_concordance">${i}</div>
   <% biblio.append(hit) %>
  % endfor
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
<hr style="width:30%;text-align:left;margin-left:0"/>
<div class='Bibliography'>
<p class='description'>Results Bibliography</p>
${bibliography(biblio, 'author', 'title', form=False)}
</div>
<%include file="footer.mako"/>
