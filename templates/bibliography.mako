<%include file="header.mako"/>
<%namespace file="bibliographic_info.mako" import="bibliography"/>
<form action="./">
<table>
 <tr><td>Query Terms:</td><td><input type='text' name='query'></input></td></tr>
 <tr><td><select name='query_method'>
 <option value='proxy'>Within</option>
 <option value='phrase'>Exactly</option>
 </select></td><td>
 <input type='text' name='query_arg'></input> words.</td></tr>
 </table>

<div class='philologic_concordance'>
 <p class='description'>Bibliography Report: ${len(results)} results.</p>
 <ol>
  ${bibliography(results, 'author', 'title', form=True)}
 </ol>
</div>
<input type='submit'/>
</form>
<%include file="footer.mako"/>
