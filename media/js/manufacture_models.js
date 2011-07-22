$(function(){
    $("select#id_manufacture").change(function(){
      $.getJSON("razborka/ajax/manufacture_models/",{id:+$(this).val()}, function(j) {
        var options = '<option value="">любая модель</option>';
        for (var i = 0; i < j.length; i++) {
          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['title'] + '</option>';
        }
        $("#id_model").html(options);
        $("#id_model option:first").attr('selected', 'selected');
        $("#id_model").attr('disabled', false);
      })
      $("#id_manufacture").attr('selected', 'selected');
    })
  })
