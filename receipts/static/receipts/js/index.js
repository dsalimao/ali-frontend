var app = angular.module('ReceiptsApp', [
  'ui.router',
  'ngMaterial',
]);

app.config(function($stateProvider, $locationProvider, $httpProvider, $mdThemingProvider) {
    $locationProvider.html5Mode(true);
    $mdThemingProvider.theme('aliTheme')
        .primaryPalette('green');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $stateProvider
      .state('index', {
          url: "/receipts/",
          templateUrl: "/static/receipts/html/index.html",
          controller: "ReceiptsIndexCtrl"
      });
});


app.controller("ReceiptsIndexCtrl", ['$scope', '$q', '$http', '$window',
function ($scope, $q, $http, $window) {
    $scope.latestReceipts = [];
    $scope.searchText = '';
    $scope.authed = false;

    $scope.initGmailDataFetching = function() {
         var PROJECT_ID = '864443634019';
         var CLIENT_ID = '864443634019-hlqr4tvv33alp9i8t4ig7h1tf6bajl2l.apps.googleusercontent.com';
         var API_KEY = 'AIzaSyDlQ-f2cHGO3NXBNIyNwexefzTb7-EShhw';
         var SCOPES = 'https://www.googleapis.com/auth/gmail.readonly';
           $window.gapi.client.setApiKey(API_KEY);
           $window.gapi.auth.authorize({
             client_id: CLIENT_ID,
             scope: SCOPES,
             immediate: false
           }, function(authResult) {
                var token = authResult['access_token'];
                if (authResult && !authResult.error) {
                    $scope.listGmail()
                } else {
                  console.log('Auth was not successful');
                }
              }
           );
    };

    $scope.syncReceipts = function() {
        var query = 'from:support@udacity.com';
        $scope.listMessages(query, $scope.getMessages)
    }

    $scope.listMessages = function(query, callback) {
      var getPageOfMessages = function(request, result) {
        request.execute(function(resp) {
          result = result.concat(resp.messages);
          var nextPageToken = resp.nextPageToken;
          if (nextPageToken) {
            request = $window.gapi.client.gmail.users.messages.list({
              'userId': 'me',
              'pageToken': nextPageToken,
              'q': query,
            });
            getPageOfMessages(request, result);
          } else {
            callback(result);
          }
        });
      };
      var initialRequest = $window.gapi.client.gmail.users.messages.list({
        'userId': 'me',
        'q': query,
      });
      getPageOfMessages(initialRequest, []);
    };

    $scope.getMessages = function(results) {
        for (var i=0;i<results.length;i++) {
            var request = $window.gapi.client.gmail.users.messages.get({
                'userId': 'me',
                'id': results[i].id,
              });
              request.execute(function(response) {
              console.log(response);
              });
        }
    }

    $scope.searchReceipts = function() {
        var tod1 = new Date();
        if ($scope.toDate) {
            tod1 = new Date($scope.toDate.getTime());
            tod1.setDate($scope.toDate.getDate() + 1);
        }
        var parameter = JSON.stringify({name: $scope.searchText, from: $scope.fromDate, to: tod1});
        $http.post('/receipts/search_receipts', parameter).
            then(function(data) {
                $scope.latestReceipts = data.data.payload;
                $scope.details = [];
              },function(err) {
                console.log(err);
              });
    };

    $scope.getDate = function(time) {
        return time.substring(0, time.indexOf('T'));
    };

    $scope.getCost = function(cost) {
        return '$'+(cost/100).toString();
    };

    $scope.getDetailData = function(id) {
        $http.get('/receipts/get_detail/' + id).
            then(function(data) {
                $scope.details = data.data.payload;
              },function(err) {
                console.log(err);
              });
        $http.get('/receipts/get_raw/' + id).
            then(function(data) {
              },function(err) {
                console.log(err);
              });
    };

    $scope.searchReceipts();
}]);
