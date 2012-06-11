<%include file="header.mako"/>
<div class='philologic_response'>
  <div class='initial_report'>
   <p class='description'>
    <%
     start, end, n = f.link.page_interval(results_per_page, len(results), q["start"], q["end"])
    %>
    % if q['theme_rheme'] == 'full':
        <% 
        start = 1 
        end = -1
        %>
    % endif
    Hits <span class="start">${start}</span> - <span class="end">${end}</span> of ${len(results)}
   </p>
  </div>

 <ol class='philologic_concordance'>
  % for i in results[start - 1:end]:
   <li class='philologic_occurrence'>
    <%
     n += 1
    %>
    <span class='hit_n'>${n}.</span> ${f.cite.make_div_cite(i)}
    <br><b>${i.position} of clause: [${i.score} = ${i.percentage}]</b><br>
    <div class='philologic_context'>${i.concordance}</div>
   </li>
  % endfor
 </ol>
 % if q['theme_rheme'] == 'full':
    <div class='theme_rheme_full_report'>Full report:<br>
    Front of clause: ${full_report['Front']} out of ${len(results)}<br>
    Middle of clause: ${full_report['Middle']} out of ${len(results)}<br>
    End of clause: ${full_report['End']} out of ${len(results)}
    </div>
 % endif
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