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
    $scope.searchText = '';

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
                console.log(data.data.payload);
              },function(err) {
                console.log(err);
              });
    };

    $scope.searchReceipts();
}]);
