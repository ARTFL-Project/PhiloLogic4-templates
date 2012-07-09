<div class='form_body' style="display:none;">
<form action="${db.locals['db_url'] + "/dispatcher.py/"}" style='width:600px; margin-left:40px; margin-right: auto;'>
<table>
 <tr><td>Query Terms:</td><td><input type='text' name='q' id='q'></input></td></tr>
 <tr><td><select name='method'>
 <option value='proxy'>Within</option>
 <option value='phrase'>Exactly</option>
 </select></td><td>
 <input type='text' name='arg'></input> words.</td></tr>
 
% for facet in db.locals["metadata_fields"]:
    <tr><td>${facet}:</td><td><input type='text' name='${facet}' id="${facet}"></input></td></tr>
% endfor

 <tr><td>Report Generator:</td><td><select name='report' id="report" onchange="showHide(this.value);">
 <option value='concordance' selected="selected">Concordance</option>
 <option value='relevance'>Ranked relevance</option>
 <option value='kwic'>KWIC</option>
 <option value='collocation'>Collocation</option>
 <option value='frequency'>Frequency Table</option>
 <option value='theme_rheme'>Theme Rheme</option></select></td></tr>
 
 <tr id="collocation"><td>Within </td><td><select name='word_num'>
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
 </select> words</td></tr>
 
 <tr id="frequency"><td>Frequency by:</td><td><select name='field'>
% for facet in db.locals["metadata_fields"]:
    <option value='${facet}'>${facet}</option>
% endfor
<input type="radio" name="rate" value="raw" checked/>Normal</input>
<input type="radio" name="rate" value="relative"/>per 10,000</input>
</td></tr>

<tr id="theme_rheme"><td>Word position:</td><td><select name='theme_rheme'>
<option value="front">Front of clause</option>
<option value="end">End of clause</option>
<option value="front_end">Front and end only</option>
<option value="front_middle_end">Front, middle and end</option>
<option value="full">Full report</option>
</select></td></tr>

<tr id="results_per_page"><td>Results per page:</td><td><select name='results_per_page'>
 <option value='20' selected="selected">20</option>
 <option value='50'>50</option>
 <option value='100'>100</option></select></td></tr>
 <tr><td><input type='submit'/></td></tr>
</table>
</form>
</div>