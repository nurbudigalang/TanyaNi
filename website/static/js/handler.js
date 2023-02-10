function bookmarkPost(postId) {
  var bookmarkButton = document.getElementById('bookmark-button-' + postId);
  $.ajax({
    type: 'POST',
    url: '/api/bookmark',
    data: {
      post_id: postId,
    },
    success: function (response) {
      if (bookmarkButton.classList.contains('bi-bookmark-fill')) {
        bookmarkButton.classList.add('bi-bookmark');
        bookmarkButton.classList.remove('bi-bookmark-fill');
      } else {
        bookmarkButton.classList.remove('bi-bookmark');
        bookmarkButton.classList.add('bi-bookmark-fill');
      }
      if (window.location.pathname == '/disimpan') {
        $.ajax({
          type: 'GET',
          url: '/api/bookmark/count',
          data: {},
          success: function (count) {
            document.getElementById('post-' + postId).remove();
            if (count == '0') {
              document.getElementById('kosong').classList.remove('d-none');
            }
          },
        });
      }
    },
  });
}

function likeDislikeJawaban(jawabanId, tipe) {
  var likeButton = document.getElementById('like-button-' + jawabanId);
  var likeCount = document.getElementById('like-count-' + jawabanId);
  var dislikeButton = document.getElementById('dislike-button-' + jawabanId);
  var dislikeCount = document.getElementById('dislike-count-' + jawabanId);
  $.ajax({
    type: 'POST',
    url: '/api/jawaban/like_dislike',
    data: {
      jawaban_id: jawabanId,
      tipe: tipe,
    },
    success: function (response) {
      $.ajax({
        type: 'GET',
        url: '/api/jawaban/like_dislike_count',
        data: {
          jawaban_id: jawabanId,
        },
        success: function (count) {
          likeCount.innerHTML = count.like;
          dislikeCount.innerHTML = count.dislike;
          if (tipe === 'like') {
            if (
              likeButton.firstElementChild.classList.contains(
                'bi-hand-thumbs-up-fill'
              )
            ) {
              likeButton.firstElementChild.classList.add('bi-hand-thumbs-up');
              likeButton.firstElementChild.classList.remove(
                'bi-hand-thumbs-up-fill'
              );
            } else {
              likeButton.firstElementChild.classList.remove(
                'bi-hand-thumbs-up'
              );
              likeButton.firstElementChild.classList.add(
                'bi-hand-thumbs-up-fill'
              );
            }
            dislikeButton.firstElementChild.classList.remove(
              'bi-hand-thumbs-down-fill'
            );
            dislikeButton.firstElementChild.classList.add(
              'bi-hand-thumbs-down'
            );
          } else {
            if (
              dislikeButton.firstElementChild.classList.contains(
                'bi-hand-thumbs-down-fill'
              )
            ) {
              dislikeButton.firstElementChild.classList.add(
                'bi-hand-thumbs-down'
              );
              dislikeButton.firstElementChild.classList.remove(
                'bi-hand-thumbs-down-fill'
              );
            } else {
              dislikeButton.firstElementChild.classList.remove(
                'bi-hand-thumbs-down'
              );
              dislikeButton.firstElementChild.classList.add(
                'bi-hand-thumbs-down-fill'
              );
            }
            likeButton.firstElementChild.classList.remove(
              'bi-hand-thumbs-up-fill'
            );
            likeButton.firstElementChild.classList.add('bi-hand-thumbs-up');
          }
        },
      });
    },
  });
}

function getDate(date) {
  const now = new Date();
  const postDate = new Date(date);
  const diff = now - postDate;

  if (diff < 24 * 60 * 60 * 1000) {
    const second = diff / 1000;
    if (second < 3600) {
      return Math.floor(second / 60) + ' menit yang lalu';
    } else {
      return Math.floor(second / 3600) + ' jam yang lalu';
    }
  } else {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return postDate.toLocaleDateString('id-ID', options);
  }
}

(function () {
  'use strict';

  var forms = document.querySelectorAll('.needs-validation');

  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      'submit',
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add('was-validated');
      },
      false
    );
  });
})();
