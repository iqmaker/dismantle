    var makes = { '0': [ 'Выберите марку автомобиля' ],
              '1': [ 'CL', 'EL', 'Integra', 'MDX', 'NSX', 'RDX', 'RL', 'RSX', 'TL', 'TSX' ],
              '2': [ '33', '75', '145', '146', '147', '155', '156', '159', '164', '166', 'Alfetta', 'Brera', 'GT', 'GTV', 'Giulietta', 'Spider'] };

            function setMake(){ 
                selector = document.getElementById( 'id_manufacture' );
                //for ( i in selector ) alert( i );

                var models = makes[ selector.value ];
                selector_models = document.getElementById( 'id_model' );
                selector_models.innerHTML = "";
                for ( var i = 0; i < models.length; ++i ) 
                { 
                    selector_models.innerHTML += ( '<option value="' + models[i] + '">' + models[i] + '</option>' );
                }
            }

