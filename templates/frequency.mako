<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<div class='philologic_frequency_report'>
 <p class='status'>Frequency Table</p>
<% field, counts = generate_frequency(results, q, db) %>
<table border="1" class="philologic_table">
  <tr><th class="table_header">${field}</th><th class="table_header">count</th></tr>
% for k,v,url in counts:
   <tr><td class="table_column"><a href='${url}'>${k}</a></td><td class="table_column">${v}</td></tr>
% endfor
</table>
</div>
<%include file="footer.mako"/>