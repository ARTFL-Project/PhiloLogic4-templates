<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<%namespace file="citation.mako" import="make_cite"/>
<div class='philologic_response'>
 <div class='philologic_concordance'>
  <div class='initial_report'>
  <p class='description'>Ranked relevance Report</p>
  <%
  start, end, n = f.link.page_interval(results_per_page, len(results), q["start"], q["end"])
  biblio = []
  kwic = True
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)} for query "${q['q'].decode("utf-8", "ignore")}"
  </div>
  % for i in results[start - 1:end]:
   <div class='philologic_occurence'>
   <%
   n += 1
   biblio.append(i)
   author = i.author
   title = i.title
   from copy import deepcopy
   link_metadata = deepcopy(q["metadata"])
   link_metadata['author'] = author
   link_metadata['title'] = title
   url = f.link.make_query_link(q["q"],q["method"],q["arg"],**link_metadata)
   hit_num = len(i.bytes)
   if hit_num >= 4:
       sample_num = 4
   else:
       sample_num = hit_num 
   %>
   ${n}. <a href='${url}'>${title}, ${author}</a>: ${sample_num} of ${hit_num} occurences displayed
   % if kwic:
    <div class="kwic_concordance">
   % endif
    <div class='philologic_context'>${fetch_relevance(i, path, q, kwic=kwic)}</div>
   % if kwic:
   </div>
   % endif
   </div>
  % endfor
 </div>
 <div class="more">
 <%
 prev, next = f.link.page_links(start, end, results_per_page, q, len(results))
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