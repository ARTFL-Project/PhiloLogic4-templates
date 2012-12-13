<div class='form_body'>
<form action="${db.locals['db_url'] + "/dispatcher.py/"}">
<table>
 <tr><td>Query Terms:</td><td><input type='text' name='q' id='q'></input></td></tr>
 <tr><td><select name='method' id='method'>
 <option value='proxy'>Within x words</option>
 <option value='phrase'>Exactly x words</option>
 <option value='sentence'>Within x sentences</option>
 </select></td><td>
 <input type='text' name='arg' id='arg'></input></td></tr>
 
% for facet in db.locals["metadata_fields"]:
    <tr><td class="search_table">${facet}:</td class="search_table"><td class="search_table"><input type='text' name='${facet}' id="${facet}"></input></td class="search_table"></tr>
% endfor

 <tr><td class="search_table">Report Generator:</td class="search_table"><td class="search_table"><select name='report' id="report">
 <option value='concordance' selected="selected">Concordance</option>
 <option value='relevance'>Ranked relevance</option>
 <option value='kwic'>KWIC</option>
 <option value='collocation'>Collocation</option>
 <option value='frequency'>Frequency Table</option>
 <option value='theme_rheme'>Theme Rheme</option></select></td class="search_table"></tr>
 
 <tr id="collocation"><td class="search_table">Within </td class="search_table"><td class="search_table"><select name='word_num' id='word_num'>
 <option value='1'>1</option>
 <option value='2'>2</option>
 <option value='3'>3</option>
 <option value='4'>4</option>
 <option value='5' selected="selected">5</option>
 <option value='6'>6</option>
 <option value='7'>7</option>
 <option value='8'>8</option>
 <option value='9'>9</option>
 <option value='10'>10</option>
 </select> words</td class="search_table"></tr>
 
 <tr id="frequency"><td class="search_table">Frequency by:</td class="search_table"><td class="search_table"><select name='field' id='field'>
% for facet in db.locals["metadata_fields"]:
    <option value='${facet}'>${facet}</option>
% endfor
<input type="checkbox" name="rate" id="rate" value="relative"/>per 10,000</input>
</td class="search_table"></tr>

<tr id="theme_rheme"><td class="search_table">Word position:</td class="search_table"><td class="search_table"><select name='theme_rheme'>
<option value="front">Front of clause</option>
<option value="end">End of clause</option>
<option value="front_end">Front and end only</option>
<option value="front_middle_end">Front, middle and end</option>
<option value="full">Full report</option>
</select></td class="search_table"></tr>

<tr id="results_per_page"><td class="search_table">Results per page:</td class="search_table"><td class="search_table"><select name='results_per_page'n id='page_num'>
 <option value='20'>20</option>
 <option value='50'>50</option>
 <option value='100'>100</option></select></td class="search_table"></tr>
 <tr><td class="search_table"><input type='submit'/></td class="search_table">
 <td class="search_table"><button type="reset" id="reset">Clear form</button></td class="search_table"></tr>
</table>
</form>
</div>