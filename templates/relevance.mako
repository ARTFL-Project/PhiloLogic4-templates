<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_response'>
  <div class='initial_report'>
   <p class='description'>
    <%
     start, end, n = f.link.page_interval(results_per_page, results, q["start"], q["end"])
    %>
    Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)}
   </p>
  </div>
<%include file="show_frequency.mako"/>
<%include file="more_context.mako"/>
 <div class="results_container">
 <ol class='philologic_concordance'>
  % for i in results[start - 1:end]:
    <li class='philologic_occurrence'>
   <%
   n += 1
   author = i.author
   title = i.title
   from copy import deepcopy
   link_metadata = deepcopy(q["metadata"])
   link_metadata['author'] = author.encode('utf-8', 'ignore')
   link_metadata['title'] = title.encode('utf-8', 'ignore')
   url = f.link.make_query_link(q["q"],q["method"],q["arg"],**link_metadata)
   hit_num = len(i.bytes)
   if hit_num >= 3:
       sample_num = 3
   else:
       sample_num = hit_num 
   %>
   <span class='hit_n'>${n}.</span><a href='${url}'> ${title}, ${author}</a>: ${sample_num} of ${hit_num} occurences displayed
   <span class="score">score: ${i.score}</span>
   <div class='philologic_context'><span class="kwic_concordance">${fetch_relevance(i, path, q)}</span></div>
   </li>
  % endfor
  </ol>
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
   <div style='clear:both;'></div>
 </div>
</div>
<%include file="footer.mako"/>