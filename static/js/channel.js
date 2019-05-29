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
    div.innerHTML = `${data['sentby']} : ${data['mess']}<br>${data['senton']}<div class="float right">
    <button id="deletemessage" data-id="${data['id']}">Delete</button></div><br><br>`;
    document.querySelector('#messages').appendChild(div);
  });

});
