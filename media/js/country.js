$(function(){
    $("select#id_state").change(function(){
      $.getJSON("/razborka/ajax/region_by_state/",{stateid:+$(this).val()}, function(j) {
        var options= '<option value="">---------</option>';
        for (var i = 0; i < j.length; i++) {
          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['title'] + '</option>';
        }
        $("#id_region").html(options);
        $("#id_region option:first").attr('selected', 'selected');
        $("#id_region").attr('disabled', false);
      })
      $("id_state").attr('selected', 'selected');
    })
  })

$(function(){
    $("select#id_region").change(function(){
      $.getJSON("/razborka/ajax/city_by_region/",{regionid:+$(this).val()}, function(j) {
        var options = '<option value="">---------</option>';
        for (var i = 0; i < j.length; i++) {
          options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['title'] + '</option>';
        }
        $("#id_city").html(options);
        $("#id_city option:first").attr('selected', 'selected');
        $("#id_city").attr('disabled', false);
      })
      $("id_region").attr('selected', 'selected');
    })
  })

