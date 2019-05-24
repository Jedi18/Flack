document.addEventListener('DOMContentLoaded', () => {

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
      document.querySelector('#enterbutton').onclick = () => {
        const message = document.querySelector('#message_in').value;
        const channelid = document.querySelector('#channelid').dataset.id;
        socket.emit('submit message', {'message':message, 'channelid':channelid});
      };
  });

  socket.on('message recieve', (data) => {
    var div = document.createElement('div');
    div.innerHTML = `${data}<br>`;
    document.querySelector('#messages').appendChild(div);
  });

});