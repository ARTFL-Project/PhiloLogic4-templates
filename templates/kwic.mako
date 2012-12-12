<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_response'>
 <div class='initial_report'>
 <p class='description'>Kwic Report</p>
  <%
  start, end, n = f.link.page_interval(results_per_page, results, q["start"], q["end"])
  kwic_results = fetch_kwic(results, path, q, f.link.byte_query, start-1, end)
  %>
  Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)} for query "${q['q'].decode("utf-8", "ignore")}"
 </div>
 <%include file="show_frequency.mako"/>
 <div class="results_container">
  % for p, i in enumerate(kwic_results):
    <% pos = p + 1 %>
   <div class="kwic_concordance">
   % if len(str(end)) > len(str(pos)):
    <% spaces = ' ' * (len(str(end)) - len(str(pos))) %>
    <span id="position" style="white-space:pre-wrap;font-weight:900">${pos}.${spaces}</span>
   % else:
    <span id="position" style="font-weight:900">${pos}.</span>    
   % endif
   ${i}</div>  
  % endfor
 </div>
 <div class="more">
 <%include file="pages.mako" args="start=start,results_per_page=results_per_page,q=q,results=results"/>
 <div style='clear:both;'></div>
 </div>
</div>
<%include file="footer.mako"/>
