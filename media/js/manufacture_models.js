
$(function(){
    $("select#id_manufacture").change(function(){
      $.getJSON("/razborka/ajax/manufacture_models/",{id:+$(this).val()}, function(j) {
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


function ReinitElements()
{ 
    for( var i = 0; i < 100; ++i ) 
    { 
        var manufacture = "id_models-" + i + "-manufacture";
        
        selector = document.getElementById( manufacture );
        if( selector!=null && selector.id!="" )
        { 
            DynamicModels( selector );
        }
    }
}
function DynamicModels( element ){ 
    var regex_id = new RegExp('-(\\d+)-');
    var index = regex_id.exec( element.id );
    var id_model = "id_models-" + index[1] + "-model";
    
    selector = document.getElementById( element.id );
    var models = makes[ selector.value ];
    selector_models = document.getElementById( id_model );
    var value = selector_models.value;
    selector_models.innerHTML = "";
    selector_models.innerHTML += ( '<option value="">любая модель</option>' );
    for ( var i = 0; i < models.length; ++i ) { 
        if( value == models[i][0] ){ 
            selector_models.innerHTML += ( '<option selected="selected" value="' + models[i][0] + '">' + models[i][1] + '</option>' );
        }
        else{
            selector_models.innerHTML += ( '<option value="' + models[i][0] + '">' + models[i][1] + '</option>' );
        }
    }
}
                        
function DynamicModelsOld( element ) 
{
    var regex_id = new RegExp('-(\\d+)-');
    var index = regex_id.exec( element.id );
    var id_model = "#id_models-" + index[1] + "-model";
    $(function(){
        $("select#" + element.id).change(function(){
        $.getJSON("/razborka/ajax/manufacture_models/",{id:+$(this).val()}, function(j) {
            var options = '<option value="">любая модель</option>';
            for (var i = 0; i < j.length; i++) {
            options += '<option value="' + parseInt(j[i].pk) + '">' + j[i].fields['title'] + '</option>';
            }
            $("select#" + id_model).html(options);
            $("select#" + id_model +" option:first").attr('selected', 'selected');
            $("select#" + id_model).attr('disabled', false);
        })
        $(element.id).attr('selected', 'selected');
        })
    })
}