$(function () {

    function show_tab(e) {
        e.preventDefault();
        $('.tabs a').removeClass('active');
        var tab = this.href.split('#')[1];
        $('#tabbed-content .content').hide().map(function () {
            if (this.id == tab) {
                $(this).fadeIn();
            }
        });
        $(this).addClass('active');
    }

    $('.tabs a').click(show_tab);
    $('.tabs').parent().find('h2 a').click(show_tab);

    $('#flash').click(function () {
        $(this).fadeOut('slow');
    });
});
