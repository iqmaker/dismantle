function set_cookie( c_name, value, exdays ) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}

function popup(mylink, windowname)
{
    if (! window.focus)return true;
    var href;
    if (typeof(mylink) == 'string')
    {
        href=mylink;
    }
    else
    {
        href=mylink.href;
    }
    window.open(href, windowname, 'width=500,height=400,scrollbars=yes');
    return false;
}