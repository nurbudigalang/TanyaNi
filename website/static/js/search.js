$(document).ready(function () {
  const inputElement = $('#example-search-input');

  inputElement.on('input', function () {
    const inputValue = inputElement.val();
    if (inputValue.length == '') {
      $('#results-list').empty();
    }
    if (inputValue.length != '') {
      $.ajax({
        type: 'GET',
        url: '/api/search',
        data: {
          query: inputValue,
        },
        success: function (data) {
          const resultsList = $('#results-list');
          resultsList.empty();
          resultsList.append(
            '<li class="result-entry border border-1">' +
              '<a href="/searchPage/' +
              inputValue +
              '" class="result-link text-decoration-none">' +
              '<div class="container-fluid p-2">' +
              '<i class="fa fa-search"></i>' +
              '<span> Cari: ' +
              inputValue +
              '</span>' +
              '</div>' +
              '</a>' +
              '</li>'
          );
          let count = 0;
          data.forEach(function (result) {
            if (count < 5) {
              resultsList.append(
                '<li class="result-entry border border-1">' +
                  '<a href="detailPertanyaan/' +
                  result.id +
                  '" class="result-link text-decoration-none">' +
                  '<div class="container-fluid p-2">' +
                  '<span>' +
                  result.judul +
                  '</span>' +
                  '</div>' +
                  '</a>' +
                  '</li>'
              );
              count++;
            }
          });
          resultsList.append(
            '<li class="result-entry border border-1">' +
              '<a href="/buatPertanyaan" class="result-link text-decoration-none">' +
              '<div class="container-fluid p-2">' +
              '<i class="bi bi-plus-circle"></i>' +
              '<span> buat pertanyaan baru' +
              '</span>' +
              '</div>' +
              '</a>' +
              '</li>'
          );
        },
      });
    }
  });
});
