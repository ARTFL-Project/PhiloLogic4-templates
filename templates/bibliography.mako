<%include file="header.mako"/>
<form action="./">
<table>
 <tr><td>Query Terms:</td><td><input type='text' name='query'></input></td></tr>
 <tr><td><select name='query_method'>
 <option value='proxy'>Within</option>
 <option value='phrase'>Exactly</option>
 </select></td><td>
 <input type='text' name='query_arg'></input> words.</td></tr>
 </table>
<div class='philologic_response'>
 <p class='description'>Bibliography Report: ${len(results)} results.</p>
 <ol class='philologic_cite_list'>
 % for i in results:
  <li class='philologic_occurrence'>
  % if i.type == 'doc':
  <span class='philologic_cite'>${f.cite.make_doc_cite(i)}</span>
  % else:
  <span class='philologic_cite'>${f.cite.make_div_cite(i)}</span>
  % endif
  </li>
 % endfor
 </ol>
</div>
<input type='submit'/>
</form>
<%include file="footer.mako"/>
