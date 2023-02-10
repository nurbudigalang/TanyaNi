$(document).ready(function () {
  const unReadMessages = $('.unread');
  const markAll = $('#mark_all');
  const notifs = $('.notif-box');

  notifs.on('click', function () {
    const notif = $(this);
    const notifId = notif.attr('id');
    if (notif.hasClass('unread')) {
      notif.removeClass('unread');
    }
    $.ajax({
      type: 'POST',
      url: 'api/notif',
      data: { notif_id: notifId },
      success: function (response) {
        window.location.href = response.redirect_url;
      },
    });
  });

  markAll.on('click', function () {
    unReadMessages.removeClass('unread');
    $.ajax({
      type: 'POST',
      url: 'api/notif',
      data: { notif_id: 'all' },
    });
  });
});
