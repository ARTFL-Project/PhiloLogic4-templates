<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<div class='philologic_response'>
 <div class='initial_report'>
 <p class='description'>Kwic Report</p>
  <%
  start, end, n = f.link.page_interval(results_per_page, results, q["start"], q["end"])
  kwic_results = fetch_kwic(results, path, q, f.link.byte_query, start-1, end)
  margin = False
  if len(str(start)) < len(str(end)):
    margin = True
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)} for query "${q['q'].decode("utf-8", "ignore")}"
 </div>
 <%include file="show_frequency.mako"/>
 <div class="results_container">
  % for p, i in enumerate(kwic_results):
   <div class="kwic_concordance">
   % if margin and len(str(p + 1)) == len(str(start)):
    <span id="position" style="white-space:pre-wrap;font-weight:900">${p + 1}. </span>
   % else:
    <span id="position" style="font-weight:900">${p + 1}.</span>    
   % endif
   ${i}</div>  
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
