document.addEventListener('DOMContentLoaded', () => {

  $('html, body').animate({scrollTop:$(document).height()}, 'slow');

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  var pageNumber = 0;

  socket.on('connect', () => {
      document.querySelector('#enterbutton').onclick = () => {
        const message = document.querySelector('#message_in').value;
        const channelid = document.querySelector('#channelid').dataset.id;
        socket.emit('submit message', {'message':message, 'channelid':channelid});
      };

      document.querySelectorAll('.deletemessage').forEach((button) => {
        button.onclick = () => {
        const messageid = button.dataset.id;
        socket.emit('delete message', {'messageid':messageid});
        };
      });
  });

  socket.on('message recieve', (data) => {
    var div = document.createElement('div');

    let userurl = document.querySelector('#userurl').dataset.url + "?name=" + data['sentby'];

    div.innerHTML = `<a href="${userurl}">${data['sentby']}</a> : ${data['mess']}<br>${data['senton']}<div class="float right">
    <button id="deletemessage" data-id="${data['id']}">Delete</button></div><br><br>`;
    document.querySelector('#messages').appendChild(div);
    document.querySelector('#message_in').value = "";
  });

  socket.on('message deleted', (data) => {
    divid = "#message" + data['messageid'];
    divtobedel = document.querySelector(divid);
    divtobedel.parentNode.removeChild(divtobedel);
  });

  socket.on('older recieved', (data) => {
    var messages = data['messages'];

    var prevDiv = document.querySelector('.deletemessage').parentNode.parentNode;
    var parentNode = document.querySelector('#messages');

    messages.forEach((message) => {
      let userurl = document.querySelector('#userurl').dataset.url + "?name=" + message['sentby'];
      var div = document.createElement('div');

      div.innerHTML = `<a href="${userurl}">${message['sentby']}</a> : ${message['message']}<br>${message['senton']}<div class="float right">
      <button id="deletemessage" data-id="${message['id']}">Delete</button></div><br><br>`;
      parentNode.insertBefore(div, prevDiv);
      prevDiv = div;
    });
  });

  window.onscroll = () => {
    if(window.scrollY == 0)
    {
      //var firstOne = document.querySelector('.deletemessage').parentNode.parentNode;
      //var topmessageid = firstOne.id;
      //topmessageid = topmessageid.substr(topmessageid.length - 2, 2);
      pageNumber++;
      channelId = document.querySelector('#channelid').dataset.id;
      socket.emit('retrieve older', {"pageNumber":pageNumber, "channelId":channelId});
    }
  };

});
