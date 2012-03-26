<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<%namespace file="citation.mako" import="make_cite"/>
<div class='philologic_response'>
 <div class='philologic_concordance'>
  <div class='initial_report'>
  <p class='description'>Ranked relevance Report</p>
  <%
  start, end, n = page_interval(results_per_page, len(results), q["start"], q["end"])
  biblio = set()
  kwic = True
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${hitnum} for query "${q['q'].decode("utf-8", "ignore")}"
  </div>
  % for i in results[start - 1:end]:
   <div class='philologic_occurence'>
   <%
   n += 1
   biblio.add(i)
   author = i.author
   title = i.title
   q["metadata"]['author'] = author
   q["metadata"]['title'] = title
   url = make_query_link(q["q"],q["method"],q["arg"],**q["metadata"])
   %>
   <a href='${url}'>${title}, ${author}</a> score: ${i.score}
   % if kwic:
    <div class="kwic_concordance">
   % endif
    <div class='philologic_context'>${report_function(i, path, q, kwic=kwic)}</div>
   % if kwic:
   </div>
   % endif
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