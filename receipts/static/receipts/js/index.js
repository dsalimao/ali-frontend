var app = angular.module('ReceiptsApp', [
  'ui.router',
]);

app.config(function ($stateProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $stateProvider
      .state('index', {
          url: "/receipts/",
          templateUrl: "/static/receipts/html/index.html",
          controller: "ReceiptsIndexCtrl"
      });
});

app.controller("ReceiptsIndexCtrl", ['$scope', '$q',
function ($scope, $q) {
    var a = {store: 'a', time: 'b', totalCost:'c'};
    $scope.latestReceipts = [a,a,a,a];
}]);
