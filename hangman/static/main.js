$("#letter-form").submit(function (e) {
  var data = $("#letter-form").serialize();

  $("#letter-form input").val("");

  $.ajax({
    type: "POST",
    url: "",
    data: data,
    success: function (data) {
      if (data.finished) {
        location.reload();
      } else {
        $("#current").text(data.current);

        $("#errors").html(
          "Errors (" +
            data.errors.length +
            "/10): " +
            '<span class="text-danger spaced">' +
            data.errors +
            "</span>"
        );

        updateDrawing(data.errors);
      }
    },
  });
  e.preventDefault();
});

function updateDrawing(errors) {
  $("#hangman-drawing").children().slice(0, errors.length).show();
}
