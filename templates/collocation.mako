<%include file="header.mako"/>
<a href="javascript:void(0)" class="show_search_form">Show search form</a>
<%include file="search_boxes.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<div class='philologic_collocation'>
 <p class='description'>Collocation Report</p>
 <p><b>Search Term: ${q['q'].decode('utf-8', 'ignore')}</b></p>
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
	    <tr><td width="25%"><a href="${link(q, all[0], 'all')}">${all[0]}</a> (${all[1]})</td>
	    <td width="25%"><a href="${link(q, left[0], 'left')}">${left[0]}</a> (${left[1]})</td>
	    <td width="25%"><a href="${link(q, right[0], 'right')}">${right[0]}</a> (${right[1]})</td></tr>

    % endfor

   </table>
 </ol>
</div>
<%include file="footer.mako"/>
