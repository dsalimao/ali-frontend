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

app.controller("ReceiptsIndexCtrl", ['$scope', '$q', '$http',
function ($scope, $q, $http) {
    $scope.latestReceipts = [];

    var parameter = JSON.stringify({});
    $http.post('/receipts/search_receipts', parameter).
    then(function(data) {
        $scope.latestReceipts = data.data.payload;
      },function(err) {
        console.log(err);
      });

    $scope.getDate = function(time) {
        return time.substring(0, time.indexOf('T'));
    };

    $scope.getCost = function(cost) {
        return '$'+(cost/100).toString();
    };

    $scope.getDetailData = function(id) {
        console.log($scope.selected);
        $http.get('/receipts/get_detail/' + id).
            then(function(data) {
                $scope.details = data.data.payload;
              },function(err) {
                console.log(err);
              });
    };
}]);
