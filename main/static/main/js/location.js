$('#locationId').on('keyup', function(){
    name = this.value
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

