<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_frequency_report'>
 <p class='status'>Frequency Table</p>
<% field, counts = generate_frequency(results, q, db) %>
<table border="1" class="philologic_table">
  <tr><th>${field}</th><th>count</th></tr>
% for k,v,url in counts:
   <tr><td><a href='${url}'>${k}</a></td><td>${v}</td></tr>
% endfor
</table>
</div>
<%include file="footer.mako"/>