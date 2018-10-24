var PROJECT_ID = '864443634019';
     var CLIENT_ID = '864443634019-g2ode4789suq2rdi8on0slfjb3obe0rq.apps.googleusercontent.com';
     var API_KEY = 'AIzaSyCtPNydDlJTSOwXloDSW4ZMYpiqNcQJ8yc';
     var SCOPES = 'https://www.googleapis.com/auth/compute';

     /**
      * Authorize Google Compute Engine API.
      */
     function authorization() {
       gapi.client.setApiKey(API_KEY);
       gapi.auth.authorize({
         client_id: CLIENT_ID,
         scope: SCOPES,
         immediate: false
       }, function(authResult) {
            if (authResult && !authResult.error) {
              window.alert('Auth was successful!');
            } else {
              window.alert('Auth was not successful');
            }
          }
       );
     }

     /**
      * Driver for sample application.
      */
     authorization();