document.addEventListener('DOMContentLoaded', function(){
    const socket = new WebSocket('ws://' + window.location.host + '/ws/data/');

    socket.onopen = function(event) {
        socket.send(JSON.stringify({'message': 'Hello.'}))
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data).data;
        const dataPcs = document.getElementById('pcs_data');
        const dataBattery = document.getElementById('battery_data');
        const dataPv = document.getElementById('pv_data');
        dataPcs.innerHTML = '';
        dataBattery.innerHTML = '';
        dataPv.innerHTML = '';
        data.forEach(function(item) {
            const key = parseInt(item[0])
            if (key < 9){
                const td = style(key, item[1]);
                dataPcs.appendChild(td);
            } else if (key >= 9 && key < 18) {
                const td = style(key, item[1]);
                dataBattery.appendChild(td);
            } else if (key >= 18) {
                const td = style(key, item[1]);
                dataPv.appendChild(td);
            }
        });
    }

    socket.onclose = function(event) {
        console.log('WebSocket is closed.', event);
    };
});

function style(key, value){
    const td = document.createElement('td');
    td.className = 'text-center whitespace-nowrap py-2';
    
    if ( key < 3 || ( key >= 9 && key < 12 ) ){
        td.textContent = `${value}V`;
    } else if ( (key >= 3 && key < 6) || ( key >= 12 && key < 15 ) ) {
        td.textContent = `${value}A`
    } else if ( key == 6 || key == 15 || key == 18 ) {
        td.textContent = `${value}kW`
    } else if ( key == 7 ) {
        td.textContent = `${value}Hz`
    } else if ( key == 8 ) {
        td.textContent = `${value}kWh`
        td.id = 'accumulate_energy'
    } else if ( key >= 16 && key < 18) {
        td.textContent = `${value}%`
    }
    
    return td;
}