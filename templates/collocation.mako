<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<div class='philologic_collocation'>
 <p class='description'>Collocation Report</p>
 <p><b>Search Term: ${q['q']}</b></p>
 <p>Your search found ${len(results)} occurrences</p>
 <ol>
  <% colloc_results = fetch_collocation(results, path, q) %>
   <table border="1" class="philologic_table">
     <colgroup span="3"></colgroup>
     <tr>
      <th>within ${q['word_num']} words on either side</th>
      <th>within ${q['word_num']} words to left</th>
      <th>within ${q['word_num']} words to right</th>
     </tr>

    % for all, left, right in colloc_results:
        <% 
        right_q = q['q'] + ' %s' % right[0]
        left_q = '%s ' % left[0] + q['q']
        q['arg'] = q['word_num']
        href_left = h.make_query_link(left_q,q["method"],q["arg"],**q["metadata"])
        href_right = h.make_query_link(right_q,q["method"],q["arg"],**q["metadata"])
        %>
	    <tr><td width="25%">${all[0]} (${all[1]})</td>
	    <td width="25%"><a href="${href_left}">${left[0]}</a> (${left[1]})</td>
	    <td width="25%"><a href="${href_right}">${right[0]}</a> (${right[1]})</td></tr>

    % endfor

   </table>
 </ol>
</div>
<%include file="footer.mako"/>
