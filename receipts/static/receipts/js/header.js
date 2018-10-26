//var app = angular.module('ReceiptsApp', [
//  'ui.router',
//  'ngMaterial',
//]);

app.controller("HeaderCtrl", ['$scope', '$q', '$http', '$window',
function ($scope, $q, $http, $window) {
    $scope.curUser = "";

    $scope.getUser = function() {
        $http.get('/oauth/get_user').
            then(function(data) {
            console.log(data.data.payload);
                $scope.curUser = data.data.payload;
              },function(err) {
                console.log(err);
              });
    }

    $scope.login = function() {
        $http.get('/oauth/start_oauth_flow')
            .then(function(data) {
                 $window.location.replace(data.data.payload);
               },function(err) {
                 console.log(err);
               });;
    }

    $scope.getUser();
}]);