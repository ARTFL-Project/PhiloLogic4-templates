<%def name="make_cite(i, make_object_link, n)">
    <%
    section_href = make_object_link(i.philo_id[:3], i.bytes)
    sub_section_href = make_object_link(i.philo_id[:4], i.bytes)
    para_href = make_object_link(i.philo_id[:5], i.bytes)
    section_names = i.head.split(',')
    if not section_names[0]:
        section_name = 'Header'
        sub_section_name = ''
        speaker_name = ''
    elif section_names[0].startswith('Dramatis'):
        section_name = section_names[0]
        sub_section_name = ''
        speaker_name = ''
    else:
        section_name = section_names[0]
        try:
            sub_section_name = section_names[1]
        except IndexError:
            sub_section_name = section_name
        speaker_name = i.who
    %>
    ${n}. ${i.author}, <i>${i.title}</i> : [<a href="${section_href}" class='philologic_cite'>${section_name}</a> |
    <a href="${sub_section_href}" class='philologic_cite'>${sub_section_name}</a> |
    <a href="${para_href}" class='philologic_cite'>${speaker_name}</a>]
</%def>