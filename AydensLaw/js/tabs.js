$(function () {

    $('.tabs a').click(function () {
        var tab = this.href.split('#')[1];
        $('#tabbed-content .content').hide().map(function () {
            if (this.id == tab) {
                $(this).fadeIn();
            }
        });
    });
});
