$('a.follow').click(function(e){
    e.preventDefault();
    $.post('/account/users/follow/',
      {
        id: $(this).data('id'),
        action: $(this).data('action')
      },
      function(data){
        if (data['status'] == 'ok') {
          var previous_action = $('a.follow').data('action');

          // toggle data-action
          $('a.follow').data('action',
            previous_action == 'follow' ? 'unfollow' : 'follow');
          // toggle link text
          $('a.follow').text(
            previous_action == 'follow' ? 'Unfollow' : 'Follow');

          // update total followers
          var previous_followers = parseInt(
            $('span.count.followers .total').text());
          $('span.count.followers .total').text(previous_action == 'follow' ?
          previous_followers + 1 : previous_followers - 1);

          // update total followings
          var previous_followings = parseInt(
            $('span.count.following .total').text());
          $('span.count.followeing .total').text(previous_action == 'follow' ?
          previous_followings + 1 : previous_followings - 1);
        }
      }
    );
});