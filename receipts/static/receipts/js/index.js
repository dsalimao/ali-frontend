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
        console.log(data.data);
        $scope.latestReceipts = data.data.payload;
        console.log($scope.latestReceipts);
      },function(err) {
        console.log(err);
      });

    $scope.getDate = function(time) {
        return time.substring(0, time.indexOf('T'));
    };

    $scope.getCost = function(cost) {
        return '$'+(cost/100).toString();
    };
}]);
