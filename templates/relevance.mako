<%include file="header.mako"/>
<div class='philologic_response'>
  <div class='initial_report'>
  <p class='description'>
  <%
  start, end, n = f.link.page_interval(results_per_page, len(results), q["start"], q["end"])
  kwic = True
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)} for query "${q['q'].decode("utf-8", "ignore")}"
  </p>
  </div>
  <ol class='philologic_concordance'>
  % for i in results[start - 1:end]:
   <li class='philologic_occurence'>
   <%
   n += 1
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
   <span class='hit_n'>${n}.</span><a href='${url}'>${title}, ${author}</a>: ${sample_num} of ${hit_num} occurences displayed
   % if kwic:
    <div class="kwic_concordance">
   % endif
    <div class='philologic_context'>${fetch_relevance(i, path, q, kwic=kwic)}</div>
   % if kwic:
   </div>
   % endif
   </li>
  % endfor
  </ol>
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
   <div style='clear:both;'></div>
 </div>
</div>
<%include file="footer.mako"/>