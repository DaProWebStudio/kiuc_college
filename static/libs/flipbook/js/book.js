$(document).ready(function () {
    url_pdf = $('#url_pdf').val()
    $("#flip_book").flipBook({
        pdfUrl: url_pdf,
        viewMode:'3d',
        skin:'white',
        btnSearch: {
            enabled: true,
            title: "Поиск",
            icon: "fas fa-search"
        },
        btnSound : {enabled:false},
        btnAutoplay : {enabled:false},
        btnShare : {enabled:false},
        btnBookmark : {enabled:false},
        btnPrint : {enabled:false},
        btnDownloadPages : {enabled:false},
        btnDownloadPdf : {enabled:false},
    });
    $('#url_pdf').remove()
})