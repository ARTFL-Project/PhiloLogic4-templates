<script type="text/javascript">
function monkeyPatchAutocomplete() {
    //taken from http://stackoverflow.com/questions/2435964/jqueryui-how-can-i-custom-format-the-autocomplete-plug-in-results    
    
    // don't really need this, but in case I did, I could store it and chain
    var oldFn = $.ui.autocomplete.prototype._renderItem;

    $.ui.autocomplete.prototype._renderItem = function( ul, item) {
        // This regex took some fiddling but should match beginning of string and
        // any match preceded by a string: this is useful for sql matches.
        var re = new RegExp('((^' + this.term + ')|( ' + this.term + '))', "gi") ; 
        var t = item.label.replace(re,"<span style='font-weight:bold;color:Red;'>" + 
                "$&" + 
                "</span>");
        return $( "<li></li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + t + "</a>" )
            .appendTo( ul );
    };
}

var pathname = window.location.pathname.replace('dispatcher.py/', '');

function autocomplete_metadata(metadata, field) {
    $("#" + field).autocomplete({
        source: pathname + "scripts/metadata_list.py?field=" + field,
        minLength: 2,
        dataType: "json"
    });
}

var fields = ${repr(db.locals['metadata_fields'])}


// These functions are for the kwic bibliography which is shortened by default
function showBiblio() {
    $(this).css('background', 'LightGray')
    $(this).children("#full_biblio").css('position', 'absolute').css('text-decoration', 'underline')
    $(this).children("#full_biblio").css('background', 'LightGray')
    $(this).children("#full_biblio").css('display', 'inline')
}

function hideBiblio() {
    $(this).css('background', 'white')
    $(this).children("#full_biblio").hide(200)
}

$(document).ready(function(){
    
    $(".show_search_form").click(function() {
        link = $(this).text()
        if (link == 'Show search form') {
            $(".form_body").slideDown()
            $(this).fadeOut(100).empty().append('Hide search form').fadeIn(100)
        }
        else {
            $(".form_body").slideUp()
            $(this).fadeOut(100).empty().append('Show search form').fadeIn(100)
        }
    });
    
    monkeyPatchAutocomplete();    
    
    $("#q").autocomplete({
        source: pathname + "scripts/term_list.py",
        minLength: 2,
        "dataType": "json"
    });
    for (i in fields) {
        var  metadata = $("#" + fields[i]).val();
        var field = fields[i];
        autocomplete_metadata(metadata, field)
    }
//    The following is to display the right options when using the back button
    if ($("#report option[value='concordance']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").hide()
        $("#results_per_page").show()
    }
    if ($("#report option[value='kwic']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").hide()
        $("#results_per_page").show()
    }
    if ($("#report option[value='collocation']").attr('selected')) {
        $("#frequency").hide()
        $("#results_per_page").hide()
        $("#theme_rheme").hide()
        $("#collocation").show()
    }
    if ($("#report option[value='frequency']").attr('selected')) {
        $("#collocation").hide()
        $("#results_per_page").hide()
        $("#theme_rheme").hide()
        $("#frequency").show()
    }
    if ($("#report option[value='relevance']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").hide()
        $("#results_per_page").show()
    }
    if ($("#report option[value='theme_rheme']").attr('selected')) {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").show()
        $("#results_per_page").show()
    }
    
//  This is for displaying the full bibliogrpahy on mouse hover
//  in kwic reports
    var config = {    
        over: showBiblio, 
        timeout: 100,  
        out: hideBiblio   
    };
    $(".kwic_biblio").hoverIntent(config)

    
// This will show more context for concordance and theme-rheme searches
/*    $(".philologic_occurrence").hover(
        function() {
            $(this).children(".more_context").fadeIn(100);
        },
        function() {
            $(this).children(".more_context").fadeOut(100);
        }
	);
*/
    $(".more_context").click(function() {
        var context_link = $(this).text();
        if (context_link == 'More') {
            $(this).siblings('.philologic_context').children('.begin_concordance').show()
            $(this).siblings('.philologic_context').children('.end_concordance').show()
            $(this).empty().fadeIn(100).append('Less')
        } 
        else {
            $(this).siblings('.philologic_context').children('.begin_concordance').hide()
            $(this).siblings('.philologic_context').children('.end_concordance').hide()
            $(this).empty().fadeIn(100).append('More')
        }
    });
    
//  This will prefill the search form with the current query
    var url = $(location).attr('href');
    var db_url = "${db.locals['db_url']}" + '/dispatcher.py/?';
    var q_string = url.replace(db_url, '');
    var val_list = q_string.split('&');
    for (var i = 0; i < val_list.length; i++) {
        var key_value = val_list[i].split('=');
        var my_value = decodeURIComponent((key_value[1]+'').replace(/\+/g, '%20'));
        var key = $('#' + key_value[0]);
        if (key_value[0] == 'results_per_page') {
            $("#page_num").val(my_value);
        }
        else if (my_value == 'relative') {
            key.prop('checked', true);
        }
        else {
            key.val(my_value);
        }
    }
    
    showHide($("#report").val());
    
    $('#report').change(function() {
        var report = $(this).val();
        showHide(report);
    });
    
    
//  Clear search form
    $("#reset").click(function() {
        $("#q").empty();
        $("#method").val("proxy");
        $("#arg").empty();
        for (i in fields) {
            var field = $("#" + i);
            $(field).empty();
        }
        $("#report").val('concordance');
        $("#results_per_page").val("20");
        showHide('concordance');
    });
    
});

function showHide(value) {
    if (value == 'frequency') {
        $("#collocation").hide()
        $("#results_per_page").hide()
        $("#theme_rheme").hide()
        $("#frequency").show()
    }
    if (value == 'collocation') {
        $("#frequency").hide()
        $("#results_per_page").hide()
        $("#theme_rheme").hide()
        $("#collocation").show()
    }
    if (value == 'concordance' || value == 'kwic' || value == 'relevance') {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").hide()
        $("#results_per_page").show()
    }
    if (value == 'theme_rheme') {
        $("#frequency").hide()
        $("#collocation").hide()
        $("#theme_rheme").show()
        $("#results_per_page").show()
    }
}

</script>