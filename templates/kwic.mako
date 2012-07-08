<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<div class='philologic_response'>
 <div class='initial_report'>
 <p class='description'>Kwic Report</p>
  <%
  start, end, n = f.link.page_interval(results_per_page, len(results), q["start"], q["end"])
  kwic_results = fetch_kwic(results, path, q, f.link.byte_query, start-1, end)
  biblio = []
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)} for query "${q['q'].decode("utf-8", "ignore")}"
 </div>
 <%include file="show_frequency.mako"/>
 <div class="results_container">
  % for i, hit in kwic_results:
   <div class="kwic_concordance">${i}</div>
   <% biblio.append(hit) %>
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
<%include file="footer.mako"/>
