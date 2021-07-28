$('#id_location-0-name').on('keyup', function(){
    var name = this.value
    if (name.length > 2) {
        fetch(`http://localhost:8800/api/find_full_names/?find=${name}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(result => {
            const datalist = document.getElementById('locations')
            $('#locations').empty()
            result.forEach(function(item) {
                let opt = document.createElement('option');
                opt.value = item.name;
                opt.id = item.id
                opt.classList.add('small')
                opt.innerHTML = item.full_name
                datalist.appendChild(opt);
            });
        })
    }
})

$('#id_location-0-name').change(function(){    
    var option = $('option[value="'+$(this).val()+'"]');    
    if (option.length) {
        $('#id_location-0-search_id').val(option.attr("id")); 
    }
})

