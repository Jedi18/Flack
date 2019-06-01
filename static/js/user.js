document.addEventListener('DOMContentLoaded', () => {
  exists = document.querySelector('#exists').dataset.exists;

  channelname = document.querySelector('#personalchannelname').dataset.name;

  if(exists == "true")
  {
    document.querySelector('#personalchannel').onclick = () => {
      const form = document.createElement('form');
      form.method = 'get';
      form.action = document.querySelector('#channelurl').dataset.url;

      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = "channelname";
      hiddenField.value = channelname;

      form.appendChild(hiddenField);

      document.body.appendChild(form);
      form.submit();
    };
  }else{
    document.querySelector('#personalchannel').onclick = () => {
      /*let firstName = document.querySelector('#username').dataset.name;
      let lastName = document.querySelector('#userpagename').innerHTML;
      // alphabetically first name comes first - firstnametosecondname
      var channelname;

      if(firstName > lastName)
      {
        let temp = lastName;
        lastName = firstName;
        firstName = temp;
      }

      channelname = firstName + "to" + lastName; */

      const form = document.createElement('form');
      form.method = 'post';
      form.action = document.querySelector('#personalcreateurl').dataset.url;

      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = "name";
      hiddenField.value = channelname;

      form.appendChild(hiddenField);

      document.body.appendChild(form);
      form.submit();
    };
  }
});
