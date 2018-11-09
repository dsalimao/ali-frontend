app.controller('MenuCtrl', function ($scope, $timeout, $mdSidenav, $log) {
       $scope.toggleMenu = buildToggler('left');
       $scope.isOpenRight = function(){
         return $mdSidenav('right').isOpen();
       };

       /**
        * Supplies a function that will continue to operate until the
        * time is up.
        */
       function debounce(func, wait, context) {
         var timer;

         return function debounced() {
           var context = $scope,
               args = Array.prototype.slice.call(arguments);
           $timeout.cancel(timer);
           timer = $timeout(function() {
             timer = undefined;
             func.apply(context, args);
           }, wait || 10);
         };
       }

       function buildToggler(navID) {
         return function() {
           // Component lookup should always be available since we are not using `ng-if`
           $mdSidenav(navID)
             .toggle()
             .then(function () {
               $log.debug("toggle " + navID + " is done");
             });
         };
       }
     })
     .controller('LeftCtrl', function ($scope, $timeout, $mdSidenav, $log, $window) {
       $scope.goNotebook = function () {
         $window.location.replace('/notebook/');
       };
       $scope.goReceipts = function () {
         $window.location.replace('/receipts/');
       };
       $scope.goAboutAli = function () {
            $window.location.replace('/about/ali/');
          };
       $scope.goAboutMe = function () {
            $window.location.replace('/about/me/');
          };
     });
