$('.select_send_language').on('change', function() {
  $(this.form).submit();
});

// скролл топ
const scrollBtn = document.querySelector('.upShow');

window.onscroll = () => {
    if (window.scrollY > 500) {
        scrollBtn.classList.remove('upShow__hide');
    } else if (window.scrollY < 500) {
        scrollBtn.classList.add('upShow__hide');
    }
};

scrollBtn.onclick = () => {
    window.scrollTo(0, 0)
}