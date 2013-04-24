$(function () {

    function show_tab(e) {
        e.preventDefault();
        var tab = this.href.split('#')[1];
        $('#tabbed-content .content').hide().map(function () {
            if (this.id == tab) {
                $(this).fadeIn();
            }
        });
    }

    $('.tabs a').click(show_tab);
    $('.tabs').parent().find('h2 a').click(show_tab);
});
