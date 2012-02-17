<%include file="header.mako"/>
<div class='philologic_cite'>
<span class='title'>${obj.author}, <i>${obj.title}</i></span></div>
% if obj.philo_type == 'doc':
    <% results = navigate_doc(obj.philo_id[0], db) %>
    % for i in results:
        <% href = "./" + "/".join(str(x) for x in i.philo_id[:len(i.philo_id)]) %>
        <a href="${href}">${i.head}</a><br>
    % endfor
% elif q['byte']:
    <div>
    ${navigate_object(obj, query_args=q['byte'])}
    </div>
% else:
    <div>
    ${navigate_object(obj)}
    </div>
% endif
<%include file="footer.mako"/>
