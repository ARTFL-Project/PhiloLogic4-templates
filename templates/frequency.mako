<%include file="header.mako"/>
<div class='philologic_frequency_report'>
 <p class='status'>Frequency Table</p>
<% field, counts = generate_frequency(results, q, db) %>
<table border="1" class="philologic_table">
  <tr><th>${field}</th><th>count</th></tr>
% for k,v in counts:
   <% 
   q["metadata"][field] = '"%s"' % k or "NULL"
   url = f.link.make_query_link(q["q"],q["method"],q["arg"],**q["metadata"])
   %>
   <tr><td><a href='${url}'>${k}</a></td><td>${v}</td></tr>
% endfor
</table>
</div>
<%include file="footer.mako"/>