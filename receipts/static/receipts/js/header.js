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
                $scope.curUser = data.data.payload;
              },function(err) {
                console.log(err);
              });
    }

    $scope.login = function() {
        console.log(1111);
        $http.get('/oauth/start_oauth_flow');
    }

}]);