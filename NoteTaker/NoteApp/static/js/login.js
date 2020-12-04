$(document).ready(() => {
    moveError();
});

function moveError() {
    var error = $('.errorlist');
    error.detach().appendTo('#form-container form');
}